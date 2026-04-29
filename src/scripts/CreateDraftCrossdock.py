import time


class CreateDraftCrossdock:
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
                "macrolocal_cluster_id": cluster.get("macrolocal_cluster_id"),
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
            type = item.get("warehouse_type")
            if type == "WAREHOUSE_TYPE_DELIVERY_POINT":
                type = "DELIVERY_POINT"
            elif type == "WAREHOUSE_TYPE_ORDERS_RECEIVING_POINT":
                type = "ORDERS_RECEIVING_POINT"
            elif type == "WAREHOUSE_TYPE_SORTING_CENTER":
                type = "SORTING_CENTER"
            elif type == "FULL_FILLMENT":
                type = "FULL_FILLMENT"
            elif type == "WAREHOUSE_TYPE_CROSS_DOCK":
                type = "CROSS_DOCK"
            result.append({
                "PointsToShipSupplies_id": item.get("warehouse_id"),
                "name": item.get("name"),
                "type": type
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
                "sku": self.getSKU(product_id)

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

    def createDraft(self, macrolocal_cluster_id, drop_off_warehouse_id, drop_off_warehouse_type, quantity, sku):
        response = self.ozon_api.draftCreaterCrossdock(macrolocal_cluster_id, drop_off_warehouse_id,
                                                       drop_off_warehouse_type, quantity, sku)
        return response

    def draftInfo(self, draft_id):
        response = self.ozon_api.draftInformation(draft_id)
        status = response.get("status")
        if status != "SUCCESS":
            if status == "FAILED":
                return {
                    "status": status,
                    "errors": response.get("errors", []), }
            for i in range(3):
                if status == "UNSPECIFIED" or status == "IN_PROGRESS":
                    time.sleep(30)
                    response = self.ozon_api.draftInformation(draft_id)

        return response

    def timeSlot(self, date_from, date_to, draft_id, macrolocal_cluster_id):
        return self.ozon_api.getTimeslotCrossdock(date_from, date_to, draft_id, macrolocal_cluster_id)

    def createSupply(self, draft_id, macrolocal_cluster_id, from_in_timezone, to_in_timezone):
        return self.ozon_api.createSupplyCrossdock(draft_id, macrolocal_cluster_id, from_in_timezone, to_in_timezone)

    def supplyInformatin(self, draft_id):
        return self.ozon_api.supplyInfo(draft_id)



