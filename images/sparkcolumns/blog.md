---
title: 5 Ways to add a new column in a PySpark Dataframe
date:  2020-02-24
draft: false
url : blog/2020/02/24/sparkcolumns/
slug: sparkcolumns
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: This post is about running XGBoost on Multi-GPU machines.

thumbnail : /images/sparkcolumns/main.png
images :
 - /images/sparkcolumns/main.png
toc : false
---

![](/images/sparkcolumns/main.png)

***Too much data is getting generated day by day.***

***Although sometimes we can manage our big data using tools like [Rapids](https://towardsdatascience.com/minimal-pandas-subset-for-data-scientist-on-gpu-d9a6c7759c7f?source=---------5------------------) or [Parallelization](https://towardsdatascience.com/add-this-single-word-to-make-your-pandas-apply-faster-90ee2fffe9e8?source=---------11------------------), ***Spark is an excellent tool to have in your repertoire if you are working with Terabytes of data.

In my [last post](https://towardsdatascience.com/the-hitchhikers-guide-to-handle-big-data-using-spark-90b9be0fe89a) on Spark, I explained how to work with PySpark RDDs and Dataframes.

Although this post explains a lot on how to work with RDDs and basic Dataframe operations, I missed quite a lot when it comes to working with PySpark Dataframes.

And it is only when I required more functionality that I read up and came up with multiple solutions to do one single thing.

***How to create a new column in spark?***

Now, this might sound trivial, but believe me, it isn’t. With so much you might want to do with your data, I am pretty sure you will end up using most of these column creation processes in your workflow. Sometimes to utilize Pandas functionality, or occasionally to use RDDs based partitioning or sometimes to make use of the mature python ecosystem.

**This post is going to be about — “Multiple ways to create a new column in Pyspark Dataframe.”**

If you have PySpark installed, you can skip the Getting Started section below.

## Getting Started with Spark

I know that a lot of you won’t have spark installed in your system to try and learn. But installing Spark is a headache of its own.

Since we want to understand how it works and work with it, I would suggest that you use Spark on Databricks [**here](https://databricks.com/try-databricks?utm_source=databricks&utm_medium=homev2tiletest)** online with the community edition. Don’t worry, it is free, albeit fewer resources, but that works for us right now for learning purposes.

![](/images/sparkcolumns/0.png)

Once you register and login will be presented with the following screen.

![](/images/sparkcolumns/1.png)

You can start a new notebook here.

Select the Python notebook and give any name to your notebook.

Once you start a new notebook and try to execute any command, the notebook will ask you if you want to start a new cluster. Do it.

The next step will be to check if the sparkcontext is present. To check if the sparkcontext is present, you have to run this command:

    sc

![](/images/sparkcolumns/2.png)

This means that we are set up with a notebook where we can run Spark.

## Data

Here, I will work on the Movielens [**ml-100k.zip](https://github.com/MLWhiz/data_science_blogs/tree/master/spark_post)** dataset. 100,000 ratings from 1000 users on 1700 movies. In this zipped folder, the file we will specifically work with is the rating file. This filename is kept as “u.data”

If you want to upload this data or any data, you can click on the Data tab in the left and then Add Data by using the GUI provided.

![](/images/sparkcolumns/3.png)

We can then load the data using the following commands:

    ratings = spark.read.load("/FileStore/tables/u.data",format="csv", sep="\t", inferSchema="true", header="false")

    ratings = ratings.toDF(*['user_id', 'movie_id', 'rating', 'unix_timestamp'])

Here is how it looks:

    ratings.show()

![](/images/sparkcolumns/4.png)

Ok, so now we are set up to begin the part we are interested in finally. How to create a new column in PySpark Dataframe?

## 1. Using Spark Native Functions

![Photo by [Andrew James](https://unsplash.com/@andrewjamesphoto?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/sparkcolumns/5.png)*Photo by [Andrew James](https://unsplash.com/@andrewjamesphoto?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

The most pysparkish way to create a new column in a PySpark DataFrame is by using built-in functions. This is the most performant programmatical way to create a new column, so this is the first place I go whenever I want to do some column manipulation.

We can use .withcolumn along with PySpark SQL functions to create a new column. In essence, you can find String functions, Date functions, and Math functions already implemented using Spark functions. We can import spark functions as:

    import pyspark.sql.functions as F

Our first function, the F.col function gives us access to the column. So if we wanted to multiply a column by 2, we could use F.col as:

    ratings_with_scale10 = ratings.withColumn("ScaledRating", 2*F.col("rating"))

    ratings_with_scale10.show()

![](/images/sparkcolumns/6.png)

We can also use math functions like F.exp function:

    ratings_with_exp = ratings.withColumn("expRating", 2*F.exp("rating"))

    ratings_with_exp.show()

![](/images/sparkcolumns/7.png)

There are a lot of other functions provided in this module, which are enough for most simple use cases. You can check out the functions list [here](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#module-pyspark.sql.functions).

## 2. Spark UDFs

![Photo by [Divide By Zero](https://unsplash.com/@divide_by_zero?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/sparkcolumns/8.png)*Photo by [Divide By Zero](https://unsplash.com/@divide_by_zero?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Sometimes we want to do complicated things to a column or multiple columns. This could be thought of as a map operation on a PySpark Dataframe to a single column or multiple columns. While Spark SQL functions do solve many use cases when it comes to column creation, I use Spark UDF whenever I want to use the more matured Python functionality.

To use Spark UDFs, we need to use the F.udf function to convert a regular python function to a Spark UDF. We also need to specify the return type of the function. In this example the return type is StringType()

    import pyspark.sql.functions as F
    from pyspark.sql.types import *

    def somefunc(value):
      if   value < 3: 
          return 'low'
      else:
          return 'high'

    #convert to a UDF Function by passing in the function and return type of function

    udfsomefunc = F.udf(somefunc, StringType())

    ratings_with_high_low = ratings.withColumn("high_low", udfsomefunc("rating"))

    ratings_with_high_low.show()

![](/images/sparkcolumns/9.png)

## 3. Using RDDs

![Photo by [Ryan Quintal](https://unsplash.com/@ryanquintal?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/sparkcolumns/10.png)*Photo by [Ryan Quintal](https://unsplash.com/@ryanquintal?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Sometimes both the spark UDFs and SQL Functions are not enough for a particular use-case. You might want to utilize the better partitioning that you get with spark RDDs. Or you may want to use group functions in Spark RDDs. You can use this one, mainly when you need access to all the columns in the spark data frame inside a python function.

Whatever the case be, I find this way of using RDD to create new columns pretty useful for people who have experience working with RDDs that is the basic building block in the Spark ecosystem.

The process below makes use of the functionality to convert between Row and pythondict objects. We convert a row object to a dictionary. Work with the dictionary as we are used to and convert that dictionary back to row again.

    import math
    from pyspark.sql import Row

    def rowwise_function(row):
      # convert row to dict:
      row_dict = row.asDict()
      # Add a new key in the dictionary with the new column name and value. 
      row_dict['Newcol'] = math.exp(row_dict['rating'])
      # convert dict to row:
      newrow = Row(**row_dict)
      # return new row
      return newrow

    # convert ratings dataframe to RDD
    ratings_rdd = ratings.rdd
    # apply our function to RDD
    ratings_rdd_new = ratings_rdd.map(lambda row: rowwise_function(row))
    # Convert RDD Back to DataFrame
    ratings_new_df = sqlContext.createDataFrame(ratings_rdd_new)

    ratings_new_df.show()

![](/images/sparkcolumns/11.png)

## 4. Pandas UDF

![Photo by [Pascal Bernardon](https://unsplash.com/@pbernardon?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/sparkcolumns/12.png)*Photo by [Pascal Bernardon](https://unsplash.com/@pbernardon?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

This functionality was introduced in the Spark version 2.3.1. And this allows you to use pandas functionality with Spark. I generally use it when I have to run a groupby operation on a Spark dataframe or whenever I need to create rolling features and want to use Pandas rolling functions/window functions.

The way we use it is by using the F.pandas_udf decorator. We assume here that the input to the function will be a pandas data frame. And we need to return a pandas dataframe in turn from this function.

The only complexity here is that we have to provide a schema for the output Dataframe. We can make that using the format below.

    # Declare the schema for the output of our function
    outSchema = StructType([StructField('user_id',IntegerType(),True),StructField('movie_id',IntegerType(),True),StructField('rating',IntegerType(),True),StructField('unix_timestamp',IntegerType(),True),StructField('normalized_rating',DoubleType(),True)])

    # decorate our function with pandas_udf decorator
    [@F](http://twitter.com/F).pandas_udf(outSchema, F.PandasUDFType.GROUPED_MAP)
    def subtract_mean(pdf):
        # pdf is a pandas.DataFrame
        v = pdf.rating
        v = v - v.mean()
        pdf['normalized_rating'] =v
        return pdf

    rating_groupwise_normalization = ratings.groupby("movie_id").apply(subtract_mean)

    rating_groupwise_normalization.show()

![](/images/sparkcolumns/13.png)

We can also make use of this to ***train multiple individual models on each spark node. ***For that, we replicate our data and give each replication a key and some training params like max_depth, etc. Our function then takes the pandas Dataframe, runs the required model, and returns the result. The structure would look something like below.

    # 0. Declare the schema for the output of our function
    outSchema = StructType([StructField('replication_id',IntegerType(),True),StructField('RMSE',DoubleType(),True)])

    # decorate our function with pandas_udf decorator
    [@F](http://twitter.com/F).pandas_udf(outSchema, F.PandasUDFType.GROUPED_MAP)
    def run_model(pdf):
        # 1. Get hyperparam values
        num_trees = pdf.num_trees.values[0]
        depth = pdf.depth.values[0]
        replication_id = pdf.replication_id.values[0]
        # 2. Train test split
        Xtrain,Xcv,ytrain,ycv = train_test_split.....
        # 3. Create model using the pandas dataframe
        clf = RandomForestRegressor(max_depth = depth, num_trees=num_trees,....)
        clf.fit(Xtrain,ytrain)
        # 4. Evaluate the model
        rmse = RMSE(clf.predict(Xcv,ycv)
        # 5. return results as pandas DF
        res =pd.DataFrame({'replication_id':replication_id,'RMSE':rmse})
        return res
                    
    results = replicated_data.groupby("replication_id").apply(run_model)

Above is just an idea and not a working code. Though it should work with minor modifications.

## 5. Using SQL

For people who like [SQL](https://towardsdatascience.com/learning-sql-the-hard-way-4173f11b26f1?source=---------10------------------), there is a way even to create columns using SQL. For this, we need to register a temporary SQL table and then use simple select queries with an additional column. One might also use it to do joins.

    ratings.registerTempTable('ratings_table')
    newDF = sqlContext.sql('select *, 2*rating as newCol from ratings_table')
    newDF.show()

![](/images/sparkcolumns/14.png)

## Conclusion

![Photo by [Kelly Sikkema](https://unsplash.com/@kellysikkema?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/sparkcolumns/15.png)*Photo by [Kelly Sikkema](https://unsplash.com/@kellysikkema?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

And that is the end of this column(pun intended)

Hopefully, I’ve covered the column creation process well to help you with your Spark problems. If you need to learn more of spark basics, take a look at:
[**The Hitchhikers guide to handle Big Data using Spark**
*Not just an Introduction*towardsdatascience.com](https://towardsdatascience.com/the-hitchhikers-guide-to-handle-big-data-using-spark-90b9be0fe89a)

***You can find all the code for this post at the [GitHub repository](https://github.com/MLWhiz/data_science_blogs/blob/master/spark_columns/Columns.ipynb) or the [published notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/7664398068420572/312750581110937/3797400441762013/latest.html) on databricks.***

Also, if you want to learn more about Spark and Spark DataFrames, I would like to call out an excellent course on [**Big Data Essentials](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.11468293556&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Fbig-data-essentials),** which is part of the [**Big Data Specialization](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.11468293466&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Fspecializations%2Fbig-data-engineering)** provided by Yandex.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [**@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)**

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
