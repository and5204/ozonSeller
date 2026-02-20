




class CreateDraft:
    def __init__(self, ozon_api):
        self.ozon_api = ozon_api

    def returnClusters(self, place):
        if place == "SNG":
            return self.removeResponseClaster(self.ozon_api.getAllClustersSNG())
        elif place == "RUS":
            return self.removeResponseClaster(self.ozon_api.getAllClustersRussia())

    def removeResponseClaster(self, response):
        result = []

        # Проходим по всем кластерам
        for cluster in response.get("clusters", []):
            warehouses_result = []

            # В каждом кластере есть logistic_clusters
            for lc in cluster.get("logistic_clusters", []):
                # В каждом logistic_cluster есть список warehouses
                for wh in lc.get("warehouses", []):
                    warehouses_result.append({
                        "name": wh.get("name"),
                        "type": wh.get("type"),
                        "warehouse_id": wh.get("warehouse_id"),
                    })

            # Добавляем обработанный кластер в результат
            result.append({
                "id": cluster.get("macrolocal_cluster_id"),
                "name": cluster.get("name"),
                "type": cluster.get("type"),
                "warehouses": warehouses_result
            })

        return result


    def returnPointsToShipSuppliesCROSSDOCK(self, search_text: str):
        raw_response = self.ozon_api.searchForPointsToShipSuppliesCROSSDOCK(search_text)
        print(raw_response)
        return self.formatPointsToShipSupplies(raw_response)

    def formatPointsToShipSupplies(self, response: dict):
        result = []

        for item in response.get("search", []):
            result.append({
                "PointsToShipSupplies_id": item.get("warehouse_id"),
                "name": item.get("name"),
                "type": item.get("warehouse_type")
            })

        return {"PointsToShipSupplies": result}



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
            product_id = item.get("product_id")

            formatted_items.append({
                "product_id": product_id,
                "offer_id": item.get("offer_id"),
                "sku" : self.getSKU(product_id)

            })

        return {
            "total": total,
            "products": formatted_items
        }

    def getSKU(self, product_id):
        response = self.ozon_api.getProductInfo(product_id)

        items = response.get("items", [])

        for item in items:
            if "sku" in item:
                return item["sku"]

        return None

    def createDraft(self, cluster_ids, drop_off_point_warehouse_id, quantity, sku):
        items = [
            {
                "quantity": quantity,
                "sku": sku
            }
        ]
        response = self.ozon_api.draftCreaterCrossdock(cluster_ids, drop_off_point_warehouse_id, items)
        return response
    def draftInfo(self, operation_id):
        return self.ozon_api.draftInformation(operation_id)





        