import time
from datetime import datetime
from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.CreateDraftCrossdock import CreateDraft

test = ConfigManager()
testApi = OzonApi(test.data["client_id"], test.data["api_key"])
testDruft = CreateDraft(testApi)
# a = testDruft.createDraft(["144"], 1020000996024000, 10, 1818181172 )
# print(a)
#
# b = testDruft.draftInfo(a)
#
#
#
# print(b)
# print(testDruft.draftInfo("019c9a3d-3f0d-74af-89b6-610d9fff43f0"))
print(testDruft.timeSlot("2026-02-26T14:15:22Z", "2026-02-27T22:15:22Z", 89304540, ["1020002007530000"]))
print(datetime.now())
