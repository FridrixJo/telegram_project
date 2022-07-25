import sqlite3


class ErrorsDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def add_phone_number(self, phone_number):
        try:
            self.sql.execute("INSERT INTO errors (`phone_number`) VALUES (?)", (phone_number,))
        except Exception as e:
            print(e, "add_account")
        return self.db.commit()

    def delete_phone_number(self, phone_number):
        try:
            self.sql.execute("DELETE FROM errors WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            pass
        return self.db.commit()

    def set_owner_id(self, phone_number, owner_id):
        try:
            self.sql.execute("UPDATE errors SET owner_id = ? WHERE phone_number = ?", (owner_id, phone_number,))
        except Exception as e:
            print(e, "set_owner_id")
        return self.db.commit()

    def get_owner_id(self, phone_number):
        try:
            result = self.sql.execute("SELECT owner_id FROM errors WHERE phone_number = ?",(phone_number,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_owner_id")

    def get_numbers_by_owner_id(self, owner_id):
        try:
            result = self.sql.execute("SELECT phone_number FROM errors WHERE owner_id = ?", (owner_id,))
        except Exception as e:
            print(e, "get_numbers")
        return result.fetchall()

    def get_all_numbers(self):
        try:
            result = self.sql.execute("SELECT phone_number FROM errors")
        except Exception as e:
            print(e, "get_all_numbers")
        return result.fetchall()

    def account_exists(self, phone_number):
        try:
            result = self.sql.execute("SELECT id FROM errors WHERE phone_number = ?",(phone_number,))
        except Exception as s:
            print(s, "account_exists")

        return bool(len(result.fetchall()))

    def set_error_status(self, phone_number, error_status):
        try:
            self.sql.execute("UPDATE errors SET status = ? WHERE phone_number = ?", (error_status, phone_number,))
        except Exception as e:
            print(e, "set_error_status")
        return self.db.commit()

    def get_error_status(self, phone_number):
        try:
            result = self.sql.execute("SELECT status FROM errors WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_error_status")
        return result.fetchall()[0][0]
