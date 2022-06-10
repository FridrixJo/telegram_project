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
        except Exception as s:
            print(s, "user_exists")

        return bool(len(result.fetchall()))


    def add_user(self, user_id):
        try:
            self.sql.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        except Exception as e:
            print(e, "user_id")
        return self.db.commit()


    def get_users(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users`")
        except Exception as s:
            print(type(s))
        return result.fetchall()


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






    def set_privacy(self, user_id, privacy):
        try:
            self.sql.execute("UPDATE `users` SET privacy = ? WHERE user_id = ?", (privacy, user_id))
        except Exception as e:
            print(e, "privacy")
        return self.db.commit()


    def get_users_sub_time(self):
        try:
            result = self.sql.execute("SELECT `sub_time` FROM `users`")
        except Exception as s:
            print(type(s))
        return result.fetchall()

    def get_users_privacy(self):
        try:
            result = self.sql.execute("SELECT `privacy` FROM `users`")
        except Exception as s:
            print(type(s))
        return result.fetchall()


    def set_sub_time(self, user_id, sub_time):
        try:
            self.sql.execute("UPDATE `users` SET sub_time = ? WHERE user_id = ?", (sub_time, user_id,))
        except Exception as e:
            print(e, "sub_time")
        return self.db.commit()
