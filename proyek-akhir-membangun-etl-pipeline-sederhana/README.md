# Building a Simple ETL Pipeline

An ETL Pipeline to extract fashion product data from the Fashion Studio website
(https://fashion-studio.dicoding.dev) using web scraping, transform the data,
and load it into 3 different data repositories.

---

## Requirements

- Python 3.12+
- PostgreSQL
- Google Cloud Account (for Google Sheets API)

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/shadeq2022/microsoft-elevate-training-center-2025.git
cd microsoft-elevate-training-center-2025/proyek-akhir-membangun-etl-pipeline-sederhana
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

| Platform | Shell | Command |
|---|---|---|
| Windows | PowerShell | `venv\Scripts\Activate.ps1` |
| Windows | CMD | `venv\Scripts\activate.bat` |
| Linux/Mac | bash/zsh | `source venv/bin/activate` |

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Google Sheets API Setup

### 1. Create a Project in Google Cloud Console
- Go to https://console.cloud.google.com/
- Click the project dropdown → **"New Project"**
- Project name: anything (e.g. `simple-etl`)
- Click **"Create"**

### 2. Enable Google Sheets API
- In the search bar, type **"Google Sheets API"**
- Click the result → Click **"Enable"**

### 3. Create a Service Account
- In the search bar, type **"Service Accounts"** → click the result
- Click **"+ Create Service Account"**
- Fill in:
  - **Service account name:** `etl-pipeline`
  - **Role:** Editor
- Click **"Continue"** → **"Done"**

### 4. Download JSON Key
- Click the newly created service account
- Open the **"Keys"** tab → **"Add Key"** → **"Create new key"**
- Select **JSON** format → Click **"Create"**
- The JSON file will be downloaded automatically
- **Rename** it to `google-sheets-api.json`
- **Move** it to the root folder of this project

### 5. Create a Google Sheets File
- Go to https://sheets.google.com
- Click **"+ Blank"** → name it: `Fashion Studio Products`
- Copy the **Spreadsheet ID** from the browser URL:
  ```
  https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
  ```

### 6. Share Spreadsheet with Service Account
- Click the **"Share"** button in the top right corner
- Enter the service account email (found in `client_email` field of `google-sheets-api.json`)
- Set role: **Editor**
- Click **"Share"**

### 7. Set Public Access
- Click **"Share"** again
- Change to **"Anyone with the link"** → role **Editor**
- Click **"Done"**

---

## PostgreSQL Setup

### 1. Install PostgreSQL
Download at https://www.postgresql.org/download/windows/

### 2. Create Database via CLI

```bash
psql -U postgres
```

```sql
CREATE DATABASE fashion_db;
\q
```

### 3. Create `.env` File
Create a `.env` file in the root folder of this project:

```
DB_PASSWORD=your_postgresql_password
```

---

## Configuration

Update the following variables in `main.py`:

```python
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"     # Spreadsheet ID from Google Sheets URL
CREDENTIALS_FILE = "google-sheets-api.json"
DB_NAME = "fashion_db"
```

---

## Running the Pipeline

```bash
python main.py
```

The pipeline runs 3 stages sequentially:
1. **Extract** — Scrapes 50 pages from https://fashion-studio.dicoding.dev
2. **Transform** — Cleans and converts the data
3. **Load** — Saves to CSV, Google Sheets, and PostgreSQL

---

## Running Unit Tests

```bash
python -m pytest tests/ -v
```

---

## Running Test Coverage

```bash
coverage run -m pytest tests/
coverage report -m
```

---

## Tech Stack

| Library | Purpose |
|---|---|
| `requests` | HTTP requests for web scraping |
| `beautifulsoup4` | HTML parsing |
| `pandas` | Data transformation |
| `sqlalchemy` | PostgreSQL connection |
| `psycopg2-binary` | PostgreSQL driver |
| `google-api-python-client` | Google Sheets API |
| `google-auth` | Google authentication |
| `pytest-cov` | Unit testing & coverage |
| `python-dotenv` | Environment variable management |
