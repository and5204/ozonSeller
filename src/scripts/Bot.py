class Bot:
    def __init__(self, draftCrossdock):
        self.draftCrossdock = draftCrossdock

    def makeRequestForDelivery(self, from_in_timezone, to_in_timezone, draft_id, warehouse_ids):
        timeZone = self.draftCrossdock.timeSlot(from_in_timezone, to_in_timezone, draft_id, warehouse_ids)#"date_from": "2019-08-24T14:15:22Z", "date_to": "2019-08-24T14:15:22Z", "draft_id": 0, "warehouse_ids": ["string"]
        if timeZone.get()

