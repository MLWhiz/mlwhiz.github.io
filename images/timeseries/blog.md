
# Using Gradient Boosting for Time Series prediction tasks

Using Gradient Boosting for Time Series prediction tasks

### Easy Time series modelling

Time series prediction problems are pretty frequent in the retail domain.

Companies like Walmart and Target need to keep track of how much product should be shipped from Distribution Centres to stores. Even a small improvement in such a demand forecasting system can help save a lot of dollars in term of workforce management, inventory cost and out of stock loss.

While there are many techniques to solve this particular problem like ARIMA, Prophet, and LSTMs, we can also treat such a problem as a regression problem too and use trees to solve it.

***In this post, we will try to solve the time series problem using XGBoost.***

***The main things I am going to focus on are the sort of features such a setup takes and how to create such features.***

## Dataset

![](/images/timeseries/0.png)

Kaggle master Kazanova along with some of his friends released a [“How to win a data science competition”](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-BShznKdc3CUauhfsM7_8xw&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0) Coursera course. The Course involved a final project which itself was a time series prediction problem.

In this competition, we are given a challenging time-series dataset consisting of daily sales data, provided by one of the largest Russian software firms — 1C Company.

We have to predict total sales for every product and store in the next month.

Here is how the data looks like:

![](/images/timeseries/1.png)

We are given the data at a daily level, and we want to build a model which predicts total sales for every product and store in the next month.

The variable date_block_num is a consecutive month number, used for convenience. January 2013 is 0, and October 2015 is 33. You can think of it as a proxy to month variable. I think all the other variables are self-explanatory.

***So how do we approach this sort of a problem?***

## Data Preparation

The main thing that I noticed is that the data preparation and [feature generation](https://towardsdatascience.com/the-hitchhikers-guide-to-feature-extraction-b4c157e96631) aspect is by far the most important thing when we attempt to solve the time series problem using regression.

### 1. Do Basic EDA and remove outliers

    sales = sales[sales['item_price']<100000]
    sales = sales[sales['item_cnt_day']<=1000]

### 2. Group data at a level you want your predictions to be:

We start with creating a dataframe of distinct date_block_num, store and item combinations.

This is important because in the months we don’t have a data for an item store combination, the machine learning algorithm needs to be told explicitly that the sales are zero.

<iframe src="https://medium.com/media/282feb03d18eabc2ba919b3c28ef8e1d" frameborder=0></iframe>

![](/images/timeseries/2.png)

The grid dataFrame contains all the shop, items and month combinations.

We then merge the Grid with Sales to get the monthly sales DataFrame. We also replace all the NA’s with zero for months that didn’t have any sales.

<iframe src="https://medium.com/media/6e8c7e543bdc74225658e124f8ef32c9" frameborder=0></iframe>

![](/images/timeseries/3.png)

### 3. Create Target Encodings

To create target encodings, we group by a particular column and take the mean/min/sum etc. of the target column on it. These features are the first features we create in our model.

***Please note that these features may induce a lot of leakage/overfitting in our system and thus we don’t use them directly in our models. We will use the lag based version of these features in our models which we will create next.***

<iframe src="https://medium.com/media/9ed2f9328f647df1a166e2a2a1ed4d9c" frameborder=0></iframe>

We group by item_id, shop_id, and item_category_id and aggregate on the item_price and item_cnt_day column to create the following new features:

![We create the highlighted target encodings](/images/timeseries/4.png)*We create the highlighted target encodings*

We could also have used [featuretools](https://towardsdatascience.com/the-hitchhikers-guide-to-feature-extraction-b4c157e96631) for this. **Featuretools** is a framework to perform automated feature engineering. It excels at transforming temporal and relational datasets into feature matrices for machine learning.

### 4. Create Lag Features

The next set of features our model needs are the lag based Features.

When we create regular classification models, we treat training examples as fairly independent of each other. But in case of time series problems, at any point in time, the model needs information on what happened in the past.

We can’t do this for all the past days, but we can provide the models with the most recent information nonetheless using our target encoded features.

<iframe src="https://medium.com/media/f26df80b41e4ae7e6a4a64dfc66f1326" frameborder=0></iframe>

So we aim to add past information for a few features in our data. We do it for all the new features we created and the item_cnt_day feature.

We fill the NA’s with zeros once we have the lag features.

<iframe src="https://medium.com/media/1056a71ff3b5f40549bd2e3df049f5db" frameborder=0></iframe>

We end up creating a lot of lag features with different lags:

    'item_id_avg_item_price_lag_1','item_id_sum_item_cnt_day_lag_1', 'item_id_avg_item_cnt_day_lag_1','shop_id_avg_item_price_lag_1', 'shop_id_sum_item_cnt_day_lag_1','shop_id_avg_item_cnt_day_lag_1','item_category_id_avg_item_price_lag_1','item_category_id_sum_item_cnt_day_lag_1','item_category_id_avg_item_cnt_day_lag_1', 'item_cnt_day_lag_1',

    'item_id_avg_item_price_lag_2', 'item_id_sum_item_cnt_day_lag_2','item_id_avg_item_cnt_day_lag_2', 'shop_id_avg_item_price_lag_2','shop_id_sum_item_cnt_day_lag_2', 'shop_id_avg_item_cnt_day_lag_2','item_category_id_avg_item_price_lag_2','item_category_id_sum_item_cnt_day_lag_2','item_category_id_avg_item_cnt_day_lag_2', 'item_cnt_day_lag_2',

    ...

## Modelling

### 1. Drop the unrequired columns

As previously said, we are going to drop the target encoded features as they might induce a lot of overfitting in the model. We also lose the item_name and item_price feature.

<iframe src="https://medium.com/media/901a4c232f6c028ca99a03b7659487a4" frameborder=0></iframe>

### 2. Take a recent bit of data only

When we created the lag variables, we induced a lot of zeroes in the system. We used the maximum lag as 12. To counter that we remove the first 12 months indexes.

    sales_means = sales_means[sales_means['date_block_num']>11]

### 3. Train and CV Split

When we do a time series split, we usually don’t take a cross-sectional split as the data is time-dependent. We want to create a model that sees till now and can predict the next month well.

    X_train = sales_means[sales_means['date_block_num']<33]
    X_cv =  sales_means[sales_means['date_block_num']==33]

    Y_train = X_train['item_cnt_day']
    Y_cv = X_cv['item_cnt_day']

    del X_train['item_cnt_day']
    del X_cv['item_cnt_day']

### 4. Create Baseline

![](/images/timeseries/5.png)

Before we proceed with modelling steps, lets check the RMSE of a naive model, as we want to [have an RMSE to compare](https://towardsdatascience.com/take-your-machine-learning-models-to-production-with-these-5-simple-steps-35aa55e3a43c) to. We assume that we are going to predict the last month sales as current month sale for our baseline model. We can quantify the performance of our model using this baseline RMSE.

<iframe src="https://medium.com/media/49573a50eb8ec9ffb10dabebc184ac95" frameborder=0></iframe>

    1.1358170090812756

### 5. Train XGB

We use the XGBRegressor object from the xgboost scikit API to build our model. Parameters are taken from this [kaggle kernel](https://www.kaggle.com/dlarionov/feature-engineering-xgboost). If you have time, you can use hyperopt to [automatically find out the hyperparameters](https://towardsdatascience.com/automate-hyperparameter-tuning-for-your-models-71b18f819604) yourself.

    from xgboost import XGBRegressor

    model = XGBRegressor(
        max_depth=8,
        n_estimators=1000,
        min_child_weight=300, 
        colsample_bytree=0.8, 
        subsample=0.8, 
        eta=0.3,    
        seed=42)

    model.fit(
        X_train, 
        Y_train, 
        eval_metric="rmse", 
        eval_set=[(X_train, Y_train), (X_cv, Y_cv)], 
        verbose=True, 
        early_stopping_rounds = 10)

![](/images/timeseries/6.png)

After running this, we can see RMSE in ranges of ***0.93*** on the CV set. And that is pretty impressive based on our baseline validation RMSE of ***1.13***. And so we work on deploying this model as part of our [continuous integration](https://towardsdatascience.com/take-your-machine-learning-models-to-production-with-these-5-simple-steps-35aa55e3a43c) effort.

### 5. Plot Feature Importance

We can also see the important features that come from XGB.

<iframe src="https://medium.com/media/63b356731dc5edc00912f282399c37ed" frameborder=0></iframe>

![Feature importances](/images/timeseries/7.png)*Feature importances*

## Conclusion

In this post, we talked about how we can use trees for even time series modelling. The purpose was not to get perfect scores on the kaggle leaderboard but to gain an understanding of how such models work.

![](/images/timeseries/8.png)

When I took part in this competition as part of the [course](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-BShznKdc3CUauhfsM7_8xw&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0), a couple of years back, using trees I reached near the top of the leaderboard.

Over time people have worked a lot on tweaking the model, hyperparameter tuning and creating even more informative features. But the basic approach has remained the same.

You can find the whole running code on [GitHub](https://github.com/MLWhiz/time_series_xgb).

Take a look at the [How to Win a Data Science Competition: Learn from Top Kagglers](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0) course in the [Advanced machine learning specialization](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0) by Kazanova. This course talks about a lot of ways to improve your models using feature engineering and hyperparameter tuning.

I am going to be writing more beginner-friendly posts in the future too. Let me know what you think about the series. Follow me up at [**Medium](https://medium.com/@rahul_agarwal)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
