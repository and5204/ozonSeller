import time


class CreateDraftDirect:
    def __init__(self, ozon_api):
        self.ozon_api = ozon_api

    # =========================
    # CLUSTERS
    # =========================

    def returnClusters(self, place):
        if place == "SNG":
            return self.removeResponseClaster(self.ozon_api.getAllClustersSNG())
        elif place == "RUS":
            return self.removeResponseClaster(self.ozon_api.getAllClustersRussia())

    def removeResponseClaster(self, response):
        result = []

        for cluster in response.get("clusters", []):
            warehouses_result = []

            for lc in cluster.get("logistic_clusters", []):
                for wh in lc.get("warehouses", []):
                    warehouses_result.append({
                        "name": wh.get("name"),
                        "type": wh.get("type"),
                        "warehouse_id": wh.get("warehouse_id"),
                    })

            result.append({
                "macrolocal_cluster_id": cluster.get("macrolocal_cluster_id"),
                "name": cluster.get("name"),
                "type": cluster.get("type"),
                "warehouses": warehouses_result
            })

        return result

    # =========================
    # STORAGE WAREHOUSES (для DIRECT)
    # =========================

    def returnPointsToShipSuppliesDIRECT(self, search_text: str):
        raw_response = self.ozon_api.searchForPointsToShipSuppliesDIRECT(search_text)
        print(raw_response)
        return self.formatPointsToShipSupplies(raw_response)

    def formatPointsToShipSupplies(self, response: dict):
        result = []

        for item in response.get("search", []):
            result.append({
                "warehouse_id": item.get("warehouse_id"),
                "name": item.get("name"),
                "type": item.get("warehouse_type")
            })

        return {"warehouses": result}

    # =========================
    # PRODUCTS
    # =========================

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

    # =========================
    # DRAFT (DIRECT)
    # =========================

    def createDraft(self, macrolocal_cluster_id, quantity, sku):
        return self.ozon_api.draftCreaterDirect(
            quantity,
            sku,
            macrolocal_cluster_id
        )

    def draftInfo(self, draft_id):
        response = self.ozon_api.draftInformation(draft_id)
        status = response.get("status")

        if status != "SUCCESS":
            if status == "FAILED":
                return {
                    "status": status,
                    "errors": response.get("errors", []),
                }

            for _ in range(3):
                if status in ["UNSPECIFIED", "IN_PROGRESS"]:
                    time.sleep(30)
                    response = self.ozon_api.draftInformation(draft_id)
                    status = response.get("status")

        return response

    # =========================
    # TIMESLOT
    # =========================

    def timeSlot(self, date_from, date_to, draft_id, macrolocal_cluster_id, storage_warehouse_id):
        return self.ozon_api.getTimeslotDirect(
            date_from,
            date_to,
            draft_id,
            macrolocal_cluster_id,
            storage_warehouse_id
        )

    # =========================
    # SUPPLY
    # =========================

    def createSupply(self, draft_id, macrolocal_cluster_id, storage_warehouse_id, from_in_timezone, to_in_timezone):
        return self.ozon_api.createSupplyDirect(
            draft_id,
            macrolocal_cluster_id,
            storage_warehouse_id,
            from_in_timezone,
            to_in_timezone
        )

    def supplyInformatin(self, draft_id):
        return self.ozon_api.supplyInfo(draft_id)