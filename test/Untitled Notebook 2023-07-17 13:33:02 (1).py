# Databricks notebook source

File Operations Sample
Various file operations sample such as Azure Blob Storage mount & umount, ls/rm/cp/mv, read CSV file, etc

1. Direct Connection to Azure Blob Storage
Configure Azure Blob Storage Connection Key

spark.conf.set(
  "fs.azure.account.key.databrickstore.blob.core.windows.net",
  "S1PtMWvUw5If1Z8FMzXAxC7OMw9G5Go8BGCXJ81qpFVYpZ9dpXOnU4zlg0PbldKkbLIbmbv02WoJsgYLGKIfgg==")
     
Reading Blob files directly

dbutils.fs.ls("wasbs://mountpoint001@databrickstore.blob.core.windows.net")
     
2. Mounting Azure Blob Storage container
Configure to mount Azure Blob Storage container onto local dir

dbutils.fs.mount(
  source = "wasbs://sharedlib@databrickstore.blob.core.windows.net",
  mount_point = "/mnt/azstorage",
  extra_configs = {"fs.azure.account.key.databrickstore.blob.core.windows.net": "S1PtMWvUw5If1Z8FMzXAxC7OMw9G5Go8BGCXJ81qpFVYpZ9dpXOnU4zlg0PbldKkbLIbmbv02WoJsgYLGKIfgg=="})
     
List files

dbutils.fs.ls("/mnt/azstorage")
     
Copy files to local dir

dbutils.fs.cp("/mnt/azstorage/libmecab.so", "file:/usr/lib/libmecab.so")
     
Remove files in local dir

dbutils.fs.rm("file:/usr/lib/libmecab.so")
     
List files in local dir

dbutils.fs.ls("file:/usr/lib/")
     
Read json file from mounted dir using Json parser and write them into SQL table

%sql
DROP TABLE IF EXISTS radio_sample_data;
CREATE TABLE radio_sample_data
USING json
OPTIONS (
 path "/mnt/azstorage/small_radio_json.json"
)
     
select from SQL table

%sql
SELECT * from radio_sample_data
     
Unmount the dir

# dbutils.fs.unmount("/mnt/azstorage")
     
3. Read file using CSV parser

display(dbutils.fs.ls("/databricks-datasets"))
     
Read CSV file in the Spark CSV datasource with options specifying
First line of file is a header
Automatically infer the schema of the data

# Use the Spark CSV datasource with options specifying:
#  - First line of file is a header
#  - Automatically infer the schema of the data
data = sqlContext.read.format("com.databricks.spark.csv")\
  .option("header", "true")\
  .option("inferSchema", "true")\
  .load("/databricks-datasets/samples/population-vs-price/data_geo.csv")
data.cache()  # Cache data for faster reuse
# data.count()
display(data)
     
