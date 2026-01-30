from http.client import responses


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
        print(raw_response)
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



    def returnProductListFormatted(
            self,
            visibility="VISIBLE",
            offer_ids=None,
            product_ids=None
    ):
        response = self.ozon_api.productList(
            visibility=visibility,
            offer_ids=offer_ids,
            product_ids=product_ids
        )

        result = response.get("result", {})

        items = result.get("items", [])
        total = result.get("total", 0)

        # format only what UI needs
        formatted_items = []
        for item in items:
            formatted_items.append({
                "product_id": item.get("product_id"),
                "offer_id": item.get("offer_id")
            })

        return {
            "total": total,
            "products": formatted_items
        }

    def getSKU(self, product_id):
        response = self.ozon_api.getProductInfo(product_id)
        print(response)
        items = response.get("items", [])
        print(items)
        for item in items:
            if "sku" in item:
                return item["sku"]

        return None



        