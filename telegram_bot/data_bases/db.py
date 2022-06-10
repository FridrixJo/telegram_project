import sqlite3

class AccountsDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def add_phone_number(self, phone_number):
        try:
            self.sql.execute("INSERT INTO accounts (`phone_number`) VALUES (?)", (phone_number,))
        except Exception as e:
            print(e, "add_account")
        return self.db.commit()


    def account_exists(self, phone_number):
        try:
            result = self.sql.execute("SELECT id FROM accounts WHERE phone_number = ?",(phone_number,))
        except Exception as s:
            print(s, "account_exists")

        return bool(len(result.fetchall()))

    def set_api_id(self, phone_number, api_id):
        try:
            self.sql.execute("UPDATE accounts SET api_id = ? WHERE phone_number = ?", (api_id, phone_number,))
        except Exception as e:
            print(e, "set_api_id")
        return self.db.commit()

    def get_api_id(self, phone_number):
        try:
            result = self.sql.execute("SELECT api_id FROM accounts WHERE phone_number = ?",(phone_number,))
        except Exception as e:
            print(e, "get_api_id")
        return result.fetchall()[0][0]

    def set_api_hash(self, phone_number, api_hash):
        try:
            self.sql.execute("UPDATE accounts SET api_hash = ? WHERE phone_number = ?", (api_hash, phone_number,))
        except Exception as e:
            print(e, "set_api_hash")
        return self.db.commit()

    def get_api_hash(self, phone_number):
        try:
            result = self.sql.execute("SELECT api_hash FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_api_hash")
        return result.fetchall()[0][0]
