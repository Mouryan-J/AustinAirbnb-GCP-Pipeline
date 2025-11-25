# InsideAirbnb Austin – GCP Data Pipeline

This repository contains my course project for **INFO-I535: Big Data Concepts**.  
I built a simple but complete cloud pipeline for the **InsideAirbnb Austin** listings dataset (~15,000 rows).

The main goal is to show how to ingest, clean, store, and visualize data using managed Google Cloud services.

---

## 1. Project Overview

- Use the public **InsideAirbnb Austin** dataset.
- Upload raw data to **Google Cloud Storage (GCS)**.
- Clean and transform the data with **PySpark** running on **Dataproc**.
- Store the cleaned table in **BigQuery**.
- Build interactive charts and maps in **Looker Studio**.

The focus is on the pipeline and data engineering steps, not on complex analytics.

---

## 2. Dataset

- Source: InsideAirbnb – Austin, Texas listings (2024 snapshot).
- Size: ~15,000 rows.
- Example fields:
  - `price`, `property_type`, `bedrooms`, `bathrooms`
  - `host_neighbourhood`, `host_response_time`, `host_response_rate`
  - `latitude`, `longitude`
  - `review_scores_rating`, `number_of_reviews`

---

## 3. Pipeline Architecture

1. **Cloud Storage**
   - Bucket with folders:
     - `raw/` – original `listings.csv`
     - `processed/` – cleaned data 
     - `scripts/` – PySpark cleaning script
     - `logs/` – job logs
2. **Dataproc + PySpark**
   - Single-node cluster (`n1-standard-4`).
   - Runs `preprocessing.py` to clean the dataset.
3. **BigQuery**
   - Dataset: `airbnb_dataset`
   - Main table: `preproccessed_lisitings`
4. **Looker Studio**
   - Connects to BigQuery and shows charts and maps.

---

## 4. Data Cleaning Steps (PySpark)

In `preprocessing.py`:

- Select only useful columns (host, price, reviews, location, property info).
- Trim spaces and clean text fields.
- Normalize Unicode and remove non-ASCII characters.
- Clean `price` and percentage fields (remove `$`, `%`, commas).
- Convert all numeric fields to the right types.
- Fill missing numeric values with the **median**.
- Fill missing categorical values (e.g., neighbourhood, property_type) with the **most frequent value**.
- Drop rows with missing latitude or longitude.
- Write the final cleaned table to **BigQuery**.

---

## 5. BigQuery Queries

In `bigquery-views.sql` you will find example queries, including:

- Average price by property type.
- Number of listings by neighbourhood.
- Average price by neighbourhood.
- Price vs accommodates (bed capacity).
- Price vs review rating.
- Host total listings vs price and rating.
- Bedrooms/bathrooms vs average price.
- Review count vs rating.

These queries were used to understand the visualizations.

---

## 6. Visualizations (Looker Studio)

Main charts and maps created:

- **Listings by Neighbourhood** (bar chart).
- **Average Price by Property Type** (bar chart).
- **Average Review Rating by Neighbourhood** (treemap).
- **Average Price vs Number of Bedrooms** (bar chart).
- **Map of rentals in Zilker** (bubble map).
- **Map of listings with review score < 3** (bubble map).


Screenshots are stored in the `images/` folder.

