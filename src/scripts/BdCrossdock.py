import sqlite3
from datetime import datetime


class BdCrossdock:
    def __init__(self, db_path="requests.db"):
        # Подключаемся к SQLite базе (создастся сама если нет)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Создаём таблицу если её нет
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cluster_id INTEGER,
            cluster_name TEXT,
            warehouse_id INTEGER,
            warehouse_name TEXT,
            warehouse_type TEXT,
            sku INTEGER,
            product_name TEXT,
            quantity INTEGER,
            from_time TEXT,
            to_time TEXT,
            status TEXT,
            error TEXT,
            created_at TEXT
        )
        """)
        self.conn.commit()

    # =========================
    # Добавление новой заявки
    # =========================
    def add_request(self, data: dict):

        self.cursor.execute("""
        INSERT INTO requests (
            cluster_id, cluster_name,
            warehouse_id, warehouse_name, warehouse_type,
            sku, product_name,
            quantity, from_time, to_time,
            status, error, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["cluster_id"],
            data["cluster_name"],

            data["warehouse_id"],
            data["warehouse_name"],
            data["warehouse_type"],

            data["sku"],
            data["product_name"],

            data["quantity"],
            data["from_time"],
            data["to_time"],

            "in_progress",
            None,
            datetime.now().isoformat()
        ))

        self.conn.commit()

        request_id = self.cursor.lastrowid  # 🔥 ВАЖНО

        return {
            "success": True,
            "id": request_id
        }

    # =========================
    # Освобождение места
    # =========================
    def _make_space(self):
        """
        Удаляет последнюю НЕ in_progress заявку.
        Если все in_progress — возвращает False
        """

        # Получаем все записи начиная с самой старой
        self.cursor.execute("""
        SELECT id, status FROM requests
        ORDER BY id ASC
        """)
        rows = self.cursor.fetchall()

        # Идём с конца (самые старые)
        for row in rows:
            req_id, status = row

            if status != "in_progress":
                # Удаляем эту запись
                self.cursor.execute("DELETE FROM requests WHERE id = ?", (req_id,))
                self.conn.commit()
                return True

        # Если все in_progress
        return False

    # =========================
    # Обновление статуса
    # =========================
    def update_status(self, request_id: int, status: str, error: str = None):
        """
        Обновляет статус заявки
        status: in_progress | done | error
        """

        self.cursor.execute("""
        UPDATE requests
        SET status = ?, error = ?
        WHERE id = ?
        """, (status, error, request_id))

        self.conn.commit()

    # =========================
    # Получение всех заявок
    # =========================
    def get_all(self):
        """
        Возвращает список всех заявок (новые сверху)
        """

        self.cursor.execute("""
        SELECT * FROM requests
        ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        result = []
        for r in rows:
            result.append({
                "id": r[0],
                "cluster_id": r[1],
                "cluster_name": r[2],
                "warehouse_id": r[3],
                "warehouse_name": r[4],
                "warehouse_type": r[5],
                "sku": r[6],
                "product_name": r[7],
                "quantity": r[8],
                "from_time": r[9],
                "to_time": r[10],
                "status": r[11],
                "error": r[12],
                "created_at": r[13],
            })

        return result

    # =========================
    # Получение одной заявки
    # =========================
    def get(self, request_id: int):
        self.cursor.execute("""
        SELECT * FROM requests WHERE id = ?
        """, (request_id,))

        r = self.cursor.fetchone()

        if not r:
            return None

        return {
            "id": r[0],
            "cluster_id": r[1],
            "warehouse_id": r[2],
            "warehouse_type": r[3],
            "sku": r[4],
            "quantity": r[5],
            "from_time": r[6],
            "to_time": r[7],
            "status": r[8],
            "error": r[9],
            "created_at": r[10],
        }