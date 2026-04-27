import time
from datetime import datetime, timedelta
from src.api.OzonApi import OzonApi
from src.config.ConfigManager import ConfigManager
from src.scripts.Bot import Bot
from src.scripts.CreateDraftCrossdock import CreateDraftCrossdock

import asyncio

async def main():
    test = ConfigManager()

    testApi = OzonApi(
        test.data["client_id"],
        test.data["api_key"]
    )

    testDruft = CreateDraftCrossdock(testApi)
    # print(testDruft.timeSlot("2026-04-28","2026-05-20", 104367917, 4041))
    testBot = Bot(testDruft)
    task1 = asyncio.create_task(
        testBot.makeRequestForDeliveryCrossdock(
            4041, 23268782971000, "FULL_FILLMENT",
            10, 1741556924,
            "2026-04-28T12:00:00", "2026-05-20T18:00:00"
        )
    )

    task2 = asyncio.create_task(
        testBot.makeRequestForDeliveryCrossdock(
            4007, 23268782971000, "FULL_FILLMENT",
            10, 1741556924,
            "2026-04-30T12:00:00", "2026-05-20T18:00:00"
        )
    )

    # Можно обрабатывать результаты по мере готовности
    result1 = await task1
    print(f"Результат 1: {result1}")

    result2 = await task2
    print(f"Результат 2: {result2}")
    # draft = testDruft.createDraft(
    #     4007,
    #     1020001046550000,
    #     "SORTING_CENTER",
    #     10,
    #     1741556924
    # )
    # print(draft)
    # info = testDruft.draftInfo(104367917)
    # print(info)
    # Кластеры
    # clusters = testDruft.returnClusters("RUS")
    # print(clusters)
    # await asyncio.sleep(10)
    # # Создание черновика

    # supply = testDruft.createSupply(104367917, 4041,"2026-04-28T00:00:00","2026-05-10T18:00:00" )
    # print(supply)
    # time.sleep(5)
    # print(testDruft.supplyInformatin(104397528))
    #
    # draft_id = draft.get("draft_id")
    #
    # # Информация по черновику
    # if draft_id:
    #     info = await testDruft.draftInfo(draft_id)
    #     print(info)
    #
    # # Проверка другого draft_id
    # info2 = await testDruft.draftInfo(98050721)
    # print(info2)

    # ВАЖНО: закрыть клиент
    # await testApi.close()
    # print(testDruft.getSKU(1241750289))


if __name__ == "__main__":
    asyncio.run(main())
# print(testDruft.timeSlot("2026-04-05", "2026-04-29", 98134343, 4065))
# print(testDruft.createSupply(92184414,4065,"2026-03-13T15:00:05","2026-03-29T15:04:05"))
# print(testDruft.supplyInformatin(92184414))
# print((datetime.now()+ timedelta(days=28)).strftime("%Y-%m-%dT%H:%M:%S"))