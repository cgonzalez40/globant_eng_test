#!/usr/bin/env python
# coding: utf-8


#import needed libraries
import pandas as pd
from google.cloud import bigquery
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()




# Defining global variables
project_id = "poc-accionclimatica-agrilac"
schema_name =  "training"



class input_schema(BaseModel):
    gcs_location: str
    schema_fields: List[str]
    batch_size : int
    


def load_pandas(url:str,
                chunk_size = 1000,
               schema_fields = []):
    """

    Load a CSV file into a Pandas DataFrame using chunking.

    This function reads a CSV file from the given URL in chunks and 
    allows specifying column names and chunk size.

    Parameters:
    ----------
    url : str
        The URL or file path of the CSV file to be loaded.
    chunk_size : int, optional (default=1000)
        The number of rows per chunk when reading the CSV file.
    schema_fields : list, optional (default=[])
        A list of column names to be used as headers. If empty, 
        the default headers from the file are used.
    """
    return  pd.read_csv(url,
                        chunksize=chunk_size,
                       sep=",",
                       names = schema_fields,
                       header = None
                       )

def bigquery_insert(df:pd.DataFrame, table:str):    
    """
    Inserts a Pandas DataFrame into a specified BigQuery table.

    This function uploads a DataFrame to a BigQuery table using the 
    BigQuery Python client. It assumes that the table schema is already defined.

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be inserted into BigQuery.
    table : str
    The fully qualified name of the target BigQuery table in the format `project.dataset.table`.

    """
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        write_disposition="WRITE_APPEND",
    )
    job = client.load_table_from_dataframe(
        df, table, job_config=job_config
    )
    job.result()

@app.post("/loadcsv/")   
def main( parameters:input_schema ):
    """
    Main function to process data from a GCS (Google Cloud Storage) location 
    and insert it into BigQuery.

    This function:
    1. Reads a CSV file from the specified GCS location using `load_pandas`.
    2. Extracts the table name from the GCS file path.
    3. Formats the BigQuery table reference.
    4. Inserts the data into BigQuery using `bigquery_insert`.
    """
    gcs_location= parameters.gcs_location
    schema_fields = parameters.schema_fields
    chunk_size = parameters.batch_size
    
    if chunk_size >= 0 and chunk_size <= 1000:
        
        data = load_pandas(url=gcs_location,
                       schema_fields = schema_fields,
                           chunk_size=chunk_size )
        for _data in data:
            sample = _data
            _table_name = (gcs_location.split("/")[-2]).split("=")[1]
            formated_table = f"{project_id}.{schema_name}.{_table_name}"
            bigquery_insert(_data,formated_table)
    else:
        raise Exception("The batch size have to be between 1 and 1000")




    

