import sqlite3
import hashlib

from defines import *
from logm import LogManager
from objects import *


class DataBaseManager:
    @staticmethod
    def md5(string: str):
        return hashlib.md5(string.encode("utf-8")).hexdigest()

    @staticmethod
    def strd_from_str(date: str):
        date = date.split("-")
        return str(int(date[2])) + " " + DATE_DICT[str(int(date[1]))] + " " + str(int(date[0]))

    def __init__(self):
        self.sql = sqlite3.connect("base.db")
        self.conn = self.sql.cursor()
        self.log = LogManager()

    def _non_query(self, cmd: str, commit=False):
        self.conn.execute(cmd)
        if commit:
            self.sql.commit()

    def _query(self, cmd: str):
        return self.conn.execute(cmd)

    def close(self):
        self.conn.close()
        self.sql.close()
        self.log.close()

    def create_all_tables(self):
        try:
            sql1 = """CREATE TABLE IF NOT EXISTS `head_data`(
            `setting` TEXT NOT NULL PRIMARY KEY,
            `value` TEXT NOT NULL)"""

            sql2 = """CREATE TABLE IF NOT EXISTS `debtors`(
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `name` TEXT NOT NULL,
            `priority` INTEGER NOT NULL DEFAULT 0 
            )"""

            sql3 = """CREATE TABLE IF NOT EXISTS `debts`(
            `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `debtor` TEXT NOT NULL,
            `amount` INTEGER NOT NULL DEFAULT 100,
            `desc` TEXT,
            `priority` INTEGER NOT NULL DEFAULT 0,
            `date` TEXT NOT NULL
            )"""

            sql4 = """CREATE TABLE IF NOT EXISTS `priorities`(
            `id` INTEGER NOT NULL PRIMARY KEY,
            `name` TEXT NOT NULL,
            `color` TEXT NOT NULL DEFAULT '#ffffff')"""

            self._non_query(sql1)
            self._non_query(sql2)
            self._non_query(sql3)
            self._non_query(sql4)
            self.sql.commit()
        except Exception as ex:
            print("ERROR. Write to log...")
            self.log.append(LOG_ERROR, "Fatal error when adding tables. " + str(ex))

    def set_auth_data(self, login: str, password: str):
        try:
            password = str(self.md5(password))
            self._non_query("DELETE FROM `head_data`", True)

            sql = "INSERT INTO `head_data` VALUES ('login','{0}'), ('pw','{1}')"
            self._non_query(sql.format(login.replace("'", "\\'"),
                                       password.replace("'", "\\'")), True)
        except Exception as ex:
            self.log.append(LOG_ERROR, "Fatal error on set_auth_data. " + str(ex))

    def auth(self, login: str, password: str):
        try:
            data = self._query("SELECT `value` FROM `head_data`").fetchall()
            v_login, v_pw = data[0][0], data[1][0]
            password = self.md5(password)
            return v_login == login and v_pw == password
        except Exception as ex:
            self.log.append(LOG_ERROR, "Fatal error on auth. " + str(ex))
            return False

    def create_priories(self):
        sql = """INSERT INTO `priorities`(`id`, `name`, `color`) VALUES
        (0, 'Обычный', '#FFFFFF'),
        (1, 'Низкий', '#9ACD32'),
        (2, 'Средний', '#FFA500'),
        (3, 'Высокий', '#F08080')
        """
        self._non_query(sql, True)

    def add_debtor(self, name: str, priority: int):
        sql = "INSERT INTO `debtors` (`name`, `priority`) VALUES ('{0}', '{1}')"
        self._non_query(sql.format(name.replace("'", "\\'"),
                                   str(priority)), True)

    def add_debt(self, debtor: str, amount: int, desc: str, priority: int, date=None):
        debtor = debtor.replace("'", "\\'")
        desc = desc.replace("'", "\\'")
        if date is None:
            date = "date('now')"
        else:
            date = "'" + date + "'"
        sql = """INSERT INTO `debts` (`debtor`, `amount`, `desc`,`priority`,`date`)
        VALUES ('{0}', '{1}', '{2}', '{3}', {4})"""
        self._non_query(sql.format(debtor, str(amount), desc, str(priority), date), True)

    def get_priorities(self, ident=-1):
        if ident != -1:
            sql = "SELECT * FROM `priorities` WHERE `id`='" + str(ident) + "'"
            data = self._query(sql).fetchone()
            id, name, color = data
            return Priority(int(id), name, color)
        else:
            sql = "SELECT * FROM `priorities`"
            data = self._query(sql).fetchall()
            li = []
            for d in data:
                id, name, color = d
                li.append(Priority(int(id), name, color))
            return li

    def get_debtors(self, name=None):
        if name is not None:
            sql = "SELECT * FROM `debtors` WHERE `name`='" + name + "'"
            data = self._query(sql).fetchone()
            id, nm, priority = data
            return Debtor(int(id), name, int(priority))
        else:
            sql = "SELECT * FROM `debtors`"
            data = self._query(sql).fetchall()
            li = []
            for d in data:
                id, nm, priority = d
                li.append(Debtor(int(id), nm, int(priority)))
            return li

    def get_debts(self, id=None, sorting=0):
        if id is not None:
            sql = "SELECT * FROM `debts` WHERE `id`='" + str(id) + "'"
            data = self._query(sql).fetchone()
            id, dbt, amount, desc, priority, date = data
            return Debt(int(id), dbt, int(amount), desc, int(priority), date)
        else:
            order = ""
            if sorting == DEBT_SORT_DEFAULT:
                order = "`id` DESC"
            if sorting == DEBT_SORT_AMOUNT:
                order = "`amount` DESC"
            if sorting == DEBT_SORT_DATE:
                order = "`date` DESC"
            if sorting == DEBT_SORT_DEBTOR:
                order = "`debtor` ASC"

            sql = "SELECT * FROM `debts` ORDER BY " + order
            data = self._query(sql).fetchall()
            li = []
            for d in data:
                id, dbt, amount, desc, priority, date = d
                li.append(Debt(int(id), dbt, int(amount), desc, int(priority), date))
            return li

    def get_debts_by_debtor(self, debtor: str, sorting=0):
        order = ""
        if sorting == DEBT_SORT_DEFAULT:
            order = "`id` DESC"
        if sorting == DEBT_SORT_AMOUNT:
            order = "`amount` DESC"
        if sorting == DEBT_SORT_DATE:
            order = "`date` DESC"
        if sorting == DEBT_SORT_DEBTOR:
            order = "`debtor` ASC"

        sql = "SELECT * FROM `debts` WHERE `debtor`='" + debtor + "' ORDER BY " + order
        data = self._query(sql).fetchall()
        li = []
        for d in data:
            id, dbt, amount, desc, priority, date = d
            li.append(Debt(int(id), dbt, int(amount), desc, int(priority), date))
        return li

    def get_debtors_count(self):
        sql = "SELECT COUNT(*) FROM `debtors`"
        data = self._query(sql).fetchone()
        return int(data[0])

    def delete_debt(self, id):
        sql = "DELETE FROM `debts` WHERE `id`='" + str(id) + "'"
        self._non_query(sql, True)
