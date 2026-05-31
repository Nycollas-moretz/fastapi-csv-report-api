# FastAPI CSV Report API

A practical FastAPI backend that receives a sales CSV file, processes the data, and returns structured business reports in JSON format.

This project is a backend/API version of a CSV report automation workflow. Instead of running a local script, the user can upload a CSV file through an API endpoint and receive processed summaries.

## What This Project Does

The API:

- Receives a CSV file upload
- Validates required columns
- Cleans and standardizes sales data
- Calculates total order amount
- Filters paid transactions
- Generates monthly sales summaries
- Generates category summaries
- Generates customer spending summaries
- Returns the results as JSON

## Business Problem

Many teams still process CSV reports manually. This API demonstrates how a repetitive spreadsheet workflow can be transformed into a reusable backend service.

A similar solution could be adapted for sales reports, inventory files, customer data, operational logs, or internal business workflows.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- python-multipart

## Project Structure

```text
fastapi-csv-report-api/
│
├── app/
│   ├── main.py
│   └── services.py
│
├── data/
│   └── sample_sales.csv
│
├── README.md
├── requirements.txt
└── .gitignore