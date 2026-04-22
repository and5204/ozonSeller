from contextlib import nullcontext
from datetime import datetime, timedelta
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





    def makeRequestForDeliveryCrossdock(self, macrolocal_cluster_id, drop_off_warehouse_id, drop_off_warehouse_type, quantity, sku, from_in_timezone, to_in_timezone):
        if(datetime.fromisoformat((datetime.now()+ timedelta(days=28)).strftime("%Y-%m-%dT%H:%M:%S")) < datetime.fromisoformat(to_in_timezone)):
            return "timezoneTo over 28 days"
        draft = self.draftCrossdock.createDraft(macrolocal_cluster_id, drop_off_warehouse_id, drop_off_warehouse_type, quantity, sku)
        # 1. Ошибочный формат ответа (с code)
        if isinstance(draft, dict) and "code" in draft:
            return draft  # возвращаем как есть, в том же формате

        # 2. Нормальный ответ с draft_id
        draft_id = draft.get("draft_id")
        if draft_id is None:
            return {
                "error": "В ответе отсутствует draft_id",
                "raw_response": draft
            }

        # Присваиваем в переменную draftId (как просил пользователь)
        draftId = draft_id  # ← здесь сохраняется draft_id

        # 3. Проверяем ошибки
        errors = draft.get("errors")
        critical_errors = []

        for err in errors:
            error_message = err.get("error_message")

            # Игнорируем разрешённые ошибки
            if error_message in ["UNSPECIFIED", "DROP_OFF_POINT_HAS_NO_TIMESLOTS"]:
                continue

            # Собираем описание ошибки
            description = self.get_error_description(error_message)

            # Собираем причины (error_reasons), если они есть
            reasons = err.get("error_reasons")
            reasons_text = []
            for r in reasons:
                reasons_text.append(f"{r} — {self.get_reason_description(r)}")

            critical_errors.append({
                "error_message": error_message,
                "description": description,
                "reasons": reasons_text if reasons_text else None
            })

        # 4. Результат
        if critical_errors:
            return {
                "draftId": draftId,
                "success": False,
                "errors": critical_errors
            }
        while (1):
            supply = self.draftCrossdock.createSupplyCrossdock(self, draftId, macrolocal_cluster_id, from_in_timezone, to_in_timezone)
            # 1. Ошибочный формат ответа (с code)
            if isinstance(supply, dict) and "code" in supply:
                return supply  # возвращаем как есть, в том же формате

            # 3. Проверяем error_reasons
            error_reasons = supply.get("error_reasons")
            critical_errors = []

            for reason in error_reasons:
                # Игнорируем нормальную (пустую) причину
                if reason == "UNSPECIFIED":
                    continue

                description = self.get_supply_error_description(reason)

                critical_errors.append({
                    "error_reason": reason,
                    "description": description
                })

            # 4. Результат
            if critical_errors:
                return {
                    "success": False,
                    "errors": critical_errors
                }
            else:
                # Всё хорошо
                return {
                    "success": True
                }

