

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

    def returnPointsToShipSuppliesCROSSDOCK(self, clasterID):
        return self.ozon_api.searchForPointsToShipSuppliesCROSSDOCK(clasterID)
    
    def removeResponsePointsToShip(self, response):
        return 0;
        