from fastapi import FastAPI, HTTPException
from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager

app = FastAPI(title="Ozon Seller API Test")

config = ConfigManager()
ozon_api = OzonApi(
    config.data["client_id"],
    config.data["api_key"]
)

@app.get("/clusters/russia")
def get_clusters_russia():
    try:
        return ozon_api.getAllClustersRussia()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
