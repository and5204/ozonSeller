import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.CreateDraft import CreateDraft
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "ui")
)

# инициализация зависимостей
config = ConfigManager()
ozon_api = OzonApi(
    config.data["client_id"],
    config.data["api_key"]
)
create_draft = CreateDraft(ozon_api)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/clusters", response_class=HTMLResponse)
def clusters_page(request: Request):
    return templates.TemplateResponse(
        "clusters.html",
        {"request": request}
    )


@app.get("/api/clusters")
def get_clusters(place: str):
    """
    place = RUS | SNG
    """
    return create_draft.returnClusters(place)

@app.get("/api/warehouses")
def get_warehouses(cluster_name: str):
    """
    cluster_name = selected cluster name
    """
    return create_draft.returnPointsToShipSuppliesCROSSDOCK(cluster_name)

@app.get("/api/products")
def get_products(visibility: str = "VISIBLE"):
    return create_draft.returnProductListFormatted(
        visibility=visibility
    )

