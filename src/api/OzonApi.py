import requests

class OzonApi:
    def __init__(self, client_id, api_key):
        self.base_url = "https://api-seller.ozon.ru/"
        self.headers = {
            "Client-Id": client_id,
            "Api-Key": api_key,
            "Content-Type": "application/json"
        }

    def draftCreater(self, cluster_ids, drop_off_point_warehouse_id, items, type): #https://docs.ozon.ru/api/seller/?__rr=2#operation/SupplyDraftAPI_DraftCreate Создание черновика(не забывай про ограничения запросов)
        url = f"{self.base_url}/v1/draft/create"
        payload = {"cluster_ids": cluster_ids,
                   "drop_off_point_warehouse_id": drop_off_point_warehouse_id,
                   "items": items,
                   "type": type}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def getAllClustersRussia(self): #https://docs.ozon.ru/api/seller/?__rr=2#operation/SupplyDraftAPI_DraftClusterList   Информация о кластерах и их склада в россии
        url = f"{self.base_url}/v1/cluster/list"
        payload = {"cluster_type": "CLUSTER_TYPE_OZON"}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def getAllClustersSNG(self): #https://docs.ozon.ru/api/seller/?__rr=2#operation/SupplyDraftAPI_DraftClusterList   Информация о кластерах и их склада в снг
        url = f"{self.base_url}/v1/cluster/list"
        payload = {"cluster_type": "CLUSTER_TYPE_CIS"}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def searchForPointsToShipSuppliesCROSSDOCK(self, search):  #https://docs.ozon.ru/api/seller/?__rr=3#operation/SupplyDraftAPI_DraftGetWarehouseFboList    Используйте метод, чтобы найти точки отгрузки для кросс-докинга.
        url = f"{self.base_url}/v1/warehouse/fbo/list"
        payload = {"filter_by_supply_type": ["CREATE_TYPE_CROSSDOCK"],
                   "search": str(search)}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def searchForPointsToShipSuppliesDIRECT(self, search):  # https://docs.ozon.ru/api/seller/?__rr=3#operation/SupplyDraftAPI_DraftGetWarehouseFboList      Используйте метод, чтобы найти точки отгрузки для прямых поставок.
        url = f"{self.base_url}/v1/warehouse/fbo/list"
        payload = {"filter_by_supply_type": ["CREATE_TYPE_DIRECT"],
                   "search": str(search)}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def productList(self,
            visibility="VISIBLE",
            offer_ids=None,
            product_ids=None,
            last_id="",
            limit=100): # https://docs.ozon.ru/api/seller/?__rr=4&abt_att=1&origin_referer=yandex.ru#operation/ProductAPI_GetProductList  Метод для получения списка всех товаров.

        url = f"{self.base_url}/v3/product/list"

        filter_data = {
            "visibility": visibility
        }

        if offer_ids:
            filter_data["offer_id"] = offer_ids

        if product_ids:
            filter_data["product_id"] = product_ids

        payload = {
            "filter": filter_data,
            "last_id": last_id,
            "limit": limit
        }

        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()
