
import os
import glob
import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum


print("=" * 60)
print("STEP 0 - GENERAZIONE DATASET")
print("=" * 60)


BASE_DIR = "./data_local"
PARQUET_DIR = os.path.join(BASE_DIR, "parquet")
JSON_DIR = os.path.join(BASE_DIR, "json")


print("\n" + "=" * 60)
print("ESERCIZIO 1A - PANDAS")
print("=" * 60)

json_files = glob.glob(os.path.join(JSON_DIR, "*.jsonl"))

total_amount = 0

for file in json_files:
    df = pd.read_json(file, lines=True)
    file_total = df["amount"].sum()
    total_amount += file_total
    print(f"File: {os.path.basename(file)} -> Totale: {file_total:.2f}")

print("\nTotale generale Pandas:", round(total_amount, 2))


print("\n" + "=" * 60)
print("ESERCIZIO 1B - DASK")
print("=" * 60)


sample_df = pd.read_json(json_files[0], lines=True)

if "payment_type" not in sample_df.columns:
    payment_types = ["Credit Card", "PayPal", "Cash", "Bank Transfer"]

    for file in json_files:
        temp_df = pd.read_json(file, lines=True)
        temp_df["payment_type"] = pd.Series(payment_types * (len(temp_df) // len(payment_types) + 1))[:len(temp_df)]
        temp_df.to_json(file, orient="records", lines=True)



dask_df = dd.read_json(
    os.path.join(JSON_DIR, "*.jsonl"),
    lines=True
)

result = (
    dask_df.groupby("payment_type")["amount"]
    .mean()
    .compute()
)

print("\nMedia importi per payment_type:")
print(result)


print("\n" + "=" * 60)
print("ESERCIZIO 2 - PYSPARK ETL")
print("=" * 60)

spark = SparkSession.builder \
    .appName("MegaShopPipeline") \
    .getOrCreate()


transactions_df = spark.read.parquet(
    os.path.join(PARQUET_DIR, "transactions_batch_*.parquet")
)

products_df = spark.read.parquet(
    os.path.join(PARQUET_DIR, "products.parquet")
)

regions_df = spark.read.parquet(
    os.path.join(PARQUET_DIR, "regions.parquet")
)

print("\nTransazioni:")
transactions_df.show(5)

print("\nProdotti:")
products_df.show(5)

print("\nRegioni:")
regions_df.show(5)


joined_df = transactions_df.join(
    products_df,
    on="product_id",
    how="inner"
)

joined_df = joined_df.join(
    regions_df,
    on="region_id",
    how="inner"
)

final_df = joined_df.select(
    "transaction_id",
    "region_name",
    "category",
    "amount",
    "year"
)

print("\nDataFrame Finale:")
final_df.show(10)


output_path = os.path.join(BASE_DIR, "processed_sales")

final_df.write \
    .mode("overwrite") \
    .partitionBy("year") \
    .parquet(output_path)

print(f"\nDati salvati in: {output_path}")


print("\n" + "=" * 60)
print("ESERCIZIO 3 - DATA VISUALIZATION")
print("=" * 60)

revenue_df = final_df.groupBy("category") \
    .agg(spark_sum("amount").alias("total_revenue"))

revenue_pandas = revenue_df.toPandas()

print("\nFatturato per categoria:")
print(revenue_pandas)


plt.figure(figsize=(10, 6))

sns.barplot(
    data=revenue_pandas,
    x="category",
    y="total_revenue"
)

plt.title("Fatturato Totale per Categoria")
plt.xlabel("Categoria")
plt.ylabel("Fatturato")
plt.xticks(rotation=45)

plt.tight_layout()

image_path = "fatturato_per_categoria.png"

plt.savefig(image_path)

print(f"\nGrafico salvato come: {image_path}")

plt.show()


spark.stop()

print("\nPipeline completata con successo!")
