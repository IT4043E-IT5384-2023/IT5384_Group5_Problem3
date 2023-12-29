from pyspark.sql import SparkSession
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

spark = (SparkSession.builder.appName("grp5_prb3").master("spark://34.142.194.212:7077")
         .config("spark.jars", "C:/Users/SVBK/Desktop/2023.1/Big data/prj3/gcs-connector-hadoop2-latest.jar")
         .config("spark.executor.memory", "1G")  # excutor excute only 2G
         .config("spark.driver.memory", "4G")
         .config("spark.debug.maxToStringFields", "1000000")
         # Cluster use only 3 cores to excute as it has 3 server
         .config("spark.executor.cores", "1")
         # each worker use 1G to excute
         .config("spark.python.worker.memory", "1G")
         # Maximum size of result is 3G
         .config("spark.driver.maxResultSize", "3G")
         .config("spark.kryoserializer.buffer.max", "1024M")
         .config("spark.port.maxRetries", "100")
         .getOrCreate())
# config the credential to identify the google cloud hadoop file
spark.conf.set("google.cloud.auth.service.account.json.keyfile",
               "C:/Users/SVBK/Desktop/2023.1/Big data/prj3/lucky-wall-393304-2a6a3df38253.json")
spark._jsc.hadoopConfiguration().set(
    'fs.gs.impl', 'com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem')
spark._jsc.hadoopConfiguration().set('fs.gs.auth.service.account.enable', 'true')

es = Elasticsearch("http://34.143.255.36:9200/",basic_auth=('elastic', 'elastic2023'))

data = spark.read.json("C:/Users/SVBK/Desktop/2023.1/Big data/prj3/tweet_information.json")
data_dicts = data.toJSON().map(lambda x: json.loads(x)).collect()

actions = [
    {
        "_index": "grp5_prb3",
        "_source": record
    }
    for record in data_dicts
]

bulk(es, actions)
spark.stop()
