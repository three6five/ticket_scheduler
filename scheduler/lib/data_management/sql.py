import pandas as pd
from sqlalchemy import create_engine
from env import re_sql_user, re_sql_pass, re_sql_port, re_sql_db, re_sql_host

engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(re_sql_user, re_sql_pass, re_sql_host, re_sql_port, re_sql_db))


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