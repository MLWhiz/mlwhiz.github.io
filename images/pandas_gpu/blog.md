---
title: Minimal Pandas Subset for Data Scientists on GPU
date:  2020-02-22
draft: false
url : blog/2020/02/22/pandas_gpu/
slug: pandas_gpu
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: In this post, I will talk about handling most of those data manipulation cases in Python on a GPU using cuDF.

thumbnail : /images/pandas_gpu/main.png
images :
 - /images/pandas_gpu/main.png
toc : false
---

![](/images/pandas_gpu/main.png)

Data manipulation is a breeze with pandas, and it has become such a standard for it that a lot of parallelization libraries like Rapids and Dask are being created in line with Pandas syntax.

Sometimes back, I wrote about the [subset](https://towardsdatascience.com/minimal-pandas-subset-for-data-scientists-6355059629ae) of Pandas functionality I end up using often. ***In this post, I will talk about handling most of those data manipulation cases in Python on a GPU using cuDF.***

With a sprinkling of some recommendations throughout.

***PS: ***for benchmarking, all the experiments below are done on a Machine with 128 GB RAM and a Titan RTX GPU with 24 GB RAM.

## What is Rapids CuDF, and why to use it?
> Built based on the [Apache Arrow](http://arrow.apache.org/) columnar memory format, cuDF is a GPU DataFrame library for loading, joining, aggregating, filtering, and otherwise manipulating data.

Simply, Rapids CuDF is a library that aims to bring pandas functionality to GPU. Apart from CuDF, Rapids also provides access to cuML and cuGraph as well, which are used to work with Machine Learning algorithms and [graphs on GPU](https://towardsdatascience.com/4-graph-algorithms-on-steroids-for-data-scientists-with-cugraph-43d784de8d0e), respectively.

Now, what is the advantage of this?

A typical GPU has over 2000 CUDA cores. Pandas, when parallelized using Dask or multiprocessing, can use eight cores or 16 CPU cores that your machine has. Now, these CPU cores are different in their power, but the CUDA cores can do easy calculations fast and thus can provide us with significant speedups.

My GPU Titan RTX has around 4600 cores. That means I should be able to parallelize my computations using GPU.

But the problem is that writing code to run for GPU is hard. And Rapids CuDF solves this problem.

Before we go any further, here is a simple example of how cuDF could help you. Here I try to get means of all columns in my random data frame having 100 million rows and five columns.

![](/images/pandas_gpu/0.png)

***That is a ~350x speedup using cuDF!!! And the code remains essentially the same. And remember, I am using a system with 128 GB RAM.***

## Installation — RAPIDS cuDF

So now we are convinced that cuDF is beneficial, the simplest way to install RAPIDS is by just going to the [site](https://rapids.ai/start.html) and check what you need using the release selector tool.

![](/images/pandas_gpu/1.png)

For me, the installation command was:

    conda install -c rapidsai -c nvidia -c conda-forge -c defaults rapids=0.11 python=3.7 cudatoolkit=10.1

For starting up or learning, you could also get started with the Google Colab notebook, which comes pre-installed with the required RAPIDS environment.

I will use the [US Accidents dataset](https://www.kaggle.com/sobhanmoosavi/us-accidents) in this post to show the capability of CuDF Dataframes.

## Reading Data with CuDF

The first thing we do is reading the data source. We can read data in cudf from the local file system

    import cudf
    gdf = cudf.read_csv('US_Accidents_May19.csv')

This command took around 1 second compared to 13 seconds when I read using pd.read_csv function

![](/images/pandas_gpu/2.png)

We could also have read from pandas Dataframes using:

    pdf = pd.read_csv('US_Accidents_May19.csv')
    gdf = cudf.DataFrame.from_pandas(pdf)

![](/images/pandas_gpu/3.png)

On that note, we can reconvert a cuDF dataframe back to a Pandas Dataframe to take advantage of the much more mature Pandas ecosystem whenever needed.

    pdf = gdf.to_pandas()

## Data Snapshot

Always useful to see some of the data. First, let us try the simple Head and Tail commands:

You can use simple head and tail commands with an option to specify the number of rows.

    # top 5 rows
    gdf.head()

    # top 50 rows
    gdf.head(50)

    # last 5 rows
    gdf.tail()

    # last 50 rows
    gdf.tail(50)

You can also see simple dataframe statistics with the following commands.

    # To get statistics of numerical columns
    gdf.describe()

![](/images/pandas_gpu/4.png)

You can also use normal functions like:

    print(gdf['TMC'].mean())

    # no of rows in dataframe
    print(len(gdf))

    # Shape of Dataframe
    print(gdf.shape)

    ---------------------------------------------------------------
    207.35274265463238
    2243939
    (2243939, 49)

***Recommendation: ***Generally working with Jupyter notebook,*** I make it a point of having the first few cells in my notebook containing these snapshots*** of the data. This helps me see the structure of the data whenever I want to. If I don’t follow this practice, I notice that I end up repeating the .head() command a lot of times in my code.

## Handling Columns in DataFrames

### a. Selecting a column

As with Pandas, CuDF lets you choose columns in two ways. Using the dot operator like df.Title and using square brackets like df['Title']

I prefer the second version, mostly. Why?

There are a couple of reasons you would be better off with the square bracket version in the longer run.

* If your column name contains spaces, then the dot version won’t work. For example, df.Revenue (Millions) won’t work while df['Revenue (Millions)]’ will.

* It also won’t work if your column name is count or mean or any of the predefined functions.

* Sometimes you might need to create a for loop over your column names in which your column name might be in a variable. In that case, the dot notation will not work. For Example, This works:

    colname = 'height'
    df[colname]

While this doesn’t:

    colname = 'height'
    df.colname

Trust me. Saving a few characters is not worth it.

***Recommendation: Stop using the dot operator***.

### b. Getting Column Names in a list

It also works just like pandas.

    columnnames = cuda_df.columns

### c. Specifying user-defined Column Names:

Sometimes you want to change the column names as per your taste. I don’t like spaces or brackets in my column names, so I change them as such.

<iframe src="https://medium.com/media/84c90c45ab801afbd00d1151fdca1272" frameborder=0></iframe>

### d. Subsetting specific columns:

Sometimes you only need to work with particular columns in a dataframe. e.g., to separate numerical and categorical columns, or remove unnecessary columns. Let’s say in our example, we only need a few columns

    gdf = gdf[['ID', 'Source', 'TMC', 'Severity', 'Start_Time', 'End_Time','Start_Lat', 'Start_Lng', 'End_Lat', 'End_Lng']]

### e. Seeing column types:

Very useful while debugging. If your code throws an error that you cannot add a str and int, you will like to run this command.

    gdf.dtypes

## Apply and Lambda in CuDF

apply and lambda are some of the best things I have learned to use with pandas. I use apply and lambda anytime I get stuck while building a complex logic for a new column or filter. Let's see if we can use them in CuDF also.

### a. Creating a Column

You can create a new column in many ways.

If you want a column that is a sum or difference of columns, you can pretty much use simple basic arithmetic.

    gdf['Somecol'] = (gdf['TMC'] + gdf['Severity']/10)/2

You can also use simple apply over a series using applymap:

    def somefunc(x):
        return x+2
    gdf['Somecol'] = gdf['TMC'].applymap(somefunc)

But sometimes we may need to build complex logic around the creation of new columns using multiple columns.

To give you an example, let’s say that we want to calculate the Haversine distance based on Lats and Longs.

***How do we do that?***

Whenever I get a hold of such problems, I use apply/lambda. Let me first show you how I will do this with pandas. A lot of the code here is taken from this [post](https://medium.com/rapids-ai/user-defined-functions-in-rapids-cudf-2d7c3fc2728d).

<iframe src="https://medium.com/media/b25b4ff45c66a5b000f200504934fa91" frameborder=0></iframe>

To do the same thing in CuDF, we have to use apply_rows for applying a function to multiple rows.

<iframe src="https://medium.com/media/e07223646e5d537e0d6cb31f278bc219" frameborder=0></iframe>

See how the structure of the haversine_distance function changes and also how we call it a little bit differently. Note that this function takes hDistance as a parameter, so we even specify the output in the function call.

In the backend, it uses Numba for the calculations.

Now this is all well and good, but it has a few caveats:

* It doesn’t take as input strings, so if you wanted to use a string column, you couldn’t. This is something that CuDF has in its features list.

* Only a few functions supported by CUDA python could be used, and not all python functions. The full list of supported functions is [here](https://numba.pydata.org/numba-doc/dev/cuda/cudapysupported.html).

So why do we use it? In this particular case, it took 48 Seconds for Pandas while only 295ms for CuDF. ***That is a 160x Speedup.***

### b. Filtering a dataframe

Pandas make filtering and subsetting dataframes pretty easy. You can filter and subset dataframes using standard operators and &,|,~ operators. You can do pretty much the same with cuDF.

    # Single condition

    df_dis_gt_2 = gdf[gdf['hDistance']>2]

    # Multiple conditions: AND

    And_df = gdf[(gdf['hDistance']>8) & (gdf['TMC']>200)]

    # Multiple conditions: OR

    Or_df = gdf[(gdf['hDistance']>8) | (gdf['TMC']>200)]

    # Multiple conditions: NOT

    Not_df = gdf[~((gdf['hDistance']>8) | (gdf['TMC']>200))]

Pretty simple stuff.

## Aggregation on Dataframes: groupby

groupby will come up a lot of times whenever you want to aggregate your data. Pandas lets you do this efficiently with the groupby function like:

df.groupby(list of columns to groupby on).aggregate({'colname':func1, 'colname2':func2}).reset_index()

You have to worry about supplying two primary pieces of information.

* List of columns to groupby on, and

* A dictionary of columns and functions you want to apply to those columns

reset_index() is a function that resets the index of a dataframe. I use this function ALWAYS whenever I do a groupby, and you might think of it as a default syntax for groupby operations.

Helpfully the syntax remains the same for cuDF.

    gdf_gby = gdf.groupby(['Traffic_Calming','Sunrise_Sunset']).agg({'TMC':'mean','Severity':'mean'}).reset_index()

![](/images/pandas_gpu/5.png)

***Caveat: ***I tried the function np.mean first, which didn’t work. It provides only elementary functions sum,mean,min and max only.

## Dealing with Multiple DataFrames: Concat and Merge:

### a. Concat

Sometimes we get data from different sources. Or someone comes to you with multiple files with each file having data for a particular year.

***How do we create a single dataframe from these multiple dataframes?***

Here we will create our use case artificially since we have a single file. We are creating two dataframes first using the basic filter operations we already know.

    severity_lt_3 = gdf[gdf['Severity']<3]
    severity_gte_3 = gdf[gdf['Severity']>=3]

Here we start with two dataframes: severity_lt_3 containing info for accidents with a severity less than 3 and severity_gte_3 providing info for accidents with severity greater than or equal to 3. We want to create a single dataframe that includes both sorts of accidents.

    fullseverity = cudf.concat([severity_lt_3,severity_gte_3])

### b. Merge

Most of the data that you will encounter will never come in a single file. One of the files might contain ratings for a particular movie, and another might provide the number of votes for a movie.

In such a case, we have two dataframes that need to be merged so that we can have all the information in a single view.

Here we will create our use case artificially since we have a single file. We are creating two dataframes first using the basic column subset operations we already know.

    accident_times_dataframe = gdf[['ID','Start_Time','End_Time']]
    accident_locations_dataframe = gdf[['ID','Start_Lat','Start_Lng','End_Lat','End_Lng']]

![](/images/pandas_gpu/6.png)

![](/images/pandas_gpu/7.png)

We need to have all this information in a single dataframe. How do we do this? This syntax is also the same as Pandas.

    information_df = cudf.merge(accident_times_dataframe,accident_locations_dataframe,on='ID',how='left')

![](/images/pandas_gpu/8.png)

We provide this merge function with four attributes- 1st DF, 2nd DF, join on which column and the joining criteria:['left','right','inner','outer']

***As far as timing is concerned, we again get a 10x speedup while doing Joins when we use cudf.***

![](/images/pandas_gpu/9.png)

***Recommendation: ***I usually always end up using left join. You will rarely need to join using outer or right. Actually whenever you need to do a right join you actually just really need a left join with the order of dataframes reversed in the merge function.

## Conclusion

***CuDF is a step in the right direction as it provides GPU for Data Processing, which takes up a lot of time in the data science pipeline.***

***Here I tried to talk about some functionality in cuDF I use often. ***There is quite a bit more the folks at NVIDIA are trying to implement, so do take a look at the [documentation](https://docs.rapids.ai/api/cudf/stable/).

***Although some of the pandas’ functionality is not yet implemented, ***that shouldn’t stop us from making use of the functions already implemented for time-critical applications and Kaggle.

I, for myself, switch between cudf and pandas dataframes multiple times in my data preparation notebooks.

It does help a lot whenever I am a little tied up on time.

I hope you found this post useful and worth your time. I tried to make this as simple as possible, but you may always **ask me** or see the documentation for doubts.

The whole code is posted in my [Github Repo](https://github.com/MLWhiz/data_science_blogs/tree/master/cudf), where I keep codes for all my posts. You can find the data at [Kaggle](https://www.kaggle.com/sobhanmoosavi/us-accidents).

Also, if you want to learn more about Python 3, I would like to call out an excellent course on Learn [Intermediate level Python](https://bit.ly/2XshreA) from the University of Michigan. Do check it out.

I am going to be writing more of such posts in the future too. Let me know what you think about them. Follow me up at [**Medium](https://medium.com/@rahul_agarwal)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz).
