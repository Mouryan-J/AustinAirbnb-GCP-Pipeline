from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import unicodedata

# Starting Spark
spark = SparkSession.builder \
    .appName("AirbnbCleaningUTF8") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

PROJECT_ID = "fa25-i535-mjayasan-airbnb"
BUCKET_NAME = "airbnb-austin-mjayasan"
INPUT_PATH = f"gs://{BUCKET_NAME}/raw/listings.csv"   # changed listings.csv.gz

print("Reading CSV...")
df = spark.read \
    .option("header", "true") \
    .option("multiLine", "true") \
    .option("escape", '"') \
    .option("quote", '"') \
    .option("mode", "PERMISSIVE") \
    .csv(INPUT_PATH)

print(f"Initial rows: {df.count()}")
print(f"Initial columns: {len(df.columns)}")


# Keeping only needed columns
keep_cols = [
    "host_response_time",
    "host_response_rate",
    "host_acceptance_rate",
    "host_neighbourhood",
    "host_listings_count",
    "host_total_listings_count",
    "latitude",
    "longitude",
    "property_type",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "price",
    "number_of_reviews",
    "review_scores_rating",
    "review_scores_cleanliness",
    "review_scores_location"
]
df = df.select([col(c) for c in keep_cols])


# Trim extra spaces
for c, t in df.dtypes:
    if t == "string":
        df = df.withColumn(c, trim(col(c)))


# Clean unicode to avoid BigQuery issues
def clean_unicode(x):
    if x is None:
        return None
    x = unicodedata.normalize("NFKD", x)
    x = "".join([c for c in x if ord(c) < 128])  # remove non-ASCII
    return x.strip()

cleanUDF = udf(clean_unicode, StringType())

string_cols = [c for c, t in df.dtypes if t == "string"]
for c in string_cols:
    df = df.withColumn(c, cleanUDF(col(c)))


# Replace unwanted text with NULL
df = df.replace(["Unknown", "unknown", "N/A", "NA", ""], None)


# Clean price to numeric
df = df.withColumn(
    "price",
    regexp_replace(regexp_replace(col("price").cast("string"), "\\$", ""), ",", "").cast("double")
)


# Convert % strings to numeric
percent_cols = ["host_response_rate", "host_acceptance_rate"]
for c in percent_cols:
    df = df.withColumn(c, regexp_replace(col(c).cast("string"), "%", "").cast("double"))


# Convert numeric fields
numeric_cols = [
    "host_listings_count",
    "host_total_listings_count",
    "latitude",
    "longitude",
    "accommodates",
    "bathrooms",
    "bedrooms",
    "price",
    "number_of_reviews",
    "review_scores_rating",
    "review_scores_cleanliness",
    "review_scores_location",
    "host_response_rate",
    "host_acceptance_rate"
]

for c in numeric_cols:
    df = df.withColumn(c, col(c).cast(DoubleType()))


# Fill numeric NULLs with median
for c in numeric_cols:
    median_val = df.approxQuantile(c, [0.5], 0.01)[0]
    df = df.withColumn(
        c,
        when(col(c).isNull(), median_val).otherwise(col(c))
    )


# Fill categorical NULLs with mode (most frequent)
categorical_cols = [
    "host_response_time",
    "host_neighbourhood",
    "property_type"
]

for c in categorical_cols:
    mode_item = df.groupBy(c).count().orderBy(desc("count")).first()
    mode_val = mode_item[0] if mode_item else None

    df = df.withColumn(
        c,
        when(col(c).isNull() | (col(c) == ""), mode_val).otherwise(col(c))
    )


# Remove rows missing geospatial info
df = df.dropna(subset=["latitude", "longitude"])


print("Cleaned sample:")
df.show(20, truncate=False)


# Write cleaned data to BigQuery
df.write \
    .format("bigquery") \
    .option("table", "fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings") \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .mode("overwrite") \
    .save()

print("Cleaning complete. BigQuery load successful.")
