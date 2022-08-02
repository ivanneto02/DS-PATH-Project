import src.UMLSConnector as connector
from .single_string_query import single_string_query
from .second_step import run_second_step
from .first_step import run_first_step
from config import *
import pandas as pd

def map_to_umls():
    print("> Reading data")
    df = pd.read_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_IN_FILE, nrows=None)
    print(f"     length: {len(df)}")

    df["name"] = df["name"].str.strip()

    print("> Establishing MySql connection")
    connection = connector.connect(
        host = MYSQL_HOST,
        database = MYSQL_DATABASE,
        user = MYSQL_USERNAME,
        password = MYSQL_PASSWORD)

    print("> STEP 1: Using MySQL keyword \"LIKE\" keyword")
    df = run_first_step(df, connection)
    if not os.path.exists(BARE_TABLE_SAVE_PATH):
        os.makedirs(BARE_TABLE_SAVE_PATH)
    df.to_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_OUT_FILE_STEP_1, index=False)

    print("> STEP 2: Using more complicated algorithm with MySQL keyword \"LIKE\" keyword")
    df = run_second_step(df, connection)
    if not os.path.exists(BARE_TABLE_SAVE_PATH):
        os.makedirs(BARE_TABLE_SAVE_PATH)
    df.to_csv(BARE_TABLE_SAVE_PATH + "/" + BARE_TABLE_OUT_FILE_STEP_2, index=False)
    print("> Done.")