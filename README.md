# AppShield — Android Privacy & Malware Risk Analyzer

AppShield analyses an Android application's requested permissions and API
usage patterns to assess its malware/privacy risk, using a machine learning
model trained on real permission-based malware data. Rather than issuing a
blind verdict, it explains which specific features contributed to each
assessment.

This is an educational/research prototype, **not** an antivirus product. It
does not determine whether an app is definitively safe.

## Features

- **Single App Check** — tick an app's permissions, get an instant risk result with explanation
- **Batch Check** — upload a CSV of many apps, get a risk-sorted table
- **Model Insights** — see which features the model relies on most overall

## Dataset

**TUANDROMD (Tezpur University Android Malware Dataset)**
Source: UCI Machine Learning Repository — https://archive.ics.uci.edu/dataset/855/tuandromd
License: Creative Commons Attribution 4.0 (CC BY 4.0)
Citation: Borah, P., Bhattacharyya, D.K., Kalita, J. (2020)

4,464 app instances, 241 features (214 permission-based + 27 API-based),
no missing values. Target: Malware vs Goodware.

**Setup:** download `TUANDROMD.csv` from the link above and place it in the
`data/` folder before running the trainer.

## Running with Docker Compose (recommended)

```bash
docker compose up --build
```

This will:
1. Build the shared image
2. Run the `trainer` service, which trains the model and saves it to `model/model.pkl`
3. Start the `dashboard` service at http://localhost:8501

## Running without Docker (for local testing)

```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

## Project Structure

```
appshield/
├── data/                # place TUANDROMD.csv here (not committed - see .gitignore)
├── model/               # model.pkl is generated here after training
├── train_model.py       # trains the classifier
├── app.py                # Streamlit dashboard (3 sections)
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## License

This project's code is licensed under the MIT License (see LICENSE).
The dataset is licensed separately under CC BY 4.0 by its original authors — see Dataset section above.
