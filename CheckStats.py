import price_lib as pl
import pandas as pd

file_name = 'nissan.xlsx'

def get_freq_from_db_stats(spares_df):
    i = 0
    freq_array = list()
    connection = pl.create__db_connection("sa-db.svautoz.ru", "root", "88sVQJXySW#", "svautoz")
    for part in spares_df.MPN:
        query = "SELECT COUNT(*) FROM SearchStat WHERE art='" + str(part) + "'"
        freq_array.append(pl.execute_read_query(connection, query)[0][0])
        i += 1
        print(i)
    return pd.Series(freq_array)


spares_df = pl.get_df_from_file(file_name, 0)  
freq = get_freq_from_db_stats(spares_df)
spares_df['freq'] = freq
pl.set_result_sheet_from_df(file_name, spares_df)







