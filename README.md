# DE Test

## Overview

This repository contains a **FastAPI-based application** designed to **load CSV data into Google BigQuery**. The application is containerized using **Docker** and deployed on **Google Cloud Run**. Additionally, it includes SQL scripts for database setup and testing, as well as Jupyter Notebooks for experimentation and analysis.

## Project Structure

```bash

├── scripts/
│   ├── bd_script/
│   │   ├── init.sql        # SQL script for table creation
│   │   ├── SQL_TEST.sql    # SQL script for test queries
│
├── data_ingestion/
│   ├── main.py            # FastAPI application for CSV ingestion
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Docker configuration for deployment
│
├── notebooks/
    data_ingestion/
│   ├── data_ingestion.ipynb  # Jupyter notebooks for experimentation
```

## API Endpoint - CSV Data Loader

The application exposes an API endpoint to **load CSV data from Google Cloud Storage (GCS) into BigQuery**.

### **POST /loadcsv/**

- **Description**: Loads a CSV file from a specified GCS location into a BigQuery table.
- **Request Body (JSON)**:
  ```json
  {
      "gcs_location": "gs://datalake_gb/zone=landing/data=employees/hired_employees.csv",
      "schema_fields": ["id", "name", "dt", "department_id", "job_id"],
      "batch_size": 1000
  }
  ```

  ```

### **Testing the API Locally**

You can test the API locally using **cURL**:

```bash
curl -X 'POST' 'http://127.0.0.1:8000/loadcsv/' \
     -H 'Content-Type: application/json' \
     -d '{"gcs_location": "gs://datalake_gb/zone=landing/data=employees/hired_employees.csv", "schema_fields": ["id","name","dt","department_id","job_id"],"batch_size": 1000}'
```

## Deployment to Google Cloud Run

The FastAPI application is deployed on **Google Cloud Run** using a **Docker container**.

### **1. Build the Docker Image**

```bash
docker build -t gcr.io/sample_project/csvingestion:0.1 .
```

### **2. Push the Image to Google Container Registry**

```bash
docker push gcr.io/sample_project/csvingestion:0.1 
```


```

## Development & Experimentation

For local experimentation, the **notebooks/** directory contains Jupyter notebooks for coding test

## Requirements

Ensure you have the following dependencies installed:

- Python 3.10
- FastAPI
- Uvicorn
- Pandas
- Google Cloud BigQuery SDK
- Docker
- Google Cloud SDK