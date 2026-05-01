import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.Bot import Bot
from src.scripts.CreateDraftCrossdock import CreateDraftCrossdock
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class SupplyRequest(BaseModel):
    cluster_id: int
    warehouse_id: int
    warehouse_type: str
    sku: int
    quantity: int
    from_time: str
    to_time: str
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
create_draft = CreateDraftCrossdock(ozon_api)
supplyBotCrossdock = Bot(create_draft)

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
@app.get("/direct", response_class=HTMLResponse)
def direct_page(request: Request):
    return templates.TemplateResponse(
        "direct.html",
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
    return create_draft.returnPointsToShipSuppliesCROSSDOCK(cluster_name)

@app.get("/api/products")
def get_products(visibility: str = "VISIBLE"):
    return create_draft.returnProductListFormatted(
        visibility=visibility
    )
@app.post("/api/create-supply")
async def create_supply_crossdock(request: SupplyRequest):

    print("[API] Получен запрос:", request)

    result = await supplyBotCrossdock.makeRequestForDeliveryCrossdock(
        macrolocal_cluster_id=request.cluster_id,
        drop_off_warehouse_id=request.warehouse_id,
        drop_off_warehouse_type=request.warehouse_type,
        quantity=request.quantity,
        sku=request.sku,
        from_in_timezone=request.from_time,
        to_in_timezone=request.to_time
    )

    print("[API] Результат:", result)

    return result


