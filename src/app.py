import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.api.OzonApi import OzonApi
from src.cancel_state import cancel_flags
from src.config.ConfigManager import ConfigManager
from src.scripts.BdCrossdock import BdCrossdock
from src.scripts.BdDirect import BdDirect
from src.scripts.Bot import Bot
from src.scripts.BotDirect import BotDirect
from src.scripts.CreateDraftCrossdock import CreateDraftCrossdock
from src.scripts.CreateDraftDirect import CreateDraftDirect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class SupplyRequest(BaseModel):
    cluster_id: int
    cluster_name: str

    warehouse_id: int
    warehouse_name: str
    warehouse_type: str

    sku: int
    product_name: str

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
create_draft_direct = CreateDraftDirect(ozon_api)
supplyBotCrossdock = Bot(create_draft)
supplyBotDirect = BotDirect(create_draft_direct)
bdCrossdok = BdCrossdock()
bdDirect = BdDirect()


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
@app.get("/searchWarehouse", response_class=HTMLResponse)
def clusters_page(request: Request):
    return templates.TemplateResponse(
        "searchWarehouse.html",
        {"request": request}
    )
@app.get("/help", response_class=HTMLResponse)
def clusters_page(request: Request):
    return templates.TemplateResponse(
        "/help.html",
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

@app.get("/api/warehousesDirect")
def get_warehouses(cluster_name: str):
    return create_draft_direct.returnPointsToShipSuppliesDIRECT(cluster_name)

@app.get("/api/products")
def get_products(visibility: str = "VISIBLE"):
    return create_draft.returnProductListFormatted(
        visibility=visibility
    )
@app.post("/api/create-supply")
async def create_supply_crossdock(request: SupplyRequest):

    print("[API] Получен запрос:", request)

    addInBd = bdCrossdok.add_request(request.dict())

    if not addInBd.get("success"):
        return addInBd

    request_id = addInBd["id"]

    cancel_flags[request_id] = False

    try:
        result = await supplyBotCrossdock.makeRequestForDeliveryCrossdock(
            macrolocal_cluster_id=request.cluster_id,
            drop_off_warehouse_id=request.warehouse_id,
            drop_off_warehouse_type=request.warehouse_type,
            quantity=request.quantity,
            sku=request.sku,
            from_in_timezone=request.from_time,
            to_in_timezone=request.to_time,
            request_id=request_id   # 🔥 передаём
        )

        print("[API] Результат:", result)

        # === если отменили ===
        if cancel_flags.get(request_id):
            bdCrossdok.update_status(request_id, "canceled", "Остановлено")
            return {"status": "canceled"}

        # === SUCCESS ===
        if isinstance(result, dict) and result.get("status") == "SUCCESS":
            bdCrossdok.update_status(request_id, "done", None)
        else:
            bdCrossdok.update_status(request_id, "error", str(result))

        return result

    except Exception as e:
        bdCrossdok.update_status(request_id, "error", str(e))
        return {"error": str(e)}

    finally:
        cancel_flags.pop(request_id, None)

@app.post("/api/create-supplyDirect")
async def create_supply_direct(request: SupplyRequest):

    print("[API] Получен запрос:", request)

    addInBd = bdDirect.add_request(request.dict())

    if not addInBd.get("success"):
        return addInBd

    request_id = addInBd["id"]

    cancel_flags[request_id] = False

    try:
        result = await supplyBotDirect.makeRequestForDeliveryDirect(
            macrolocal_cluster_id=request.cluster_id,
            storage_warehouse_id=request.warehouse_id,
            quantity=request.quantity,
            sku=request.sku,
            from_in_timezone=request.from_time,
            to_in_timezone=request.to_time,
            request_id=request_id
        )

        print("[API] Результат:", result)

        # === если отменили ===
        if cancel_flags.get(request_id):
            bdDirect.update_status(request_id, "canceled", "Остановлено")
            return {"status": "canceled"}

        # === SUCCESS ===
        if isinstance(result, dict) and result.get("status") == "SUCCESS":
            bdDirect.update_status(request_id, "done", None)
        else:
            bdDirect.update_status(request_id, "error", str(result))

        return result

    except Exception as e:
        bdDirect.update_status(request_id, "error", str(e))
        return {"error": str(e)}

    finally:
        cancel_flags.pop(request_id, None)

@app.post("/api/cancel/{request_id}")
async def cancel_request(request_id: int):

    cancel_flags[request_id] = True

    bdCrossdok.update_status(request_id, "canceled", "Остановлено пользователем")

@app.post("/api/cancelDirect/{request_id}")
async def cancel_request_direct(request_id: int):
    cancel_flags[request_id] = True

    bdDirect.update_status(request_id, "canceled", "Остановлено пользователем")

    return {"success": True}
@app.get("/api/requests")
def get_requests():
    return bdCrossdok.get_all()

@app.get("/api/requestsDirect")
def get_requests_direct():
    return bdDirect.get_all()


