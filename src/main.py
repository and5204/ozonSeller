from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.CreateDraftCrossdock import CreateDraft

test = ConfigManager()
testApi = OzonApi(test.data["client_id"], test.data["api_key"])
testDruft = CreateDraft(testApi)
a = testDruft.createDraft(["4040"], 1020000996024000, 10, 1818181172 )
b = testDruft.draftInfo(a.get("operation_id"))
print(a)
print(b)

