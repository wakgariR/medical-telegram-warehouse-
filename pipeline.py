from dagster import job, op
import os

# Import your existing scripts
from src import telegram_scraper
from src import database
from src import dbt_runner
from src import yolo_detect
from dagster import job, op
from src import telegram_scraper, database, dbt_runner, yolo_detect

@op
def scrape_telegram_data():
    telegram_scraper.scrape_all_channels()
    return "Scraping Done"

@op
def load_raw_to_postgres():
    database.load_raw_data("data/raw/telegram_messages")
    return "Raw Data Loaded"

@op
def run_dbt_transformations():
    dbt_runner.run_dbt()
    return "DBT Models Completed"

@op
def run_yolo_enrichment():
    yolo_detect.run_yolo()
    return "YOLO Enrichment Completed"

@job
def telegram_pipeline():
    scraped = scrape_telegram_data()
    loaded = load_raw_to_postgres()
    loaded  # sets dependency: load runs after scrape
    dbt_done = run_dbt_transformations()
    dbt_done  # runs after load
    run_yolo_enrichment()  # runs after dbt
