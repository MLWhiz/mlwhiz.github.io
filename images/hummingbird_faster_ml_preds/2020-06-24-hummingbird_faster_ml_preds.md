
---
title:  How to run your ML model Predictions 50 times faster?
date:  2020-06-24
draft: false
url : blog/2020/06/06/hummingbird_faster_ml_preds/
slug: hummingbird_faster_ml_preds
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: 

thumbnail : /images/hummingbird_faster_ml_preds/main.png
images :
 - /images/hummingbird_faster_ml_preds/main.png
toc : false
---

![](/images/hummingbird_faster_ml_preds/main.png)


With the advent of so many computing and serving frameworks, it is getting stressful day by day for the developers to put a model into [production](https://towardsdatascience.com/take-your-machine-learning-models-to-production-with-these-5-simple-steps-35aa55e3a43c). If the question of what model performs best on my data was not enough, now the question is what framework to choose for serving a model trained with Sklearn or LightGBM or [PyTorch](https://towardsdatascience.com/moving-from-keras-to-pytorch-f0d4fff4ce79). And new frameworks are being added as each day passes.

So is it imperative for a [Data Scientist](https://towardsdatascience.com/top-10-resources-to-become-a-data-scientist-in-2020-99a315194701) to learn a different framework because a Data Engineer is comfortable with that, or conversely, does a Data Engineer need to learn a new platform that the Data Scientist favors?

Add to that the factor of speed and [performance](https://towardsdatascience.com/faster-and-memory-efficient-pytorch-models-using-amp-50fd3c8dd7fe) that these various frameworks offer, and the question suddenly becomes even more complicated.

So, I was pleasantly surprised when I came across the [Hummingbird](https://github.com/microsoft/hummingbird) project on Github recently, which aims to answer this question or at least takes a positive step in the right direction.

---
## So, What is HummingBird?

![](/images/hummingbird_faster_ml_preds/0.png)

*As per their documentation:*
> *Hummingbird* is a library for compiling trained traditional ML models into tensor computations. *Hummingbird* allows users to seamlessly leverage neural network frameworks (such as [PyTorch](https://pytorch.org/)) to accelerate traditional ML models.
> Thanks to *Hummingbird*, users can benefit from:
> (1) all the current and future optimizations implemented in neural network frameworks;
> (2) native hardware acceleration;
> (3) having a unique platform to support both traditional and neural network models, and have all of this
> (4) without having to re-engineer their models.

Put even more simply; you can now convert your models written in Scikit-learn or [Xgboost](https://towardsdatascience.com/lightning-fast-xgboost-on-multiple-gpus-32710815c7c3) or LightGBM into PyTorch models and gain the performance benefits of Pytorch while inferencing.

*As of right now, Here is the list of [*operators](https://github.com/microsoft/hummingbird/wiki/Supported-Operators) Hummingbird supports with more on the way.

---
## A Simple Example

We can start by installing Hummingbird, which is as simple as:

    pip install hummingbird-ml

To use hummingbird, I will begin with a minimal example on a small random [classification](https://towardsdatascience.com/the-5-classification-evaluation-metrics-you-must-know-aa97784ff226) Dataset. We start by creating a sample dataset with 100,000 rows and using a RandomForestClassifier on top of that.

    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from hummingbird.ml import convert

    # Create some random data for binary classification
    from sklearn import datasets

    X, y = datasets.make_classification(n_samples=100000, n_features=28)

    # Create and train a model (scikit-learn RandomForestClassifier in this case)

    skl_model = RandomForestClassifier(n_estimators=1000, max_depth=10)
    skl_model.fit(X, y)

What hummingbird helps us with is to convert this sklearn model into a PyTorch model by just using the simple command:

    # Using Hummingbird to convert the model to PyTorch
    model = convert(skl_model, 'pytorch')
    print(type(model))
    --------------------------------------------------------
    hummingbird.ml._container.PyTorchBackendModel

We can now load our new Pytorch model to GPU using:

    model.to('cuda')

This is great. So, we can convert from sklearn model to a PyTorch model, which should run faster on a GPU. But by how much?

Let us see a simple performance comparison.

---
## Comparison

### 1. Batch Mode

We will start by using the sklearn model to predict the whole train dataset and check out the time it takes.

![](/images/hummingbird_faster_ml_preds/1.png)

We can do the same with our new PyTorch model:

![](/images/hummingbird_faster_ml_preds/2.png)

That is a speedup of 9580/195 ~ 50x.

### 2. Single Example Prediction

We predict a single example here to see how the model would perform in a real-time setting. The sklearn model:

![](/images/hummingbird_faster_ml_preds/3.png)

vs. Pytorch model

![](/images/hummingbird_faster_ml_preds/4.png)

That is again a speedup of 79.6/1.6 ~50x.

---
## Small Caveat

A small caveat I experienced is that the predictions from the sklearn model and the hummingbird PyTorch model were not exactly the same.

For example, here are the predictions I got from both models:

![](/images/hummingbird_faster_ml_preds/5.png)

Yes, sometimes, they differ in the 7th digit, which might be a function of the conversion process. I think that it won’t change the final 1 or 0 predictions much. We can also check that:

    scikit_1_0 = scikit_preds[:,1]>0.5 
    hb_1_0 = hb_preds[:,1]>0.5 
    print(len(scikit_1_0) == sum(scikit_1_0==hb_1_0))
    ------------------------------------------------------------
    True

So, for this case, both the models exactly gave the same 1 or 0 predictions for the whole dataset of 100,000 rows.

So I guess it is okay.

---
## Conclusion

The developers at Microsoft are still working on adding many more operators which range from models to feature engineering like MinMaxScaler or LabelEncoder to the code, and I am hopeful that they will further develop and improve this project. Here is the [roadmap](https://github.com/microsoft/hummingbird/wiki/Roadmap-for-Upcoming-Features-and-Support) to development if you are interested.

Although Hummingbird is not perfect yet, it is the first system able to run classical ML inference DNN frameworks and proves them mature enough to be used as generic compilers. I will try to include it in my development workflow when it comes to making predictions at high throughput or latency.

You can find the code for this post as well as all my posts at my [GitHub](https://github.com/MLWhiz/data_science_blogs/tree/master/hummingbird) repository.

### Continue Learning

If you want to learn more about building and putting a Machine Learning model in production, this [course on AWS](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.14884356434&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Faws-machine-learning) for implementing Machine Learning applications promises just that.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------) or Subscribe to my [blog](http://eepurl.com/dbQnuX?source=post_page---------------------------) to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
