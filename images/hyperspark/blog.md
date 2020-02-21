---
title: 100x faster Hyperparameter Search Framework with Pyspark
date:  2020-02-21
draft: false
url : blog/2020/02/22/hyperspark/
slug: hyperspark
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: This post is about setting up a hyperparameter tuning framework for Data Science using scikit-learn/xgboost/lightgbm and pySpark

thumbnail : /images/hyperspark/main.png
images :
 - /images/hyperspark/main.png
toc : false
---

![](/images/hyperspark/main.png)

Recently I was working on tuning hyperparameters for a huge Machine Learning model.

Manual tuning was not an option since I had to tweak a lot of parameters. [Hyperopt](https://towardsdatascience.com/automate-hyperparameter-tuning-for-your-models-71b18f819604) was also not an option as it works serially i.e. at a time, only a single model is being built. So it was taking up a lot of time to train each model and I was pretty short on time.

I had to come up with a better more efficient approach if I were to meet the deadline. So I thought of the one thing that helps us data scientists in many such scenarios — ***Parallelization.***

***Can I parallelize my model hyperparameter search process?***

As you would have guessed, the answer is Yes.

***This post is about setting up a hyperparameter tuning framework for Data Science using scikit-learn/xgboost/lightgbm and pySpark.***

## Grid vs Randomized?

Before we get to implementing the hyperparameter search, we have two options to set up the hyperparameter search — Grid Search or Random search.

![Starting with a 3×3 grid of parameters, we can see that Random search ends up doing more searches for the important parameter.](/images/hyperspark/0.png)*Starting with a 3×3 grid of parameters, we can see that Random search ends up doing more searches for the important parameter.*

The figure above gives a definitive answer as to why Random search is better.

Let’s say we have to tune two hyperparameters for our Machine Learning model. One is not important, and one is very important. In a grid search, we look at three settings for the important parameter. While in a randomized search, we search through 9 settings for the important parameter. And the amount of time we spent is the same.

Since, Randomized search, searches more thoroughly through the whole space and provides us with better hyperparameters, we will go with it in our example.

## Setting Up Our Example

At my workplace, I have access to a pretty darn big cluster with 100s of nodes. It is a data Scientist’s dream. But in this post, I am going to be using the Databricks Community Edition Free server with a toy example. If you want to set up this small server for yourself for practice, check out my [post](https://towardsdatascience.com/the-hitchhikers-guide-to-handle-big-data-using-spark-90b9be0fe89a) on Spark.

You can choose to load your data using Spark, but here I start by creating our own classification data to set up a minimal example which we can work with.

    X,y = datasets.make_classification(n_samples=10000, n_features=4, n_informative=2, n_classes=2, random_state=1,shuffle=True)

    train = pd.DataFrame(X)
    train['target'] = y

    # Convert this pandas Data to spark Dataframe. 
    train_sp = spark.createDataFrame(train)

    # Change the column names.
    train_sp = train_sp.toDF(*['c0', 'c1', 'c2', 'c3', 'target'])

The train_sp spark dataset looks like:

![](/images/hyperspark/1.png)

## The Idea — Replicate and Apply

![Photo by [Frank Vessia](https://unsplash.com/@frankvex?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/hyperspark/2.png)*Photo by [Frank Vessia](https://unsplash.com/@frankvex?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

So now we have got our training dataset in Spark. And we want to run multiple models on this DataFrame.

Spark is inherently good with Key-Value pairs. That is all data with a particular key could be sent to a single machine. And we can apply functions to that data.

But we want all our data on every machine. How do we do that?

***We replicate our data n times and add a replication_id to our data so that each key has all the data.***

Ok, now we can send the whole data to multiple machines using groupby on replication_id. But how do we use pandas and scikit learn on that data?

***The answer is: we use pandas_udf. ***This functionality was introduced in the Spark version 2.3.1. And this allows you to utilise pandas functionality with Spark.

If you don’t understand this yet, do look at the code as sometimes it is easier to understand the code.

## The Code

We first replicate our train dataframe 100 times here by using cross_join with a data frame that contains a column with 1–100 replication_id.

    # replicate the spark dataframe into multiple copies

    replication_df = spark.createDataFrame(pd.DataFrame(list(range(1,100)),columns=['replication_id']))

    **replicated_train_df = train_sp.crossJoin(replication_df)**

![Every row is replicated 100 times with different replication_id](/images/hyperspark/3.png)*Every row is replicated 100 times with different replication_id*

We also define a function that takes as input a pandas dataframe, gets random hyperparameters using the python random module, runs a model on data(Here I am training a scikit model, but you can replace it with any model like XGBoost or Lightgbm as well) and returns the result in the form of a Pandas Dataframe. Do take a look at the function and the comments.

<iframe src="https://medium.com/media/6712e8f8099a96c2b0c1246f538e3be1" frameborder=0></iframe>

We can now apply this pandas_udf function to our replicated dataframe using:

    results = replicated_train_df.groupby("replication_id").apply(run_model)

What the above code does is that it sends all the data with the same replication id to a single machine and applies the function run_model to the data. The above call happens lazily so you won’t be able to see the results till you run the below action call.

    results.sort(F.desc("Accuracy")).show()

![Results of our Hyperparameter search](/images/hyperspark/4.png)*Results of our Hyperparameter search*

For this toy example, the accuracy results may look pretty close to one another, but they will differ in the case of noisy real-world datasets. Since all of these 100 models run in parallel on different nodes, we can save a lot of time when doing random hyperparameter search.

The speedup factor certainly depends on how many nodes you have in your cluster. For me, I had 100 machines at my disposal, so I got ~ 100x speedup.

You can get the full code in this Databricks [Notebook](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/7664398068420572/3438177909678058/3797400441762013/latest.html) or get it from my [GitHub](https://github.com/MLWhiz/data_science_blogs/tree/master/spark_hyperparams_tuning) repository where I keep codes for all my posts.

## Continue Learning

If you want to learn more about practical data science, do take a look at the [**“How to win a data science competition”](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-BShznKdc3CUauhfsM7_8xw&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0)** Coursera course. I learned a lot of new things from this course taught by one of the most prolific Kaggler.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources as sharing knowledge is never a bad idea.
