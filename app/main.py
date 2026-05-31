from fastapi import FastAPI, File, HTTPException, UploadFile

from app.services import process_sales_csv

app = FastAPI(
    title="CSV Report Processing API",
    description="API for uploading sales CSV files and generating structured business reports.",
    version="1.0.0",
)

@app.get("/health")
def health_check() -> dict:
    """Check if the API is running."""
    return {"status": "ok"}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)) -> dict:
    """Upload a CSV file and return generated sales reports."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a CSV file.",
        )
    
    try:
        file_content = await file.read()
        reports = process_sales_csv(file_content)

        return {
            "status": "success",
            "filename": file.filename,
            **reports,
        }
    
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while processing file: {str(error)}",
        )