class DataBase:
    @staticmethod
    def config():
        return {
            "host": "localhost",
            "dbname": "CollectiveDB",
            "user": "collective_engineer",
            "password": "coll",
            "port": "5432"
        }

    @staticmethod
    def sql_read_workers():
        return "SELECT second_name, first_name, last_name, role, gild, id FROM workers ORDER BY first_name"

    @staticmethod
    def sql_add_worker():
        return "INSERT INTO workers (second_name, first_name, last_name, role, gild) values (%s,%s,%s,%s,%s)"

    @staticmethod
    def sql_edit_worker():
        return "UPDATE workers SET (second_name, first_name, last_name, role, gild) = (%s,%s,%s,%s,%s) WHERE id = %s)"




    @staticmethod
    def sql_del_worker():
        return "DELETE FROM workers WHERE id=%s"

    @staticmethod
    def sql_list_role():
        return "SELECT id, role FROM roles ORDER BY id"

    @staticmethod
    def sql_list_gild():
        return "SELECT id, gild FROM gilds ORDER BY id"