import json
import os

class ConfigManager:
    def __init__(self, path="src/config/settings.json"):
        self.path = path
        if not os.path.exists(self.path):
            self.data = {
                "client_id": "",
                "api_key": "",
            }
            self.save()
        else:
            self.load()

    def load(self): # для закрузки ФАЙЛА
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self): # для сохранения ФАЙЛА
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get(self, key): # для получения данных из словаря data
        return self.data.get(key)

    def set(self, key, value): # для изменения данных в словаре и последующем обновлении данных в Json файле
        self.data[key] = value
        self.save()
