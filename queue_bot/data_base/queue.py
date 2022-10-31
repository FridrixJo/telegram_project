import sqlite3


class QueueDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def set_work(self, work, id=1):
        try:
            self.sql.execute("UPDATE `conditions` SET work = ? WHERE id = ?", (work, id))
        except Exception as e:
            print(e, "set_work")
        return self.db.commit()

    def get_work(self, id=1):
        try:
            result = self.sql.execute("SELECT work FROM conditions WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_work")

    def set_head(self, head, id=1):
        try:
            self.sql.execute("UPDATE `conditions` SET head = ? WHERE id = ?", (head, id))
        except Exception as e:
            print(e, "set_head")
        return self.db.commit()

    def get_head(self, id=1):
        try:
            result = self.sql.execute("SELECT head FROM conditions WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_head")

    def set_first(self, first, id=1):
        try:
            self.sql.execute("UPDATE `conditions` SET first = ? WHERE id = ?", (first, id))
        except Exception as e:
            print(e, "set_first")
        return self.db.commit()

    def get_first(self, id=1):
        try:
            result = self.sql.execute("SELECT first FROM conditions WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_first")

    def set_count(self, count, id=1):
        try:
            self.sql.execute("UPDATE `conditions` SET count = ? WHERE id = ?", (count, id))
        except Exception as e:
            print(e, "set_second")
        return self.db.commit()

    def inc_count(self, id=1):
        try:
            self.sql.execute("UPDATE `conditions` SET count = ? WHERE id = ?", (self.get_count() + 1, id))
        except Exception as e:
            print(e, "inc_count")
        return self.db.commit()

    def get_count(self, id=1):
        try:
            result = self.sql.execute("SELECT second FROM conditions WHERE id = ?", (id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_second")

    def reset_conditions(self, id=1):
        try:
            self.sql.execute("UPDATE `conditions` SET count = ? WHERE id = ?", (self.get_count() + 1, id))
        except Exception as e:
            print(e, "inc_count")
        return self.db.commit()

