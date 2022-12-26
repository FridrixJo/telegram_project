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

    def add_account_manually(self, api_hash, api_id, phone_number, owner_id, status='added', message_count=0):
        try:
            self.sql.execute("INSERT INTO accounts (`phone_number`, `api_id`, `api_hash`, `owner_id`, 'status', `message_count`) VALUES (?, ?, ?, ?, ?, ?)", (phone_number, api_id, api_hash, owner_id, status, message_count))
        except Exception as e:
            print(e, "add_account_manually")
        return self.db.commit()

    def delete_phone_number(self, phone_number):
        try:
            self.sql.execute("DELETE FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            pass
        return self.db.commit()

    def set_owner_id(self, phone_number, owner_id):
        try:
            self.sql.execute("UPDATE accounts SET owner_id = ? WHERE phone_number = ?", (owner_id, phone_number,))
        except Exception as e:
            print(e, "set_owner_id")
        return self.db.commit()

    def get_owner_id(self, phone_number):
        try:
            result = self.sql.execute("SELECT owner_id FROM accounts WHERE phone_number = ?",(phone_number,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_owner_id")

    def get_numbers_by_owner_id(self, owner_id):
        try:
            result = self.sql.execute("SELECT phone_number FROM accounts WHERE owner_id = ?", (owner_id,))
        except Exception as e:
            print(e, "get_api_id")
        return result.fetchall()

    def get_added_numbers_by_owner_id(self, owner_id, status):
        try:
            result = self.sql.execute("SELECT phone_number FROM accounts WHERE owner_id = ? AND status = ?", (owner_id, status,))
        except Exception as e:
            print(e, "get_added_numbers_by_owner_id")
        return result.fetchall()

    def get_all_numbers(self):
        try:
            result = self.sql.execute("SELECT phone_number FROM accounts")
        except Exception as e:
            print(e, "get_all_numbers")
        return result.fetchall()

    def get_all_added_numbers(self, status):
        try:
            result = self.sql.execute("SELECT phone_number FROM accounts WHERE status = ?", (status,))
        except Exception as e:
            print(e, "get_all_added_numbers")
        return result.fetchall()

    def account_exists_by_phone_name(self, phone_number):
        try:
            result = self.sql.execute("SELECT id FROM accounts WHERE phone_number = ?",(phone_number,))
        except Exception as s:
            print(s, "account_exists_by_phone_number")

        return bool(len(result.fetchall()))

    def account_exists_by_api_hash(self, api_hash):
        try:
            result = self.sql.execute("SELECT id FROM accounts WHERE api_hash = ?", (api_hash,))
        except Exception as s:
            print(s, "account_exists_by_api_hash")

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

    def get_phone_number_by_api_hash(self, api_hash):
        try:
            result = self.sql.execute("SELECT phone_number FROM accounts WHERE api_hash = ?", (api_hash,))
        except Exception as e:
            print(e, "get_phone_number_by_api_hash")
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

    def set_number_hash(self, phone_number, number_hash):
        try:
            self.sql.execute("UPDATE accounts SET number_hash = ? WHERE phone_number = ?", (number_hash, phone_number,))
        except Exception as e:
            print(e, "set_number_hash")
        return self.db.commit()

    def get_number_hash(self, phone_number):
        try:
            result = self.sql.execute("SELECT number_hash FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_number_hash")
        return result.fetchall()[0][0]

    def get_list_number_hash(self):
        try:
            result = self.sql.execute("SELECT `number_hash` FROM `accounts`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def set_condition(self, phone_number, condition):
        try:
            self.sql.execute("UPDATE accounts SET condition = ? WHERE phone_number = ?", (condition, phone_number,))
        except Exception as e:
            print(e, "set_condition")
        return self.db.commit()

    def set_same_condition(self, condition):
        try:
            self.sql.execute("UPDATE accounts SET condition = ?", (condition,))
        except Exception as e:
            print(e, "set_same_condition")
        return self.db.commit()

    def get_condition(self, phone_number):
        try:
            result = self.sql.execute("SELECT condition FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_condition")
        return result.fetchall()[0][0]

    def get_all_conditions(self):
        try:
            result = self.sql.execute("SELECT condition FROM accounts")
        except Exception as e:
            print(e, "get_all_conditions")
        return result.fetchall()

    def set_name(self, phone_number, name):
        try:
            self.sql.execute("UPDATE accounts SET name = ? WHERE phone_number = ?", (name, phone_number,))
        except Exception as e:
            print(e, "set_name")
        return self.db.commit()

    def get_name(self, phone_number):
        try:
            result = self.sql.execute("SELECT name FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_name")
        return result.fetchall()[0][0]

    def set_message_count(self, phone_number, message_count):
        try:
            self.sql.execute("UPDATE accounts SET message_count = ? WHERE phone_number = ?", (message_count, phone_number,))
        except Exception as e:
            print(e, "set_message_count")
        return self.db.commit()

    def get_message_count(self, phone_number):
        try:
            result = self.sql.execute("SELECT message_count FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_message_count")
        return result.fetchall()[0][0]

    def get_all_message_count(self):
        try:
            result = self.sql.execute("SELECT message_count FROM accounts")
        except Exception as e:
            print(e, "get_all_message_count")
        return result.fetchall()

    def get_all_message_count_by_user_id(self, owner_id):
        try:
            result = self.sql.execute("SELECT message_count FROM accounts WHERE owner_id = ?", (owner_id,))
        except Exception as e:
            print(e, "get_all_message_count_by_user_id")
        return result.fetchall()

    def set_username(self, phone_number, username):
        try:
            self.sql.execute("UPDATE accounts SET username = ? WHERE phone_number = ?", (username, phone_number,))
        except Exception as e:
            print(e, "set_username")
        return self.db.commit()

    def get_username(self, phone_number):
        try:
            result = self.sql.execute("SELECT username FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_username")
        return result.fetchall()[0][0]

    def set_status(self, phone_number, status):
        try:
            self.sql.execute("UPDATE accounts SET status = ? WHERE phone_number = ?", (status, phone_number,))
        except Exception as e:
            print(e, "set_status")
        return self.db.commit()

    def get_status(self, phone_number):
        try:
            result = self.sql.execute("SELECT status FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_status")
        return result.fetchall()[0][0]

    def set_mailing_message(self, phone_number, mailing_message):
        try:
            self.sql.execute("UPDATE accounts SET mailing_message = ? WHERE phone_number = ?", (mailing_message, phone_number,))
        except Exception as e:
            print(e, "set_mailing_message")
        return self.db.commit()

    def get_mailing_message(self, phone_number):
        try:
            result = self.sql.execute("SELECT mailing_message FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_mailing_message")
        return result.fetchall()[0][0]

    def set_chat(self, phone_number, chat):
        try:
            self.sql.execute("UPDATE accounts SET chat = ? WHERE phone_number = ?", (chat, phone_number,))
        except Exception as e:
            print(e, "set_chat")
        return self.db.commit()

    def get_chat(self, phone_number):
        try:
            result = self.sql.execute("SELECT chat FROM accounts WHERE phone_number = ?", (phone_number,))
        except Exception as e:
            print(e, "get_chat")
        return result.fetchall()[0][0]

    def get_all_chats(self):
        try:
            result = self.sql.execute("SELECT chat FROM accounts",)
        except Exception as e:
            print(e, "get_all_chats")
        return result.fetchall()
