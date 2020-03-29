---
title: Practical Spark Tips for Data Scientists
date:  2020-03-20
draft: false
url : blog/2020/03/20/sparktips/
slug: sparktips
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: This post is going to be about Multiple ways to create a new column in Pyspark Dataframe

thumbnail : /images/sparktips/main.png
images :
 - /images/sparktips/main.png
toc : false
---


***I know — Spark is sometimes frustrating to work with.***

***Although sometimes we can manage our big data using tools like [Rapids](https://towardsdatascience.com/minimal-pandas-subset-for-data-scientist-on-gpu-d9a6c7759c7f?source=---------5------------------) or [Parallelization](https://towardsdatascience.com/add-this-single-word-to-make-your-pandas-apply-faster-90ee2fffe9e8?source=---------11------------------), ***there is no way around using*** ***Spark if you are working with Terabytes of data.

In my [l](https://towardsdatascience.com/the-hitchhikers-guide-to-handle-big-data-using-spark-90b9be0fe89a)ast few posts on Spark, I explained how to work with [PySpark RDDs](https://towardsdatascience.com/the-hitchhikers-guide-to-handle-big-data-using-spark-90b9be0fe89a) and [Dataframes](https://towardsdatascience.com/5-ways-to-add-a-new-column-in-a-pyspark-dataframe-4e75c2fd8c08). Although these posts explain a lot on how to work with RDDs and Dataframe operations, they still are not quite enough.

Why? Because Spark gives memory errors a lot of times, and it is only when you genuinely work on big datasets with spark, would you be able to truly work with Spark.

**This post is going to be about — “Practical Spark and memory management tips for Data Scientists.”**

## 1. Map Side Joins

![Joining Dataframes](/images/practicalspark/0.png)*Joining Dataframes*

The syntax of joins in Spark is pretty similar to pandas:

    df3 = df1.join(df2, df1.column == df2.column,how='left')

But I faced a problem. The df1 had around 1Billion rows while df2 had around 100 Rows. When I tried the above join, it didn’t work and failed with memory exhausted errors after running for 20 minutes.

I was writing this code on a pretty big cluster with more than 400 executors with each executor having more than 4GB RAM. I was stumped as I tried to repartition my data frames using multiple schemes, but nothing seemed to work.

So what should I do? Is Spark not able to work with a mere billion rows? Not Really. I just needed to use Map-side joins or broadcasting in Spark terminology.

    **from** **pyspark.sql.functions** **import** broadcast
    df3 = df1.join(broadcast(df2), df1.column == df2.column,how='left')

Using the simple broadcasting code above, I was able to send the smaller df2 to all the nodes, and this didn’t take a lot of time or memory. What happens in the backend is that a copy of df2 is sent to all the partitions and each partition uses that copy to do the join. That means that there is no data movement when it comes to df1, which is a lot bigger than df2.

## 2. Spark Cluster Configurations

![Set the Parallelism and worker nodes based on your task size](/images/practicalspark/1.png)*Set the Parallelism and worker nodes based on your task size*

What also made my life difficult while I was starting work with Spark was the way the Spark cluster needs to be configured. Your spark cluster might need a lot of custom configuration ad tuning based on the job you want to run.

Some of the most important configurations and options are as follows:

### a. spark.sql.shuffle.partitions and spark.default.parallelism:

spark.sql.shuffle.partitions configures the number of partitions to use when shuffling data for joins or aggregations. The spark.default.parallelism is the default number of partitions in RDDs returned by transformations like join, reduceByKey, and parallelize when not set by the user. The default value for these is 200.

***In simple words, these set the degree of parallelism you want to have in your cluster.***

If you don’t have a lot of data, the value of 200 is fine, but if you have huge data, you might want to increase these numbers. It also depends on the number of executors you have. My cluster was pretty big with 400 executors, so I kept this at 1200. A rule of thumb is to keep it as a multiple of the number of executors so that each executor ends up with multiple jobs.

    sqlContext.setConf( "spark.sql.shuffle.partitions", 800)
    sqlContext.setConf( "spark.default.parallelism", 800)

### b. spark.sql.parquet.binaryAsString

I was working with .parquet files in Spark, and most of my data columns were strings. But somehow whenever I loaded the data in Spark, the string columns got converted into binary format on which I was not able to use any string manipulation functions. The way I solved this was by using:

    sqlContext.setConf("spark.sql.parquet.binaryAsString","true")

The above configuration converts the binary format to string while loading parquet files. Now it is a default configuration I set whenever I work with Spark.

### c. Yarn Configurations:

There are other configurations that you might need to tune that define your cluster. But these need to be set up when the cluster is starting and are not as dynamic as the above ones. The few I want to put down here are for managing memory spills on the executor nodes. Sometimes the executor core gets a lot of work.

* spark.yarn.executor.memoryOverhead: 8192

* yarn.nodemanager.vmem-check-enabled: False

There are a lot of configurations that you might want to tune while setting up your spark cluster. You can take a look at them in the [official docs](https://spark.apache.org/docs/latest/configuration.html).

## 3. Repartitioning

![Keeping the workers happy by having them handle an equal amount of data](/images/practicalspark/2.png)*Keeping the workers happy by having them handle an equal amount of data*

You might want to repartition your data if you feel your data has been skewed while working with all the transformations and joins. The simplest way to do it is by using:

    df = df.repartition(1000)

Sometimes you might also want to repartition by a known scheme as this scheme might be used by a certain join or aggregation operation later on. You can use multiple columns to repartition using:

    *df = df.repartition('cola', 'colb','colc','cold')*

You can get the number of partitions in a data frame using:

    df.rdd.getNumPartitions()

You can also check out the distribution of records in a partition by using the glom function. This helps in understanding the skew in the data that happens while working with various transformations.

    *df.glom().map(len).collect()*

## Conclusion

There are a lot of things we don’t know, we don’t know. These are called unknown unknowns. It is only by multiple code failures and reading up on multiple stack overflow threads that we understand what we need.

Here I have tried to summarize a few of the problems that I faced around memory issues and configurations while working with Spark and how to solve them. There are a lot of other configuration options in Spark, which I have not covered, but I hope this post gave you some clarity on how to set these and use them.

Now, if you need to learn Spark basics, take a look at my previous post:
[**The Hitchhikers guide to handle Big Data using Spark**
*Not just an Introduction*towardsdatascience.com](https://towardsdatascience.com/the-hitchhikers-guide-to-handle-big-data-using-spark-90b9be0fe89a)

Also, if you want to learn more about Spark and Spark DataFrames, I would like to call out these excellent courses on [**Big Data Essentials: HDFS, MapReduce and Spark RDD](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.11468293556&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Fbig-data-essentials)** and [**Big Data Analysis: Hive, Spark SQL, DataFrames and GraphFrames](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.11468293488&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Fbig-data-analysis)** by Yandex on Coursera.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [**@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)**

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
