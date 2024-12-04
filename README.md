# Sales Analytics and Web Scraping Tool

## Project Overview
This project consists of two Python scripts:
1. Web Scraping Tool (`web_scraper.py`)
2. Sales KPI Dashboard Generator (`kpi_dashboard.py`)

## Prerequisites

### System Requirements
- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Dark-Kernel/sales-analytixs.git
cd sales-analytixs
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv sales-env
source sales-env/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies

#### Web Scraping Tool
> We can use selenium if needed for dynamic websites
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `csv`: Data export
- `logging`: Error tracking and logging

#### KPI Dashboard
- `pandas`: Data manipulation
- `plotly`: Interactive visualizations
- `openpyxl`: Excel file support

## Scripts Description

### 1. Web Scraper (`web_scraper.py`)

#### Features
- Scrapes data from publicly accessible websites
- Handles pagination
- Robust error handling
- Exports data to CSV

#### Usage
```bash
python web_scraper.py
```

#### Customization
- Modify `base_url` to scrape different websites
- Adjust `max_pages` to control scraping depth
- Customize data extraction in `_extract_book_details()` method

### 2. KPI Dashboard (`kpi_dashboard.py`)

#### Features
- Supports CSV and Excel input files
- Generates interactive HTML dashboard
- Calculates multiple KPIs by category
- Produces visualizations and summary tables

#### Usage
```bash
python kpi_dashboard.py
```

#### Input File Requirements
Your sales data file must have the following columns:
- `Date`
- `ProductID`
- `ProductName`
- `Category`
- `QuantitySold`
- `PricePerUnit`
- `TotalSales`

#### Customization
- Modify `calculate_kpis()` to add or change KPI calculations
- Adjust `create_visualizations()` to modify chart types or styling

## Scheduling Automation

### Linux/Mac (Cron)
1. Open terminal
2. Edit crontab:
```bash
crontab -e
```
3. Add scheduling line:
```bash
0 0 * * * /path/to/python /path/to/kpi_dashboard.py  # Runs daily at midnight
```
> For more information, see [Cron](https://crontab.guru/)

### Windows (Task Scheduler)
> Maybe something is missing, because I don't have windows
1. Open Task Scheduler
2. Create a new task
3. Set trigger (daily/weekly)
4. Set action to run Python script
5. Specify full path to Python and script

