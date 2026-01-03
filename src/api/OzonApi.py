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