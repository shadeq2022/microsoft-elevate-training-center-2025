# ETL Pipeline - Fashion Studio

A simple ETL pipeline that scrapes fashion product data, transforms it, and saves it to CSV, Google Sheets, and PostgreSQL.

## Requirements

- Python 3.12+
- PostgreSQL
- Google Cloud Account

## Setup

```bash
# Clone and enter the project
git clone https://github.com/shadeq2022/microsoft-elevate-training-center-2025.git
cd microsoft-elevate-training-center-2025/proyek-akhir-membangun-etl-pipeline-sederhana

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root folder:
```
DB_PASSWORD=your_postgresql_password
```

Place your `google-sheets-api.json` in the root folder, then update `main.py`:
```python
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
```

## Run

```bash
python main.py
```

## Test

```bash
python -m pytest tests/ -v
```

## Output

- **867 rows** saved to `products.csv`, Google Sheets, and PostgreSQL (`fashion_db`)
