import mysql.connector
from mysql.connector import Error
import pandas as pd


def create__db_connection(host_name, user_name, user_password, database_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def get_df_from_file(file_name, sheet):
    xl = pd.ExcelFile(file_name)
    spares_df = xl.parse(xl.sheet_names[sheet])
    xl.close()
    return spares_df


def set_result_sheet_from_df(file_name, spares_df):
    with pd.ExcelWriter(file_name, mode='a', if_sheet_exists='new') as writer:  
        spares_df.to_excel(writer, sheet_name='Result')