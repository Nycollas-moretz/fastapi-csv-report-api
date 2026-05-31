from io import StringIO
import pandas as pd


REQUIRED_COLUMNS = {
    "order_id",
    "date",
    "customer",
    "category",
    "product",
    "quantity",
    "unit_price",
    "payment_status",
}


def validate_required_columns(df: pd.DataFrame) -> None:
    """Validate if the CSV has all required columns."""
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")


def read_csv_content(file_content: bytes) -> pd.DataFrame:
    """Read uploaded CSV content and convert it into a pandas DataFrame."""
    decoded_content = file_content.decode("utf-8")
    csv_buffer = StringIO(decoded_content)

    return pd.read_csv(csv_buffer)


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize sales data."""
    validate_required_columns(df)

    cleaned = df.copy()

    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce").fillna(0.0)
    cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce").fillna(0.0)

    cleaned["payment_status"] = cleaned["payment_status"].astype(str).str.strip().str.lower()
    cleaned["category"] = cleaned["category"].astype(str).str.strip()
    cleaned["product"] = cleaned["product"].astype(str).str.strip()
    cleaned["customer"] = cleaned["customer"].astype(str).str.strip()

    cleaned = cleaned.dropna(subset=["date"])

    cleaned["total_amount"] = cleaned["quantity"] * cleaned["unit_price"]
    cleaned["month"] = cleaned["date"].dt.to_period("M").astype(str)

    return cleaned


def build_reports(df: pd.DataFrame) -> dict:
    """Build report data and return it as a dictionary."""
    paid_sales = df[df["payment_status"] == "paid"].copy()

    total_revenue = float(paid_sales["total_amount"].sum())
    total_paid_orders = int(paid_sales["order_id"].count())
    total_items_sold = float(paid_sales["quantity"].sum())

    monthly_sales = (
        paid_sales
        .groupby("month", as_index=False)
        .agg(
            total_revenue=("total_amount", "sum"),
            total_orders=("order_id", "count"),
            total_items_sold=("quantity", "sum"),
        )
        .sort_values("month")
    )

    category_summary = (
        paid_sales
        .groupby("category", as_index=False)
        .agg(
            total_revenue=("total_amount", "sum"),
            total_orders=("order_id", "count"),
            total_items_sold=("quantity", "sum"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    customer_summary = (
        paid_sales
        .groupby("customer", as_index=False)
        .agg(
            total_spent=("total_amount", "sum"),
            total_orders=("order_id", "count"),
        )
        .sort_values("total_spent", ascending=False)
    )

    return {
        "summary": {
            "total_revenue": total_revenue,
            "total_paid_orders": total_paid_orders,
            "total_items_sold": total_items_sold,
        },
        "monthly_sales": monthly_sales.to_dict(orient="records"),
        "category_summary": category_summary.to_dict(orient="records"),
        "customer_summary": customer_summary.to_dict(orient="records"),
    }


def process_sales_csv(file_content: bytes) -> dict:
    """Process uploaded CSV content and return report data."""
    raw_df = read_csv_content(file_content)
    cleaned_df = clean_sales_data(raw_df)
    reports = build_reports(cleaned_df)

    return reports