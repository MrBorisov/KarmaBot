import sqlite3


def insert_user_into_users(user_name, tg_user_id):
    # добавляем нового пользователся в таблицу users, попутно проверяя нет ли уже его там
    if select_userid_from_users(tg_user_id)==0:
        try:
            sqlite_connection = sqlite3.connect('users.db')
            cursor = sqlite_connection.cursor()
            # Подключен к SQLite

            sqlite_insert_with_param = """INSERT INTO users
                                  (tg_user_id, tg_user_name)
                                  VALUES (?, ?);"""
            data_tuple = (tg_user_id, user_name)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqlite_connection.commit()
            # Переменные Python успешно вставлены в таблицу users
            cursor.close()
        except sqlite3.Error as error:
            return 2 #при ошибке возвращаем 2
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                # Соединение с SQLite закрыто
        return 1 # возвращаем 1 если добавили пользователя успешно
    else:
        return 0 # возвращаем 0 если пользователь уже существует


def select_userid_from_users(tg_user_id):
    # находим id user в таблице юзер, можно было написать запрос с join, но мне лень. пока так...
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()

        cursor.execute('SELECT num_user from users WHERE tg_user_id LIKE ?', ['%' + tg_user_id + '%'])
        records = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            # Соединение с SQLite закрыто
    if records != None:
        return records[0]
    else:
        return 0

def add_user_reward(tg_user_id, count_kpi_user, kpi_date):
    #Добавляем запись с вознаграждением в таблицу top_kpi, kpi_date в формате YYYY-MM-DD HH:MM:SS
    num_user = select_userid_from_users(tg_user_id) #получим id пользователя из таблицы users
    #Добавим запись в таблицу top_kpi
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        # Подключен к SQLite

        sqlite_insert_with_param = """INSERT INTO top_kpi
                              (num_user, count_kpi_user, kpi_date)
                              VALUES (?, ?, ?);"""
        data_tuple = (num_user, count_kpi_user, kpi_date)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        # Переменные Python успешно вставлены в таблицу users
        cursor.close()
    except sqlite3.Error as error:
        return 0
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            # Соединение с SQLite закрыто
    return 1  # возвращаем 1 если добавили награду успешно

def select_top_kpi(tg_user_id):# надо протестировать
    # найдем все строки в таблице top_kpi чтобы показать рейтинг пользователя
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        cursor.execute('SELECT sum(tk.count_kpi_user)  FROM users JOIN top_kpi tk on users.num_user = tk.num_user WHERE tg_user_id LIKE ?', ['%' + tg_user_id + '%'])
        records = cursor.fetchone()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            # Соединение с SQLite закрыто
    if records != None:
        return records[0]
    else:
        return 0
def is_user_admin(tg_user_id):
    # получим значение is_admin пользователя с tg_user_id
    try:
        sqlite_connection = sqlite3.connect('users.db')
        cursor = sqlite_connection.cursor()
        cursor.execute('SELECT is_adm from users WHERE tg_user_id LIKE ?', ['%' + tg_user_id + '%'])
        records = cursor.fetchone()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            # Соединение с SQLite закрыто
    if records != None:
        return records[0]
    else:
        return 0

