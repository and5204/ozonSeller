import asyncio
from datetime import datetime, timedelta

from src.cancel_state import cancel_flags


class Bot:
    def __init__(self, draftCrossdock):
        self.draftCrossdock = draftCrossdock

    def get_error_description(error_code: str) -> str:
        """Возвращает понятное описание ошибки по коду error_message."""
        descriptions = {
            "UNSPECIFIED": "ошибка не определена",
            "EMPTY_ITEMS_LIST": "передан пустой список items",
            "ITEMS_COUNT_MORE_THAN_MAX": "превышено количество sku",
            "UNKNOWN_CLUSTER_IDS": "кластер с таким id не существует",
            "ITEMS_VALIDATION": "ошибки валидации товарного состава",
            "DROP_OFF_POINT_DOES_NOT_EXIST": "точка отгрузки с таким id не существует",
            "DROP_OFF_POINT_HAS_NO_TIMESLOTS": "нет доступных таймслотов на точке отгрузки",
            "TOTAL_VOLUME_IN_LITRES_INVALID": "объём поставляемых товаров слишком большой для этой точки",
            "SKU_DISTRIBUTION_REQUIRED_BUT_NOT_POSSIBLE": "требуется распределение SKU, но оно невозможно",
            "CROSS_DOCK_IN_DELIVERY_POINT_DISABLED_FOR_SELLER": "поставка кросс-докингом через пункт выдачи заказов недоступна для продавца",
            "DUPLICATE_SKUS_IN_REQUEST": "в запросе есть дубликаты SKU",
            "CAN_NOT_CREATE_DRAFT": "не удалось создать черновик",
            "DRAFT_TOTALS_INVALID_ERROR": "некорректные итоговые данные в черновике",
            "CAN_NOT_START_CALCULATION": "не удалось начать расчёт",
            "PICKUP_IS_NOT_AVAILABLE": "самовывоз недоступен",
            "DROP_OFF_NOT_COMPATIBLE_WITH_PICKUP": "точка отгрузки несовместима с самовывозом",
            "UNDEFINED": "неизвестная ошибка"
        }
        return descriptions.get(error_code, f"Неизвестная ошибка ({error_code})")

    def get_reason_description(reason_code: str) -> str:
        """Возвращает понятное описание причины ошибки (error_reasons)."""
        descriptions = {
            "UNSPECIFIED": "не определена",
            "ORDER_CREATION_NOT_AVAILABLE_FOR_SELLER": "создание заказов недоступно для продавца",
            "ALL_ITEMS_REJECTED": "все товары отклонены",
            "NOT_AVAILABLE_CLUSTERS": "нет доступных кластеров",
            "ALL_ITEMS_COUNT_INVALID": "в товарном составе больше 5000 SKU",
            "ALL_ITEMS_VOLUME_INVALID": "в товарном составе объём товаров больше 100 000 литров",
            "ALL_BUNDLES_EMPTY": "товарные составы пустые",
            "HAS_EMPTY_BUNDLE": "минимум 1 товарный состав в черновике пустой",
            "DISABLED_FOR_SELLER": "отгрузка курьером отключена для продавца",
            "NO_ACTIVE_SELLER_WAREHOUSE": "нет активного склада продавца",
            "INVALID_SELLER_WAREHOUSE": "склад продавца недоступен",
            "UNDEFINED": "неизвестная причина"
        }
        return descriptions.get(reason_code, f"Неизвестная причина ({reason_code})")

    def get_supply_error_description(error_code: str) -> str:
        """Возвращает понятное описание ошибки для createSupplyCrossdock."""
        descriptions = {
            "UNSPECIFIED": "ошибка не определена",
            "SOME_SERVICE_ERROR": "ошибка при редактировании поставки",
            "ORDER_SKU_LIMIT": "количество товаров в поставке больше 5000",
            "INVALID_QUANTITY_OR_QUANT": "некорректное количество товара или грузомест",
            "ORDER_ALREADY_CREATED": "заказ уже создан",
            "ORDER_CREATION_IN_PROGRESS": "создание заказа в процессе",
            "DRAFT_DOES_NOT_EXIST": "черновик не существует",
            "CONTRACTOR_CAN_NOT_CREATE_ORDER": "контрагент не может создать заказ",
            "INACTIVE_CONTRACT": "нельзя редактировать состав поставки с неактивным договором",
            "DRAFT_INCORRECT_STATE": "некорректный статус черновика",
            "INVALID_VOLUME": "некорректный объём поставки",
            "INVALID_ROUTE": "некорректный маршрут",
            "INVALID_STORAGE_WAREHOUSE": "некорректный склад хранения",
            "INVALID_STORAGE_REGION": "некорректный регион хранения",
            "INVALID_SPLITTING": "некорректное разделение",
            "INVALID_SUPPLY_CONTENT": "некорректное содержимое поставки",
            "TIMESLOT_NOT_AVAILABLE": "нет доступных таймслотов",
            "SKU_DISTRIBUTION_REQUIRED_BUT_NOT_POSSIBLE": "требуется распределение SKU, но оно невозможно",
            "XDOCK_IN_DELIVERY_POINT_DISABLED_FOR_SELLER": "поставка кросс-докингом через пункт выдачи заказов недоступна для продавца",
            "DRAFT_IS_LOCKED": "черновик заблокирован",
            "INVALID_PACKAGE_UNITS_COUNTS": "некорректное количество грузомест",
            "SELLER_CONVERSATION_DOES_NOT_EXIST": "точка отгрузки с таким id не существует",
            "USER_CAN_NOT_CREATE_SELLER_CONVERSATION": "пользователь не может создать диалог с продавцом",
            "SKU_WITH_ETTN_REQUIRED_TAG_NOT_ALLOWED_FOR_DROP_OFF_POINT": "товар с меткой is_ettn_required не разрешён для точки отгрузки",
            "INVALID_SELLER_WAREHOUSE": "склад продавца недоступен",
            "PICKUP_ORDER_LIMIT_EXCEEDED": "превышен лимит заказов на самовывоз",
            "MINIMUM_VOLUME_IN_LITRES_INVALID": "некорректный минимальный объём в литрах",
            "INVALID_CLUSTERS_COUNT": "переданы не все кластеры из расчёта",
            "CAN_NOT_CREATE_ORDER": "не удалось создать заказ",
            "UNDEFINED": "неизвестная ошибка"
        }
        return descriptions.get(error_code, f"Неизвестная ошибка ({error_code})")

    def checkTime(self, from_in_timezone, to_in_timezone):
        fromTZ = None
        currentDatetime = (datetime.now()+ timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S")
        if (datetime.fromisoformat(currentDatetime) > datetime.fromisoformat(to_in_timezone)):
            return 0
        if (datetime.fromisoformat(currentDatetime) > datetime.fromisoformat(from_in_timezone)):
            fromTZ = currentDatetime
            return fromTZ
        return from_in_timezone

    async def makeRequestForDeliveryCrossdock(self, macrolocal_cluster_id, drop_off_warehouse_id, drop_off_warehouse_type,
                                        quantity, sku, from_in_timezone, to_in_timezone, request_id):

        iteration = 0

        while True:
            if cancel_flags.get(request_id):
                print("[CANCEL] Остановлено пользователем")
                return {"status": "canceled"}
            iteration += 1
            print(f"\n[LOOP] Итерация: {iteration}")

            draftExist = True

            if datetime.fromisoformat(
                    (datetime.now() + timedelta(days=28)).strftime("%Y-%m-%dT%H:%M:%S")) < datetime.fromisoformat(
                    to_in_timezone):
                print("[EXIT] to_in_timezone > 28 дней")
                return "timezoneTo over 28 days"

            timeChecked = self.checkTime(from_in_timezone, to_in_timezone)
            print(f"[TIME] from={from_in_timezone}, to={to_in_timezone}, checked={timeChecked}")

            if timeChecked == 0:
                print("[EXIT] Время вышло")
                return "Time is end"
            else:
                from_in_timezone = timeChecked

            print("[DRAFT] Создаём черновик...")
            draft = self.draftCrossdock.createDraft(
                macrolocal_cluster_id,
                drop_off_warehouse_id,
                drop_off_warehouse_type,
                quantity,
                sku
            )

            print(f"[DRAFT RESPONSE] {draft}")

            # Ошибочный формат ответа
            if isinstance(draft, dict) and "code" in draft:
                print(f"[ERROR] Draft API code: {draft.get('code')}")

                if draft.get("code") == 429 or draft.get("code") == 8:
                    print("[WAIT] Rate limit, ждём 5 минут...")
                    await asyncio.sleep(180)
                    continue

                return draft

            draft_id = draft.get("draft_id")

            if draft_id is None:
                print("[ERROR] Нет draft_id")
                return {
                    "error": "В ответе отсутствует draft_id",
                    "raw_response": draft
                }

            print(f"[DRAFT] draft_id={draft_id}")
            draftId = draft_id

            errors = draft.get("errors") or []
            print(f"[DRAFT ERRORS] {errors}")

            critical_errors = []

            for err in errors:
                error_message = err.get("error_message")
                print(f"[DRAFT ERROR] {error_message}")

                if error_message in ["UNSPECIFIED"]:
                    continue

                if error_message in ["DROP_OFF_POINT_HAS_NO_TIMESLOTS"]:
                    print("нет таймслотов")
                    continue

                if error_message in ["CAN_NOT_START_CALCULATION", "UNDEFINED"]:
                    print("[DRAFT] Нельзя использовать, пересоздаём")
                    draftExist = False
                    continue

                description = self.get_error_description(error_message)

                reasons = err.get("error_reasons") or []
                print(f"[DRAFT ERROR REASONS] {reasons}")

                reasons_text = []
                for r in reasons:
                    reasons_text.append(f"{r} — {self.get_reason_description(r)}")

                critical_errors.append({
                    "error_message": error_message,
                    "description": description,
                    "reasons": reasons_text if reasons_text else None
                })

            if critical_errors:
                print(f"[EXIT] Критические ошибки: {critical_errors}")
                return {
                    "draftId": draftId,
                    "success": False,
                    "errors": critical_errors
                }
            draftInfoExist = True
            while draftInfoExist:
                if cancel_flags.get(request_id):
                    print("[CANCEL] Остановлено пользователем")
                    return {"status": "canceled"}
                await asyncio.sleep(10)
                draftInfo = self.draftCrossdock.draftInfo(draftId)
                print(f"[DRAFT INFO] {draftInfo}")

                # === Проверка code ===
                if "code" in draftInfo:
                    code = draftInfo.get("code")
                    print(f"[DRAFT INFO] Получен code={code}")

                    if code == 8:
                        print("[DRAFT INFO] Code 8 — повторяем запрос")
                        await asyncio.sleep(130)
                        continue

                    print(f"[DRAFT INFO] Критический code={code}")
                    draftExist = False
                    break

                # === НОВОЕ: проверка invalid_reason ===
                invalid_timeslot_reasons = {
                    "NOT_AVAILABLE_TIMESLOT_FOR_DROP_OFF_POINT",
                    "NOT_AVAILABLE_TIMESLOT_FOR_STORAGE_WAREHOUSE",
                    "NOT_AVAILABLE_TIMESLOT_FOR_BOTH_WAREHOUSES",
                    "NOT_AVAILABLE_TIMESLOT_NO_REASON"
                }

                clusters = draftInfo.get("clusters", [])

                found_invalid = False

                for cluster in clusters:
                    for wh in cluster.get("warehouses", []):
                        availability = wh.get("availability_status", {})
                        reason = availability.get("invalid_reason")

                        if reason in invalid_timeslot_reasons:
                            print(f"[DRAFT INFO] Нет таймслотов ({reason}) → пересоздаём draft")
                            draftExist = False
                            found_invalid = True
                            await asyncio.sleep(9*60)
                            break

                    if found_invalid:
                        break

                if found_invalid:
                    break

                # === Проверка status ===
                status = draftInfo.get("status")

                if status is None:
                    print("[DRAFT INFO] Нет ни code, ни status")
                    draftExist = False
                    break

                if status == "SUCCESS":
                    print("[DRAFT INFO] Статус SUCCESS — выходим из цикла")
                    draftInfoExist = False
                    break

                print(f"[DRAFT INFO] Статус не SUCCESS: {status}")
                draftExist = False
                break

            # Сюда попадём только при status == "SUCCESS"
            print("[DRAFT INFO] Черновик успешно проверен, продолжаем...")

            timeslot_retry = True
            while timeslot_retry:
                if cancel_flags.get(request_id):
                    print("[CANCEL] Остановлено пользователем")
                    return {"status": "canceled"}
                await asyncio.sleep(10)
                timeslot = self.draftCrossdock.timeSlot(
                    from_in_timezone[:10],
                    to_in_timezone[:10],
                    draftId,
                    macrolocal_cluster_id
                )
                print(f"[TIMESLOT] Ответ: {timeslot}")

                # Проверяем наличие "code"
                if "code" in timeslot:
                    code = timeslot.get("code")
                    if code == 5:
                        print("[TIMESLOT] Code 5 — черновик невалиден")
                        draftExist = False
                        timeslot_retry = False
                        break
                    elif code == 8:
                        print("[TIMESLOT] Code 8 — ждём 130 секунд и повторяем")
                        await asyncio.sleep(130)
                        continue
                    else:
                        print(f"[TIMESLOT] Неизвестный code={code}")
                        return {
                            "success": False,
                            "error": f"Ошибка API при получении таймслотов",
                            "code": code,
                            "raw_response": timeslot
                        }

                # Проверяем error_reason
                error_reason = timeslot.get("error_reason")
                if error_reason in ["INVALID_CLUSTERS_COUNT", "REQUESTED_PERIOD_MORE_THAN_MAX",
                                    "INVALID_REQUESTED_CLUSTER_IDS", "UNDEFINED"]:
                    print(f"[TIMESLOT] Критический error_reason: {error_reason}")
                    draftExist = False
                    timeslot_retry = False
                    break

                # Проверяем наличие таймслотов
                result = timeslot.get("result", {})
                drop_off = result.get("drop_off_warehouse_timeslots", {})
                days = drop_off.get("days", [])

                # Собираем все таймслоты
                all_timeslots = []
                for day in days:
                    for ts in day.get("timeslots", []):
                        all_timeslots.append({
                            "from": ts.get("from_in_timezone"),
                            "to": ts.get("to_in_timezone")
                        })

                if not all_timeslots:
                    print("[TIMESLOT] timeslots пуст — ждём 9 минут и повторяем")
                    await asyncio.sleep(9 * 60)
                    continue

                print(f"[TIMESLOT] Найдено таймслотов: {len(all_timeslots)}")

                # Преобразуем строки в datetime для сравнения
                from_dt = datetime.fromisoformat(from_in_timezone)
                to_dt = datetime.fromisoformat(to_in_timezone)

                # Фильтруем только подходящие таймслоты
                suitable_timeslots = []
                for ts in all_timeslots:
                    ts_from = datetime.fromisoformat(ts["from"])
                    ts_to = datetime.fromisoformat(ts["to"])

                    if ts_from >= from_dt and ts_from < to_dt and ts_to <= to_dt and ts_to > from_dt:
                        suitable_timeslots.append(ts)

                if not suitable_timeslots:
                    print("[TIMESLOT] Нет подходящего таймслота — ждём 9 минут и повторяем")
                    await asyncio.sleep(9 * 60)
                    continue

                # Сортируем по from_in_timezone и берём первый (самый ранний)
                suitable_timeslots.sort(key=lambda x: x["from"])
                new_from = suitable_timeslots[0]["from"]
                new_to = suitable_timeslots[0]["to"]

                print(f"[TIMESLOT] Выбран самый ранний таймслот: {new_from} — {new_to}")
                timeslot_retry = False

            while draftExist:
                if cancel_flags.get(request_id):
                    print("[CANCEL] Остановлено пользователем")
                    return {"status": "canceled"}

                await asyncio.sleep(10)
                print(f"[SUPPLY] Пытаемся создать supply (draft_id={draftId})")

                supply = self.draftCrossdock.createSupply(
                    draftId,
                    macrolocal_cluster_id,
                    new_from,
                    new_to
                )

                print(f"[SUPPLY RESPONSE] {supply}")

                if isinstance(supply, dict) and "code" in supply:
                    if supply.get("code") == 429 or supply.get("code") == 8:
                        print("[WAIT] Rate limit, ждём 5 минут...")
                        await asyncio.sleep(180)
                        continue
                    if supply.get("code") == 5:
                        draftExist = False
                        continue
                    print(f"[ERROR] Supply API code: {supply.get('code')}")
                    return supply

                error_reasons = supply.get("error_reasons") or []
                print(f"[SUPPLY REASONS] {error_reasons}")

                critical_errors = []
                supplyExist = False
                if not error_reasons: #пустой список
                    supplyExist = True

                for reason in error_reasons:
                    print(f"[SUPPLY REASON] {reason}")

                    if reason in ["UNSPECIFIED", "ORDER_ALREADY_CREATED", "ORDER_CREATION_IN_PROGRESS"]:
                        supplyExist = True
                        continue


                    if reason in ["TIMESLOT_NOT_AVAILABLE", "CAN_NOT_CREATE_ORDER", "UNDEFINED"]:
                        continue

                    if reason in ["DRAFT_DOES_NOT_EXIST", "DRAFT_INCORRECT_STATE", "DRAFT_IS_LOCKED"]:
                        print("[SUPPLY] Draft больше невалиден → пересоздание")
                        draftExist = False
                        break

                    description = self.get_supply_error_description(reason)

                    critical_errors.append({
                        "error_reason": reason,
                        "description": description
                    })

                if critical_errors:
                    print(f"[EXIT] Критические ошибки supply: {critical_errors}")
                    return {
                        "success": False,
                        "errors": critical_errors
                    }

                elif supplyExist:
                    if cancel_flags.get(request_id):
                        print("[CANCEL] Остановлено пользователем")
                        return {"status": "canceled"}

                    supplyInfoExist = True
                    while supplyInfoExist:
                        await asyncio.sleep(10)
                        supplyInfo = self.draftCrossdock.supplyInformatin(draftId)

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
                                draftExist = False

                                break  # <-- ключевое отличие

                            # ❌ все остальные ошибки — как раньше
                            return supplyInfo

                else:
                    print("заново")


