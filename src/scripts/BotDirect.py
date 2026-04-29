import asyncio
from datetime import datetime, timedelta


class BotDirect:
    def __init__(self, draftDirect):
        self.draftDirect = draftDirect

    def get_error_description(self, error_code: str) -> str:
        descriptions = {
            "UNSPECIFIED": "ошибка не определена",
            "EMPTY_ITEMS_LIST": "передан пустой список items",
            "ITEMS_COUNT_MORE_THAN_MAX": "превышено количество sku",
            "UNKNOWN_CLUSTER_IDS": "кластер не существует",
            "ITEMS_VALIDATION": "ошибки валидации",
            "CAN_NOT_CREATE_DRAFT": "не удалось создать черновик",
            "UNDEFINED": "неизвестная ошибка"
        }
        return descriptions.get(error_code, f"Неизвестная ошибка ({error_code})")

    def get_supply_error_description(self, error_code: str) -> str:
        descriptions = {
            "UNSPECIFIED": "ошибка не определена",
            "ORDER_ALREADY_CREATED": "заказ уже создан",
            "ORDER_CREATION_IN_PROGRESS": "создание заказа в процессе",
            "DRAFT_DOES_NOT_EXIST": "черновик не существует",
            "DRAFT_INCORRECT_STATE": "некорректный статус черновика",
            "DRAFT_IS_LOCKED": "черновик заблокирован",
            "INVALID_STORAGE_WAREHOUSE": "невалидный склад",
            "TIMESLOT_NOT_AVAILABLE": "нет таймслота",
            "UNDEFINED": "неизвестная ошибка"
        }
        return descriptions.get(error_code, f"Неизвестная ошибка ({error_code})")

    def checkTime(self, from_in_timezone, to_in_timezone):
        current = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")

        if datetime.fromisoformat(current) > datetime.fromisoformat(to_in_timezone):
            return 0

        if datetime.fromisoformat(current) > datetime.fromisoformat(from_in_timezone):
            return current

        return from_in_timezone

    async def makeRequestForDeliveryDirect(
        self,
        macrolocal_cluster_id,
        storage_warehouse_id,
        quantity,
        sku,
        from_in_timezone,
        to_in_timezone
    ):

        iteration = 0

        while True:
            iteration += 1
            print(f"\n[LOOP] Итерация: {iteration}")

            draftExist = True

            # ограничение 28 дней
            if datetime.now() + timedelta(days=28) < datetime.fromisoformat(to_in_timezone):
                return "timezoneTo over 28 days"

            # проверка времени
            timeChecked = self.checkTime(from_in_timezone, to_in_timezone)

            if timeChecked == 0:
                return "Time is end"

            from_in_timezone = timeChecked

            # =========================
            # CREATE DRAFT
            # =========================

            print("[DRAFT] Создаём черновик...")
            draft = self.draftDirect.createDraft(
                macrolocal_cluster_id,
                quantity,
                sku
            )

            print("[DRAFT RESPONSE]", draft)

            if "code" in draft:
                if draft["code"] in [8, 429]:
                    print("[RATE LIMIT] ждём 3 минуты")
                    await asyncio.sleep(180)
                    continue
                return draft

            draft_id = draft.get("draft_id")
            if not draft_id:
                return {"error": "нет draft_id"}

            # =========================
            # DRAFT INFO
            # =========================

            while True:
                await asyncio.sleep(10)

                info = self.draftDirect.draftInfo(draft_id)
                print("[DRAFT INFO]", info)
                if "code" in info:
                    if info["code"] == 8:
                        await asyncio.sleep(120)
                        continue
                    draftExist = False
                    break
                invalid_timeslot_reasons = {
                    "NOT_AVAILABLE_TIMESLOT_FOR_DROP_OFF_POINT",
                    "NOT_AVAILABLE_TIMESLOT_FOR_STORAGE_WAREHOUSE",
                    "NOT_AVAILABLE_TIMESLOT_FOR_BOTH_WAREHOUSES",
                    "NOT_AVAILABLE_TIMESLOT_NO_REASON"
                }

                clusters = info.get("clusters", [])

                found_invalid = False

                for cluster in clusters:
                    for wh in cluster.get("warehouses", []):
                        availability = wh.get("availability_status", {})
                        reason = availability.get("invalid_reason")

                        if reason in invalid_timeslot_reasons:
                            print(f"[DRAFT INFO] Нет таймслотов ({reason}) → пересоздаём draft")
                            draftExist = False
                            found_invalid = True
                            await asyncio.sleep(9 * 60)
                            break

                    if found_invalid:
                        break

                if found_invalid:
                    break



                if info.get("status") == "SUCCESS":
                    break

                if info.get("status") == "FAILED":
                    return info

            # =========================
            # TIMESLOTS
            # =========================

            while True:
                await asyncio.sleep(10)

                ts = self.draftDirect.timeSlot(
                    from_in_timezone[:10],
                    to_in_timezone[:10],
                    draft_id,
                    macrolocal_cluster_id,
                    storage_warehouse_id
                )

                print("[TIMESLOT]", ts)

                # === обработка code ===
                if "code" in ts:
                    if ts["code"] == 8:
                        await asyncio.sleep(120)
                        continue
                    draftExist = False
                    break

                result = ts.get("result", {})
                drop_off = result.get("drop_off_warehouse_timeslots", {})

                days = drop_off.get("days", [])

                all_slots = []

                # === правильный парсинг ===
                for day in days:
                    for t in day.get("timeslots", []):
                        all_slots.append(t)

                # === если нет таймслотов ===
                if not all_slots:
                    print("[WAIT] нет таймслотов")
                    await asyncio.sleep(9 * 60)
                    continue

                # === фильтрация (очень рекомендую, как у тебя в crossdock) ===
                from_dt = datetime.fromisoformat(from_in_timezone)
                to_dt = datetime.fromisoformat(to_in_timezone)

                suitable = []
                for t in all_slots:
                    ts_from = datetime.fromisoformat(t["from_in_timezone"])
                    ts_to = datetime.fromisoformat(t["to_in_timezone"])

                    if ts_from >= from_dt and ts_from < to_dt and ts_to <= to_dt:
                        suitable.append(t)

                if not suitable:
                    print("[WAIT] нет подходящих таймслотов")
                    await asyncio.sleep(9 * 60)
                    continue

                # === берём самый ранний ===
                chosen = sorted(suitable, key=lambda x: x["from_in_timezone"])[0]

                from_in_timezone = chosen["from_in_timezone"]
                to_in_timezone = chosen["to_in_timezone"]

                print("[TIMESLOT SELECTED]", from_in_timezone, to_in_timezone)

                break

            # =========================
            # CREATE SUPPLY
            # =========================

            while draftExist:
                await asyncio.sleep(10)

                print("[SUPPLY] создаём...")
                supply = self.draftDirect.createSupply(
                    draft_id,
                    macrolocal_cluster_id,
                    storage_warehouse_id,
                    from_in_timezone,
                    to_in_timezone
                )

                print("[SUPPLY RESPONSE]", supply)

                if "code" in supply:
                    if supply["code"] in [8, 429]:
                        await asyncio.sleep(180)
                        continue
                    if supply.get("code") == 5:
                        draftExist = False
                        continue
                    return supply

                reasons = supply.get("error_reasons") or []

                if not reasons:
                    print("[SUCCESS] supply создан")


                for r in reasons:
                    if r in ["ORDER_ALREADY_CREATED", "ORDER_CREATION_IN_PROGRESS"]:
                        return {"success": True}

                    if r in ["DRAFT_DOES_NOT_EXIST", "DRAFT_IS_LOCKED"]:
                        draftExist = False
                        break
                supplyInfoExist = True
                while supplyInfoExist:
                    await asyncio.sleep(10)
                    supplyInfo = self.draftDirect.supplyInformatin(draft_id)

                    # === обработка rate limit ===
                    if isinstance(supplyInfo, dict) and "code" in supplyInfo:
                        if supplyInfo.get("code") in [429, 8]:
                            print("[WAIT] Rate limit, ждём 5 минут...")
                            await asyncio.sleep(180)
                            continue

                        print(f"[ERROR] Supply API code: {supplyInfo.get('code')}")
                        return supplyInfo

                    status = supplyInfo.get("status")

                    # === SUCCESS ===
                    if status == "SUCCESS":
                        print("SUCCESS")
                        return supplyInfo

                    # === FAILED ===
                    if status == "FAILED":
                        reasons = supplyInfo.get("error_reasons", [])
                        print(f"[SUPPLY FAILED] reasons={reasons}")

                        # 🔁 НУЖНЫЙ КЕЙС — просто выходим из цикла
                        if "TIMESLOT_NOT_AVAILABLE" in reasons:
                            print("[SUPPLY] Таймслот исчез → выходим из цикла, пробуем заново")
                            supplyInfoExist = False
                            supplyExist = False
                            break  # <-- ключевое отличие

                        # ❌ все остальные ошибки — как раньше
                        return supplyInfo
                print("[RETRY] пробуем снова")