"""APPSHIELD API: serves the existing Random Forest bundle (model/model.pkl) and the web UI."""
import io, os, time, warnings
import joblib, numpy as np, pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

warnings.filterwarnings("ignore")
bundle = joblib.load(os.getenv("MODEL_PATH", "model/model.pkl"))
model, F = bundle["model"], list(bundle["features"])
IDX = {f: i for i, f in enumerate(F)}
imp = pd.Series(model.feature_importances_, index=F).sort_values(ascending=False)
kind = lambda f: "api" if "->" in f else "permission"
band = lambda p: "low" if p < 0.35 else ("medium" if p < 0.65 else "high")

dataset = None
DATA = os.getenv("DATA_PATH", "data/TUANDROMD.csv")
if os.path.exists(DATA):
    d = pd.read_csv(DATA)
    d.columns = d.columns.str.strip()
    c = d[d.columns[-1]].astype(str).str.strip().str.lower().value_counts()
    dataset = {"apps": int(c.get("malware", 0) + c.get("goodware", 0)),
               "malware": int(c.get("malware", 0)), "goodware": int(c.get("goodware", 0))}

app = FastAPI(title="APPSHIELD")

@app.get("/api/meta")
def meta():
    return {"model": type(model).__name__, "trees": len(model.estimators_), "n_features": len(F),
            "n_permission": sum(kind(f) == "permission" for f in F), "n_api": sum(kind(f) == "api" for f in F),
            "accuracy": bundle.get("test_accuracy"), "dataset": dataset,
            "features": [{"name": f, "kind": kind(f)} for f in F],
            "samples": {"malware": bundle.get("sample_malware", []), "goodware": bundle.get("sample_goodware", [])},
            "top": [{"feature": f, "importance": float(v), "kind": kind(f)} for f, v in imp.head(15).items()]}

class Req(BaseModel):
    features: list[str]

@app.post("/api/analyze")
def analyze(r: Req):
    t0 = time.perf_counter()
    sel = [f for f in dict.fromkeys(r.features) if f in IDX]
    x = np.zeros((1, len(F)))
    for f in sel: x[0, IDX[f]] = 1
    X = pd.DataFrame(x, columns=F)
    t1 = time.perf_counter()
    p = float(model.predict_proba(X)[0, 1]); pred = int(model.predict(X)[0])
    t2 = time.perf_counter()
    ev = []
    if sel:  # leave-one-out: how much would malware probability change without this feature?
        M = np.repeat(x, len(sel), axis=0)
        for i, f in enumerate(sel): M[i, IDX[f]] = 0
        q = model.predict_proba(pd.DataFrame(M, columns=F))[:, 1]
        ev = sorted(({"feature": f, "kind": kind(f), "delta": p - float(q[i]), "importance": float(imp[f])}
                     for i, f in enumerate(sel)), key=lambda e: (-abs(e["delta"]), -e["importance"]))
    t3 = time.perf_counter()
    return {"prob": p, "pred": pred, "band": band(p), "selected": len(sel), "evidence": ev[:8],
            "ms": {"vector": (t1 - t0) * 1e3, "inference": (t2 - t1) * 1e3, "evidence": (t3 - t2) * 1e3}}

def _norm(c):
    c = str(c).strip().upper().replace("ANDROID.PERMISSION.", "")
    return c

@app.get("/api/template")
def template():
    return Response(",".join(F) + "\n" + ",".join("0" for _ in F) + "\n", media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=appshield_template.csv"})

@app.post("/api/batch")
async def batch(file: UploadFile = File(...)):
    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw), sep=None, engine="python", encoding_errors="replace")
    except Exception:
        raise HTTPException(400, "Could not read this file as CSV.")
    if df.shape[1] < 2 or len(df) == 0:
        raise HTTPException(422, "The file needs a header row, one column per feature and at least one app row.")
    # tolerant column matching: ignores case, spaces and the 'android.permission.' prefix
    lookup = {_norm(f): f for f in F}
    cols, label = {}, None
    for c in df.columns:
        if str(c).strip().lower() in ("label", "class", "target"): label = c
        elif _norm(c) in lookup: cols[lookup[_norm(c)]] = c
    if not cols:
        raise HTTPException(422, f"None of the {len(df.columns)} columns match the model's {len(F)} features "
                                 "(permission and API-call names such as READ_SMS). Download the template for the exact format.")
    X = pd.DataFrame({f: pd.to_numeric(df[cols[f]], errors="coerce") if f in cols else 0 for f in F}).fillna(0)
    X = (X > 0).astype(float)
    p = model.predict_proba(X)[:, 1]; pred = model.predict(X)
    bands = [band(v) for v in p]
    out = {"total": len(p), "matched": len(cols), "flagged": int(pred.sum()),
           "bands": {b: bands.count(b) for b in ("low", "medium", "high")},
           "rows": [{"row": i + 1, "prob": float(p[i]), "pred": int(pred[i]), "band": bands[i],
                     "indicators": int(X.iloc[i].sum())} for i in range(len(p))]}
    if label is not None:
        y = df[label].astype(str).str.strip().str.lower().map({"malware": 1, "goodware": 0, "1": 1, "0": 0})
        ok = y.notna()
        if ok.any():
            out["label_agreement"] = float((pred[ok.values] == y[ok].astype(int).values).mean())
            out["labeled"] = int(ok.sum())
            for r, v in zip(out["rows"], y): r["label"] = None if pd.isna(v) else int(v)
    return out

app.mount("/", StaticFiles(directory="static", html=True), name="ui")
