import sqlite3


class UsersDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def user_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `users` WHERE `user_id` = ?",(user_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "user_exists")

    def add_user(self, user_id):
        try:
            self.sql.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        except Exception as e:
            print(e, "user_id")
        return self.db.commit()

    def get_users(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def get_users_by_access(self, access):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users` WHERE access = ?", (access,))
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def delete_user(self, user_id):
        try:
            self.sql.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        except Exception as e:
            pass
        return self.db.commit()

    def delete_all(self):
        user_list = self.get_users()
        print(user_list)
        try:
            for i in user_list:
                self.delete_user(i[0])
        except Exception as e:
            print(e)
        return self.db.commit()

    def set_name(self, user_id, name):
        try:
            self.sql.execute("UPDATE `users` SET name = ? WHERE user_id = ?", (name, user_id))
        except Exception as e:
            print(e, "name")
        return self.db.commit()

    def get_name(self, user_id):
        try:
            result = self.sql.execute("SELECT name FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_name")

    def set_access(self, user_id, access):
        try:
            self.sql.execute("UPDATE `users` SET access = ? WHERE user_id = ?", (access, user_id))
        except Exception as e:
            print(e, "access")
        return self.db.commit()

    def get_access(self, user_id):
        try:
            result = self.sql.execute("SELECT access FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_number_hash")

    def set_seconds(self, user_id, seconds):
        try:
            self.sql.execute("UPDATE `users` SET seconds = ? WHERE user_id = ?", (seconds, user_id))
        except Exception as e:
            print(e, "seconds")
        return self.db.commit()

    def get_seconds(self, user_id):
        try:
            result = self.sql.execute("SELECT seconds FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_seconds")

    def set_time(self, user_id, time):
        try:
            self.sql.execute("UPDATE `users` SET time = ? WHERE user_id = ?", (time, user_id))
        except Exception as e:
            print(e, "time")
        return self.db.commit()

    def get_time(self, user_id):
        try:
            result = self.sql.execute("SELECT time FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_time")

    def set_period(self, user_id, period):
        try:
            self.sql.execute("UPDATE `users` SET period = ? WHERE user_id = ?", (period, user_id))
        except Exception as e:
            print(e, "period")
        return self.db.commit()

    def get_period(self, user_id):
        try:
            result = self.sql.execute("SELECT period FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_period")

    def increment_purchases(self, user_id):
        try:
            actual_purchases = self.get_purchases(user_id)
            self.sql.execute("UPDATE `users` SET purchases = ? WHERE user_id = ?", (actual_purchases + 1, user_id))
        except Exception as e:
            print(e, "period")
        return self.db.commit()

    def get_purchases(self, user_id):
        try:
            result = self.sql.execute("SELECT purchases FROM users WHERE user_id = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as e:
            print(e, "get_purchases")

    def get_users_by_period(self, period):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users` WHERE `period` = ?", (period,))
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def get_periods(self):
        try:
            result = self.sql.execute("SELECT period FROM `users`")
            return result.fetchall()
        except Exception as s:
            print(type(s))
