---
title: How to find Feature importances for BlackBox Models?
date:  2019-12-04
draft: false
url : blog/2019/12/04/blackbox/
slug: blackbox
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: this post is explaining how permutation importance works and how we can code it using ELI5

thumbnail : /images/blackbox/main.png
images :
 - /images/blackbox/main.png
toc : false
---

# How to find Feature importances for BlackBox Models?

DS Algorithms

## How to find Feature importances for BlackBox Models?

### Permutation Importance as a feature selection method

Data Science is the study of algorithms.

I grapple through with many algorithms on a day to day basis, so I thought of listing some of the most common and most used algorithms one will end up using in this new [DS Algorithm series](https://towardsdatascience.com/tagged/ds-algorithms).

How many times it has happened when you create a lot of features and then you need to come up with ways to reduce the number of features?

Last time I wrote a post titled “[The 5 Feature Selection Algorithms every Data Scientist should know](https://towardsdatascience.com/the-5-feature-selection-algorithms-every-data-scientist-need-to-know-3a6b566efd2)” in which I talked about using correlation or tree-based methods and adding some structure to the process of feature selection.

Recently I got introduced to another novel way of feature selection called ***Permutation Importance*** and really liked it.

***So, this post is explaining how permutation importance works and how we can code it using ELI5.***

## What is Permutation Importance?

Simply speaking, we can attribute importance to a feature based on how our evaluation metric(F1, Accuracy AUC, etc.) changes if we remove a particular feature from our dataset.

It could be pretty straightforward — We remove a feature from our dataset and train the classifier and see how the evaluation metric changes. And we do it for all features.

So we fit our model at least n times, where n is the number of features in the model. It is so much work and computation. ***Can we do better?***

![[Source](https://www.kaggle.com/dansbecker/permutation-importance): We permute a feature and predict using the updated dataset. Intuitively, if our accuracy or any evaluation metric doesn’t take a hit, we can say that the feature is not important. If our accuracy does take a hit, we consider this feature important.](/images/blackbox/0.png)*[Source](https://www.kaggle.com/dansbecker/permutation-importance): We permute a feature and predict using the updated dataset. Intuitively, if our accuracy or any evaluation metric doesn’t take a hit, we can say that the feature is not important. If our accuracy does take a hit, we consider this feature important.*

Yes, we can. To calculate permutation importance, we shuffle/permute the values for a single feature and make predictions using the resulting dataset.

The predictions are then used to calculate our evaluation metric. Intuitively, if our accuracy or any evaluation metric doesn’t take a hit, we can say that the feature is not important. If our accuracy does take a hit, we consider this feature important.

## Data

We will try to do this using a dataset to understand it better.

I am going to be using a football player dataset and try to find out the most important features using it.

![](/images/blackbox/1.png)

*Don’t worry if you don’t understand football terminologies. I will try to keep it at a minimum.*

You can see the full code here in this [Kaggle Kernel](https://www.kaggle.com/mlwhiz/permutation-feature-selection-using-football-data).

### Some simple Data Preprocessing

We have done some basic preprocessing such as removing nulls and one hot encoding. We also convert the problem to a classification problem using:

    y = traindf['Overall']>=80

Here we use High Overall as a proxy for a great player. Our dataset(X) looks like below and has 223 columns.

![train Data X](/images/blackbox/2.png)*train Data X*

## Implementation

### 1. For sklearn Models

ELI5 library makes it quite easy for us to use permutation importance for sklearn models. First, we train our model.

    from sklearn.ensemble import RandomForestClassifier
    my_model = RandomForestClassifier(n_estimators=100,
                                      random_state=0).fit(X, y)

Then we use the function PermutationImportance from the eli5.sklearn module.

    from eli5.sklearn import PermutationImportance
    import eli5
    perm = PermutationImportance(my_model,n_iter=2).fit(X, y)
    eli5.show_weights(perm, feature_names = X.columns.tolist())

The results look like:

![](/images/blackbox/3.png)

Here we note that Reactions, Interceptions and BallControl are the most important features to access a player’s quality.

### 2. For BlackBox Models or Non-sklearn models

![](/images/blackbox/4.png)

We can also use eli5 to calculate feature importance for non scikit-learn models also. Here we train a LightGBM model.

    import numpy as np

    from lightgbm import LGBMClassifier

    lgbc=LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=32, colsample_bytree=0.2,
                reg_alpha=3, reg_lambda=1, min_split_gain=0.01, min_child_weight=40)

    lgbc.fit(X,y)

We will need to create a wrapper for our score function to calculate our evaluation metric.

    from sklearn.metrics import accuracy_score

    #define a score function. In this case I use accuracy
    def score(X, y):
        y_pred = lgbc.predict(X)
        return accuracy_score(y, y_pred)

We can now use get_score_importances function from eli5.permutation_importance to get the final feature importances.

    from eli5.permutation_importance import get_score_importances

    # This function takes only numpy arrays as inputs
    base_score, score_decreases = get_score_importances(score, np.array(X), y)

    feature_importances = np.mean(score_decreases, axis=0)

We can see the top 5 features using:

    feature_importance_dict = {}
    for i, feature_name in enumerate(X.columns):
        feature_importance_dict[feature_name]=feature_importances[i]

    print(dict(sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)[:5]))

    ---------------------------------------------------------------
    {'Reactions': 0.019626631422435127,
     'Interceptions': 0.004075114268406832,
     'BallControl': 0.0025001376727793235,
     'ShortPassing': 0.0012996310369513431,
     'Strength': 0.0009251610771518149}

## Conclusion

[Feature engineering](https://towardsdatascience.com/the-hitchhikers-guide-to-feature-extraction-b4c157e96631) and feature selection are critical parts of any machine learning pipeline.

We strive for accuracy in our models, and one cannot get to a good accuracy without revisiting these pieces again and again.

In this post, I tried to explain Permutation importance as a feature selection method. It helps us find feature importance for any BlackBox model, unlike the techniques in my previous [post](https://towardsdatascience.com/the-5-feature-selection-algorithms-every-data-scientist-need-to-know-3a6b566efd2) on feature selection.

If you want to learn more about feature engineering/selection, I would like to call out the [How to Win a Data Science Competition: Learn from Top Kagglers](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0) course in the [Advanced machine learning specialization](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0) by Kazanova. This course talks about a lot of intuitive ways to improve your model using useful feature engineering/selection techniques. Definitely recommended.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------).
