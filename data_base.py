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
        return "SELECT w.second_name, w.first_name, w.last_name, r.role, g.gild, w.id FROM workers w \
                JOIN roles r ON w.role = r.id  \
                JOIN gilds g ON w.gild = g.id  \
                ORDER BY second_name"

    @staticmethod
    def sql_add_worker():
        return "INSERT INTO workers (second_name, first_name, last_name, role, gild) values (%s,%s,%s,%s,%s)"

    @staticmethod
    def sql_edit_worker():
        return "UPDATE workers SET (second_name, first_name, last_name, role, gild) = (%s,%s,%s,%s,%s) WHERE id = %s"

    @staticmethod
    def sql_del_worker():
        return "DELETE FROM workers WHERE id=%s"

    @staticmethod
    def sql_list_role():
        return "SELECT id, role FROM roles ORDER BY id"

    @staticmethod
    def sql_list_gild():
        return "SELECT id, gild FROM gilds ORDER BY id"