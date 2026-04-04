import time
from datetime import datetime, timedelta
from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.Bot import Bot
from src.scripts.CreateDraftCrossdock import CreateDraftCrossdock

test = ConfigManager()
testApi = OzonApi(test.data["client_id"], test.data["api_key"])
testDruft = CreateDraftCrossdock(testApi)
testBot = Bot(testDruft)
# print(testBot.makeRequestForDeliveryCrossdock(4065, 1020000996024000,  "SORTING_CENTER", 10, 1818181172))
# print(testDruft.returnClusters("RUS"))
# a = testDruft.createDraft(4065, 1020000996024000,"SORTING_CENTER", 10, 1818181172 )
# print(a)

# b = testDruft.draftInfo(98050721)
#
#
#
# print(b)
# print(testDruft.timeSlot("2026-04-05", "2026-04-29", 98134343, 4065))
# print(testDruft.createSupply(92184414,4065,"2026-03-13T15:00:05","2026-03-29T15:04:05"))
# print(testDruft.supplyInformatin(92184414))
print((datetime.now()+ timedelta(days=28)).strftime("%Y-%m-%dT%H:%M:%S"))
