import pandas as pd
from sqlalchemy import create_engine
from env import reporting_engine_mysql_dev, reporting_engine_mysql_prod, DEV_MODE

print(f'{DEV_MODE=}')

host_dct = reporting_engine_mysql_dev if DEV_MODE else reporting_engine_mysql_prod
host = host_dct['host']
port = host_dct['port']
user = host_dct['user']
password = host_dct['password']
db = host_dct['db']

engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, db))


def get_df_from_table(table):
    try:
        with engine.connect() as connection:
            df = pd.read_sql_table(table, con=connection)

        return df
    except Exception as e:
        raise ValueError(e)


def get_df_from_query(query):
    try:
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        raise ValueError(e) from e