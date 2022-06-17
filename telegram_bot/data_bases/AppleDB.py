import sqlite3


class AppleDB:
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

    def set_privacy(self, user_id, privacy):
        try:
            self.sql.execute("UPDATE `users` SET privacy = ? WHERE user_id = ?", (privacy, user_id))
        except Exception as e:
            print(e, "privacy")
        return self.db.commit()

    def set_parse_status(self, user_id, parse_status):
        try:
            self.sql.execute("UPDATE `users` SET parse_status = ? WHERE user_id = ?", (parse_status, user_id,))
        except Exception as e:
            print(e, "parse_status")
        return self.db.commit()

    def get_parse_status(self, user_id):
        try:
            result = self.sql.execute("SELECT `parse_status` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def set_search_area(self, user_id, search_area):
        try:
            self.sql.execute("UPDATE `users` SET search_area = ? WHERE user_id = ?", (search_area, user_id,))
        except Exception as e:
            print(e, "search_area")
        return self.db.commit()

    def get_search_area(self, user_id):
        try:
            result = self.sql.execute("SELECT `search_area` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def set_category(self, user_id, category):
        try:
            self.sql.execute("UPDATE `users` SET category = ? WHERE user_id = ?", (category, user_id,))
        except Exception as e:
            print(e, "category")
        return self.db.commit()

    def get_category(self, user_id):
        try:
            result = self.sql.execute("SELECT `category` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]


    def set_page_url(self, user_id, page_url):
        try:
            self.sql.execute("UPDATE `users` SET page_url = ? WHERE user_id = ?", (page_url, user_id,))
        except Exception as e:
            print(e, "page_url")
        return self.db.commit()

    def get_page_url(self, user_id):
        try:
            result = self.sql.execute("SELECT `page_url` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]


    def no_type(self, user_id):
        try:
            result = self.sql.execute("SELECT type FROM users WHERE user_id = ?",(user_id,))
        except Exception as s:
            print(s, "type_exists")

        return result.fetchall()[0][0] is None

    def no_city(self, user_id):
        try:
            result = self.sql.execute("SELECT city FROM users WHERE user_id = ?",(user_id,))
        except Exception as s:
            print(s, "city_exists")

        return result.fetchall()[0][0] is None


    def no_nickname(self, user_id):
        try:
            result = self.sql.execute("SELECT nickname FROM users WHERE user_id = ?",(user_id,))
        except Exception as s:
            print(s, "nickname_exists")

        return result.fetchall()[0][0] is None

    def get_users(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `users`")
        except Exception as s:
            print(type(s))
        return result.fetchall()

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

    def get_city(self, user_id):
        try:
            result = self.sql.execute("SELECT `city` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_type(self, user_id):
        try:
            result = self.sql.execute("SELECT `type` FROM `users` WHERE `user_id` = ?",(user_id,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

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

    def delete_all(self):
        user_list = self.get_users()
        print(user_list)
        try:
            for i in user_list:
                self.delete_user(i[0])
        except Exception as e:
            print(e)
        return self.db.commit()

    def set_sub_time(self, user_id, sub_time):
        try:
            self.sql.execute("UPDATE `users` SET sub_time = ? WHERE user_id = ?", (sub_time, user_id,))
        except Exception as e:
            print(e, "sub_time")
        return self.db.commit()

    def set_nickname(self, user_id, nickname):
        try:
            self.sql.execute("UPDATE `users` SET nickname = ? WHERE user_id = ?", (nickname, user_id))
        except Exception as e:
            print(e, "nickname")
        return self.db.commit()

    def set_city(self, user_id, city):
        try:
            self.sql.execute("UPDATE `users` SET city = ? WHERE user_id = ?", (city, user_id))
        except Exception as e:
            print(e, "city")
        return self.db.commit()

    def set_type(self, user_id, type):
        try:
            self.sql.execute("UPDATE `users` SET type = ? WHERE user_id = ?", (type, user_id))
        except Exception as e:
            print(e, "type")
        return self.db.commit()


class AppleCategoryDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def get_cat1(self, main_category):
        try:
            result = self.sql.execute("SELECT `cat1` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_cat2(self, main_category):
        try:
            result = self.sql.execute("SELECT `cat2` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_cat3(self, main_category):
        try:
            result = self.sql.execute("SELECT `cat3` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_cat4(self, main_category):
        try:
            result = self.sql.execute("SELECT `cat4` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_cat5(self, main_category):
        try:
            result = self.sql.execute("SELECT `cat5` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_cat6(self, main_category):
        try:
            result = self.sql.execute("SELECT `cat6` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]




    def get_link_cat1(self, main_category):
        try:
            result = self.sql.execute("SELECT `link_cat1` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]


    def get_link_cat2(self, main_category):
        try:
            result = self.sql.execute("SELECT `link_cat2` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_link_cat3(self, main_category):
        try:
            result = self.sql.execute("SELECT `link_cat3` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_link_cat4(self, main_category):
        try:
            result = self.sql.execute("SELECT `link_cat4` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_link_cat5(self, main_category):
        try:
            result = self.sql.execute("SELECT `link_cat5` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]

    def get_link_cat6(self, main_category):
        try:
            result = self.sql.execute("SELECT `link_cat6` FROM `categories` WHERE `main_category` = ?",(main_category,))
        except Exception as s:
            print(type(s))
        return result.fetchall()[0][0]
