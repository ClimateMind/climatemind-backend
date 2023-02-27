import pandas as pd
import os

from app.common.db_utils import create_sqlalchemy_engine

PATH = os.path.dirname(os.path.realpath(__file__))
# Change file variable when an updated CSV needs to be used.

file = f"{PATH}/lkp_postal_nodes.csv"

# Create a connection to the database.
engine = create_sqlalchemy_engine(echo=True, fast_executemany=True)

# Create a new table (with data) based on the CSV file whenever the docker container is rebuilt.


def add_lrf_data(engine_override=None):
    try:
        data = pd.read_csv(file, index_col=0)
        data.to_sql(
            "lrf_data",
            engine_override or engine,
            if_exists="replace",
            method="multi",
            chunksize=256,
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    add_lrf_data()
