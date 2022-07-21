import sqlite3


class Database:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def user_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(s, "user_exists")

        return bool(len(result.fetchall()))

    def no_nickname(self,user_id):
        try:
            result = self.sql.execute("SELECT nickname FROM users WHERE user_id = ?",(user_id,))
        except Exception as s:
            print(s, "nickname_exists")

        #print(result.fetchall()[0][0])
        return result.fetchall()[0][0] is None

    def get_users(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users`")
        except Exception as s:
            print(type(s))
        return result.fetchall()

    def add_user(self, user_id):
        try:
            self.sql.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        except Exception as e:
            print(e, "user_id")
        return self.db.commit()

    def delete_user(self, user_id):
        try:
            self.sql.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        except Exception as e:
            pass
        return self.db.commit()

    def set_sub_time(self, sub_time, user_id):
        try:
            #self.sql.execute("UPDATE `users` SET `sub_time` = ? WHERE `user_id` = ?", (sub_time, user_id,))
            self.sql.execute("UPDATE `users` SET sub_time = ? WHERE user_id = ?", (sub_time, user_id,))
        except Exception as e:
            print(e, "sub_time")
        return self.db.commit()

    def set_nickname(self, nickname, user_id):
        try:
            self.sql.execute("UPDATE `users` SET nickname = ? WHERE user_id = ?", (nickname, user_id))
        except Exception as e:
            print(e, "nickname")
        return self.db.commit()
