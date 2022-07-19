import sqlite3


class WebScraperDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()

    def close(self):
        self.db.close()

    def user_exists(self, user_id):
        try:
            result = self.sql.execute("SELECT `id` FROM `web_scraper` WHERE `user_id` = ?",(user_id,))
            return bool(len(result.fetchall()))
        except Exception as s:
            print(s, "user_exists")

    def add_user(self, user_id):
        try:
            self.sql.execute("INSERT INTO `web_scraper` (`user_id`) VALUES (?)", (user_id,))
        except Exception as e:
            print(e, "user_id")
        return self.db.commit()

    def get_users(self):
        try:
            result = self.sql.execute("SELECT `user_id` FROM `web_scraper`")
            return result.fetchall()
        except Exception as s:
            print(type(s))

    def delete_user(self, user_id):
        try:
            self.sql.execute("DELETE FROM web_scraper WHERE user_id = ?", (user_id,))
        except Exception as e:
            print(e)
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

    def set_web_scraper_id(self, user_id, web_scraper_id):
        try:
            self.sql.execute("UPDATE `web_scraper` SET scraper_id = ? WHERE user_id = ?", (web_scraper_id, user_id,))
        except Exception as e:
            print(e, "web_scraper_id")
        return self.db.commit()

    def get_web_scraper_id(self, user_id):
        try:
            result = self.sql.execute("SELECT `web_scraper_id` FROM `web_scraper` WHERE `user_id` = ?", (user_id,))
            return result.fetchall()[0][0]
        except Exception as s:
            print(type(s))
