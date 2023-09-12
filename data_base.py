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
    def sql_read_workers_1():
        return "SELECT w.second_name, w.first_name, w.last_name, r.role, g.gild, w.id FROM workers w \
                JOIN roles r ON w.role = r.id  \
                JOIN gilds g ON w.gild = g.id  \
                ORDER BY w.second_name, w.first_name, w.last_name"

    @staticmethod
    def sql_read_workers_2():
        return "SELECT id, second_name, first_name, last_name, role, gild FROM workers \
                ORDER BY second_name, first_name, last_name"

    @staticmethod
    def sql_add_worker():
        return "INSERT INTO workers (second_name, first_name, last_name, role, gild) values (%s,%s,%s,%s,%s) RETURNING id"

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
        return "SELECT id, gild, role FROM gilds ORDER BY id"

    @staticmethod
    def sql_read_date_report():
        return "SELECT id, date, day_of_week FROM date_report \
                WHERE extract(year from date::timestamp) = %s \
                AND extract(month from date::timestamp) = %s \
               ORDER BY date"

    @staticmethod
    def sql_insert_date_report():
        return "INSERT INTO date_report (date, day_of_week) values (%s, %s)"

    @staticmethod
    def sql_insert_workers_report():
        return "INSERT INTO workers_report (day_id, worker_id, work_hour, rating, status, place, time_of_day, description, team) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    @staticmethod
    def sql_read_workers_report(filter_worker_role, date_year, date_month, filter_worker_gild):
        return "SELECT w.second_name, w.first_name, w.last_name, dr.date, wr.work_hour, wr.rating, wr.status, \
                        wr.worker_id, wr.day_id, w.gild, wr.place, wr.time_of_day, wr.description, w.role \
                FROM workers_report wr \
                join workers w on w.id = wr.worker_id \
                join date_report dr on dr.id = wr.day_id \
                join roles rs on w.role = rs.id \
                join gilds gd on w.gild = gd.id \
                where rs.role = " + filter_worker_role + "\
                and gd.gild = " + filter_worker_gild + "\
                and extract(year from dr.date::timestamp) = " + date_year + "\
                and extract(month from dr.date::timestamp) = " + date_month + "\
                ORDER BY w.second_name, w.first_name, w.last_name, dr.date"

    @staticmethod
    def sql_edit_table():
        return "UPDATE workers_report SET (work_hour, rating, status, place, time_of_day, description) = (%s,%s,%s,%s,%s,%s) \
                WHERE worker_id = %s AND day_id = %s \
                RETURNING day_id, worker_id"

    @staticmethod
    def sql_list_all_date():
        return "SELECT DISTINCT DATE_PART('year', date)::int AS years, DATE_PART('month', date)::int AS month, TO_CHAR(date, 'TMMonth') as month_name\
                FROM date_report dr \
                ORDER BY years, month"