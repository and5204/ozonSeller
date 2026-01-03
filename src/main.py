from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.CreateDraft import CreateDraft

test = ConfigManager()
testApi = OzonApi(test.data["client_id"], test.data["api_key"])
testDruft = CreateDraft(testApi)
print(testDruft.returnPointsToShipSuppliesCROSSDOCK('Казань'))