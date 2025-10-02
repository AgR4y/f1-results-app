from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List, Dict

app = FastAPI(
    title="F1 Results API",
    description="Ergast API からF1のレース結果を取得して、レース名と上位3名を返します。",
    version="0.1.0",
)

# CORS: 将来フロントエンド(別ポート)から叩くときに必要
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 学習用なので広めに許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ERGAST_BASE = "https://api.jolpi.ca/ergast/f1" # Ergast: 無料のF1公開API

@app.get("/results/{year}")
def get_results(year: int) -> List[Dict]:
    """
    エンドポイント（URLのこと）:
      GET /results/{year}
    例: /results/2024

    返り値(JSON):
      [
        {"race": "Bahrain Grand Prix", "top3": ["Verstappen", "Perez", "Sainz"]},
        ...
      ]
    """
    url = f"{ERGAST_BASE}/{year}/results.json?limit=1000"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        # 外部APIへの接続失敗など
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")

    try:
        races_raw = data["MRData"]["RaceTable"]["Races"]
    except (KeyError, TypeError):
        raise HTTPException(status_code=500, detail="Unexpected response format from Ergast")

    results: List[Dict] = []
    for race in races_raw:
        race_name = race.get("raceName", "Unknown Race")
        # 各レースの結果配列から上位3件を取得
        top3_entries = (race.get("Results") or [])[:3]
        # ドライバーの姓（familyName）を取り出す
        top3_names = [
            f'{entry["Driver"].get("familyName", "Unknown")}'
            for entry in top3_entries
            if "Driver" in entry
        ]
        results.append({"race": race_name, "top3": top3_names})

    return results
