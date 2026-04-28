import requests

class OzonApi:
    def __init__(self, client_id, api_key):
        self.base_url = "https://api-seller.ozon.ru/"
        self.headers = {
            "Client-Id": client_id,
            "Api-Key": api_key,
            "Content-Type": "application/json"
        }

    def draftCreaterCrossdock(
            self,
            macrolocal_cluster_id,
            drop_off_warehouse_id,
            drop_off_warehouse_type,
            quantity,
            sku
    ):

        url = f"{self.base_url}/v1/draft/crossdock/create"

        payload = {
            "cluster_info": {
                "items": [
                    {
                        "quantity": quantity,
                        "sku": sku
                    }
                ],
                "macrolocal_cluster_id": macrolocal_cluster_id
            },
            "deletion_sku_mode": "PARTIAL",

            "delivery_info": {
                "drop_off_warehouse": {
                    "warehouse_id": drop_off_warehouse_id,
                    "warehouse_type": drop_off_warehouse_type
                },
                "type": "DROPOFF"
            }
        }

        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def draftCreaterDirect(self, quantity, sku, macrolocal_cluster_id): #https://docs.ozon.ru/api/seller/?__rr=2#operation/SupplyDraftAPI_DraftCreate Создание черновика(не забывай про ограничения запросов)
        url = f"{self.base_url}/v1/draft/direct/create"
        payload = {"cluster_info": {
                    "items": [
                    {
                        "quantity": quantity,
                        "sku": sku
                    }
                            ],
                    "macrolocal_cluster_id": macrolocal_cluster_id
                    },
                    "deletion_sku_mode": "PARTIAL"}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()
    def draftInformation(self, draft_id): #https://docs.ozon.ru/api/seller/?__rr=4&abt_att=2&origin_referer=docs.ozon.ru#operation/SupplyDraftAPI_DraftCreateInfo информация о черновике по его id
        url = f"{self.base_url}/v2/draft/create/info"
        payload = {"draft_id": draft_id}
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
        print(resp.json())
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

    def getProductInfo(self, product_id): #https://docs.ozon.ru/api/seller/?__rr=4&abt_att=1&origin_referer=yandex.ru#operation/ProductAPI_GetProductInfoList получение информации о товаре, в том числе sku
        url = f"{self.base_url}/v3/product/info/list"
        payload = {"product_id": [str(product_id)]}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def getTimeslotCrossdock(self, date_from, date_to, draft_id, macrolocal_cluster_id): #https://docs.ozon.ru/api/seller/?__rr=5&abt_att=2&origin_referer=docs.ozon.ru#operation/DraftTimeslotInfo
        url = f"{self.base_url}/v2/draft/timeslot/info"
        payload = {"date_from": date_from,
                    "date_to": date_to,
                   "draft_id": draft_id,
                   "supply_type": "CROSSDOCK",
                   "selected_cluster_warehouses": [
                    {
                        "macrolocal_cluster_id": macrolocal_cluster_id,
                    }
                    ]}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def getTimeslotDirect(self, date_from, date_to, draft_id, macrolocal_cluster_id, storage_warehouse_id): #https://docs.ozon.ru/api/seller/?__rr=5&abt_att=2&origin_referer=docs.ozon.ru#operation/DraftTimeslotInfo
        url = f"{self.base_url}/v2/draft/timeslot/info"
        payload = {"date_from": date_from,
                    "date_to": date_to,
                   "draft_id": draft_id,
                   "supply_type": "DIRECT",
                   "selected_cluster_warehouses": [
                    {
                        "macrolocal_cluster_id": macrolocal_cluster_id,
                        "storage_warehouse_id" : storage_warehouse_id
                    }
                    ]}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def createSupplyCrossdock(self,draft_id, macrolocal_cluster_id, from_in_timezone, to_in_timezone):
        url = f"{self.base_url}/v2/draft/supply/create"
        payload = {"draft_id": draft_id,
                   "selected_cluster_warehouses": [
                       {
                           "macrolocal_cluster_id": macrolocal_cluster_id
                       }
                   ],
                   "timeslot":
                       {
                           "from_in_timezone": from_in_timezone,
                           "to_in_timezone": to_in_timezone
                       }
                   ,
                   "supply_type" : "CROSSDOCK"}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()
    def createSupplyDirect(self,draft_id, macrolocal_cluster_id, storage_warehouse_id, from_in_timezone, to_in_timezone):
        url = f"{self.base_url}/v2/draft/supply/create"
        payload = {"draft_id": draft_id,
                   "selected_cluster_warehouses": [
                       {
                           "macrolocal_cluster_id": macrolocal_cluster_id,
                           "storage_warehouse_id" : storage_warehouse_id
                       }
                   ],
                   "timeslot":
                       {
                           "from_in_timezone": from_in_timezone,
                           "to_in_timezone": to_in_timezone
                       }
                   ,
                   "supply_type": "DIRECT"}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def supplyInfo(self, draft_id):
        url = f"{self.base_url}/v2/draft/supply/create/status"
        payload = {"draft_id": draft_id}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()