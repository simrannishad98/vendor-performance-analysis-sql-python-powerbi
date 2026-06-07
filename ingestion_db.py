import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')
def ingest_db(df, table_name,engine):
    df.to_sql(table_name, con = engine, if_exists = 'replace', index= False)

def load_raw_data():
    start = time.time()
    for file in os.listdir('.'):
        if '.csv' in file:
            logging.info(f'Ingesting {file} in db')
            table_name = file[:-4]
            first_chunk = True
            total_rows = 0
            num_cols = 0
            
            for chunk in pd.read_csv(file, chunksize=100000):
                if first_chunk:
                    chunk.to_sql(table_name, con=engine, if_exists='replace', index=False)
                    num_cols = chunk.shape[1]
                    first_chunk = False
                else:
                    chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
                total_rows += len(chunk)
                
            print((total_rows, num_cols))
            
    end = time.time()
    total_time = (end - start)/60
    logging.info('----------------------Ingestion Complete----------------------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__ == '__main__':
    os.makedirs("logs", exist_ok=True)
    load_raw_data()