from psycopg2 import connect


class DataBase:
    login = ''
    password = ''
    requests = dict()

    @staticmethod
    def init_connection(login, password):
        connection = {
            "host": "10.10.10.93",
            "dbname": "CollectiveDB",
            "user": login,
            "password": password,
            "port": "5432"
        }
        return connection


def select_requests():
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM requests")
                for row in cursor.fetchall():
                    DataBase.requests[row[0]] = row[1]
                pass
    except:
        pass


def select_workers():
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['select_workers'])
                workers = cursor.fetchall()
                return workers
    except:
        pass


def insert_worker(s_name, f_name, l_name, role, guild, t_num):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['insert_worker'], (s_name, f_name, l_name, role, guild, role, t_num,))
                return cursor.fetchone()
    except:
        pass


def update_worker(s_name, f_name, l_name, role, guild, t_num, w_id):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['update_worker'],
                               (s_name, f_name, l_name, role, guild, role, t_num, w_id,))
    except:
        pass


def delete_worker(ids):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['delete_worker'], (ids,))
    except:
        pass


def select_roles():
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['select_roles'])
                tuple_role = cursor.fetchall()
                list_role = [role[1] for role in tuple_role]
            return tuple_role, list_role
    except:
        pass


def select_teams():
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['select_teams'])
                list_teams_tmp = cursor.fetchall()
                list_teams = [str(team[1]) + ': ' + team[2] for team in list_teams_tmp]
                list_teams[0] = 'бригада'
                return list_teams
    except:
        pass


def select_guilds(tuple_role):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['select_guilds'])
                list_guild = cursor.fetchall()
                dict_guilds = dict()
                for role in tuple_role:
                    dict_guilds[role[1]] = []
                    for guild in list_guild:
                        if role[0] == guild[2]:
                            dict_guilds[role[1]].append(guild[1])
                return list_guild, dict_guilds
    except:
        pass


def select_date(year, month):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['select_cur_dates'], (year, month,))
                return tuple(cursor.fetchall())
    except:
        pass


def insert_report(id_date, id_worker):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['insert_report'], (id_date, id_worker,))
    except:
        pass


def select_reports(role, guild, year, month):
    with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(DataBase.requests['select_reports'], (role, guild, year, month,))
            reports = cursor.fetchall()
            id_report = 0
            new_reports_dict = dict()
            for report in reports:
                if id_report != report[7]:
                    new_reports_dict[report[7]] = dict()
                    id_report = report[7]
                new_reports_dict[report[7]][report[8]] = {'role': report[13], 'hour': report[4],
                                                          'rating': report[5], 'status': report[6],
                                                          'place': report[10], 'time_of_day': report[11],
                                                          'description': report[12], 'team': report[14],
                                                          'brigadier': report[15], 'guild': report[9],
                                                          'props_type': report[16]}
            return new_reports_dict, reports


def update_report(hour, rating, status, place, time_of_day, description, team, id_worker, id_date):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['update_report'],
                               (hour, rating, status, place, time_of_day, description, team, id_worker, id_date))
    except:
        pass


def select_all_date():
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                all_date_dict = dict()
                cursor.execute(DataBase.requests['select_all_date'])
                all_date_list = cursor.fetchall()
                year = 0
                for date in all_date_list:
                    if year != date[0]:
                        all_date_dict[str(date[0])] = dict()
                        year = date[0]
                    all_date_dict[str(date[0])][str(date[1])] = str(date[2]).lower()
                return all_date_dict
    except:
        pass


def select_text_permit(type_permit):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                dict_text = dict()
                cursor.execute(DataBase.requests['select_text_permit'], (type_permit,))
                text_list = cursor.fetchall()
                group = 0
                for text in text_list:
                    if group != text[0]:
                        dict_text[str(text[0])] = dict()
                        group = text[0]
                    dict_text[str(text[0])][str(text[1])] = str(text[2])
                return dict_text
    except:
        pass


def select_settings(setting):
    try:
        with connect(**DataBase.init_connection(DataBase.login, DataBase.password)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(DataBase.requests['select_settings'], (setting,))
                value = cursor.fetchall()
                return value
    except:
        pass
