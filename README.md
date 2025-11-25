
# **Airbnb Austin – Cloud-Based Big Data Processing Pipeline**

This repository contains the implementation and documentation of a complete cloud-native data engineering workflow built using the *InsideAirbnb Austin* dataset. The project demonstrates raw data ingestion, distributed preprocessing, scalable analytical storage, and visualization using Google Cloud Platform (GCP). It was developed as part of the **Big Data Concepts and Implementations** course at Indiana University Bloomington.

---

## **1. Project Overview**

The primary objective of this project is to design and execute a reproducible big-data processing pipeline using managed cloud services. The workflow integrates multiple GCP components—Cloud Storage, Dataproc (PySpark), BigQuery, and Looker Studio—to demonstrate how large, semi-structured datasets can be systematically cleaned, structured, queried, and visualized in a modern cloud ecosystem.

The dataset used is the 2024 InsideAirbnb Austin listings file (~15,000 rows), containing host attributes, pricing information, geolocation coordinates, and review metrics.

---

## **2. System Architecture**

The project follows a multi-stage architecture typical of professional data engineering pipelines:

```
               ┌────────────────────────┐
               │ InsideAirbnb Dataset   │
               └────────────┬───────────┘
                            ▼
                ┌────────────────────┐
                │ Google Cloud Storage│
                │ raw/  scripts/     │
                └───────────┬────────┘
                            ▼
                 ┌────────────────────┐
                 │ Dataproc (PySpark) │
                 │ Data Cleaning Job  │
                 └───────────┬────────┘
                            ▼
                ┌──────────────────────┐
                │   BigQuery Dataset   │
                │ preprocessed listings│
                └──────────┬───────────┘
                            ▼
                ┌──────────────────────┐
                │    Looker Studio     │
                │  Dashboards & Maps   │
                └──────────────────────┘
```

This structure separates raw, processed, and analytical layers, ensuring reproducibility and clear data lineage.

---

## **3. Data Processing Workflow**

### **3.1 Data Ingestion**

The raw CSV file (`listings.csv`) is uploaded to Google Cloud Storage under a dedicated `raw/` directory. Cloud Storage serves as the durable and centralized ingestion point.

### **3.2 PySpark Preprocessing on Dataproc**

A single-node Dataproc cluster executes the `preprocessing.py` PySpark script.
Key processing steps include:

* Unicode normalization (NFKD) to resolve BigQuery encoding conflicts
* Removal of non-ASCII characters
* Trimming and standardization of categorical fields
* Cleaning of price and percentage fields
* Conversion of all numeric columns to `DoubleType`
* Median imputation for missing numerical values
* Mode imputation for categorical columns
* Removal of geospatially incomplete rows
* Writing the processed dataset directly to BigQuery

The BigQuery connector (`spark-bigquery-latest_2.12.jar`) enables seamless integration.

### **3.3 Analytical Queries in BigQuery**

A collection of SQL queries (stored in `bigquery-views.sql`) is used to explore relationships across pricing, neighbourhood trends, host characteristics, review behaviour, and spatial patterns.

### **3.4 Visualization in Looker Studio**

Looker Studio dashboards provide interactive summaries such as:

* Geographic distribution of listings
* Average price by property type
* Review scores by neighbourhood
* Listings count per neighbourhood
* Price vs. bedrooms
* Map of low-rated properties

Each visualization directly connects to the BigQuery table, ensuring real-time updates.

---

## **4. Repository Structure**

```
Airbnb-GCP-Pipeline/
│
├── preprocessing.py                 # PySpark cleaning script
├── bigquery-views.sql               # Analytical SQL queries
├── README.md                        # Project documentation
│
└── images/                          # Visualization outputs
      ├── avg_price_property_type.jpg
      ├── avg_review_rating_neighbourhood.jpg
      ├── listings_by_neighbourhood.jpg
      ├── bedrooms_vs_price.jpg
      ├── map_low_reviews.jpg
      ├── map_all_listings.jpg
```

---

## **5. Technologies Used**

* **Google Cloud Storage** – Ingestion and persistent storage
* **Google Dataproc (PySpark)** – Distributed preprocessing
* **Google BigQuery** – Analytical data warehouse
* **Looker Studio** – Visualization and dashboarding
* **InsideAirbnb Dataset** – Public dataset source

This pipeline exemplifies cloud-native processing using virtualization, distributed execution, and schema-driven analytics.

---

## **6. Dataset Source**

Inside Airbnb Project
[https://insideairbnb.com](https://insideairbnb.com)

Austin, Texas listings — September 2024 release.

---

## **7. Author**

**Mouryan Jayasankar**
Indiana University Bloomington


