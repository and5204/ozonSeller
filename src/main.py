from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager

test = ConfigManager()
testApi = OzonApi(test.data["client_id"], test.data["api_key"])
print(testApi.getAllClustersSNG())
