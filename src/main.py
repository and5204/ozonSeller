import time
from datetime import datetime
from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.CreateDraftCrossdock import CreateDraft

test = ConfigManager()
testApi = OzonApi(test.data["client_id"], test.data["api_key"])
testDruft = CreateDraft(testApi)
# a = testDruft.createDraft(4002, 1020000996024000,"SORTING_CENTER", 10, 1818181172 )
# print(a)
#
# b = testDruft.draftInfo(a.get("draft_id"))
#
#
#
# print(b)
print(testDruft.timeSlot("2026-03-08", "2026-03-20", 90934981, 4002))
# print(testDruft.draftInfo("019c9a3d-3f0d-74af-89b6-610d9fff43f0"))
# print(testDruft.timeSlot("2026-03-04T14:15:22Z", "2026-03-10T22:15:22Z", 90904021, ["1020002007530000"]))
# print(datetime.now())
