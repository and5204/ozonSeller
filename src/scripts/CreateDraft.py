

class CreateDraft:
    def __init__(self, ozon_api):
        self.ozon_api = ozon_api

    def returnClusters(self, place):
        if place == "SNG":
            return self.removeResponseClaster(self.ozon_api.getAllClustersSNG())
        elif place == "RUS":
            return self.removeResponseClaster(self.ozon_api.getAllClustersRussia())

    def removeResponseClaster(self, response):
        for cluster in response.get("clusters", []):
            cluster.pop("logistic_clusters", None)
        return response

    def returnPointsToShipSuppliesCROSSDOCK(self, search_text: str):
        raw_response = self.ozon_api.searchForPointsToShipSuppliesCROSSDOCK(search_text)
        return self.formatWarehouses(raw_response)

    def formatWarehouses(self, response: dict):
        result = []

        for item in response.get("search", []):
            result.append({
                "warehouse_id": item.get("warehouse_id"),
                "name": item.get("name"),
                "type": item.get("warehouse_type")
            })

        return {"warehouses": result}

        