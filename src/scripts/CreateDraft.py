
class CreateDraft:
    def __init__(self, ozon_api):
        self.ozon_api = ozon_api

    def returnClusters(self, place):
        if place == "SNG":
            return self.remove_logistics(self.ozon_api.getAllClustersSNG())
        elif place == "RUS":
            return self.remove_logistics(self.ozon_api.getAllClustersRussia())

    def remove_logistics(self, response):
        for cluster in response.get("clusters", []):
            cluster.pop("logistic_clusters", None)
        return response