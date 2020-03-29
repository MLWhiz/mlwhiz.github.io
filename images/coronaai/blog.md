---
title: Can AI help in fighting against Corona?
date:  2020-03-25
draft: false
url : blog/2020/03/24/coronaai/
slug: coronaai
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: This post is going to be about Multiple ways to create a new column in Pyspark Dataframe

thumbnail : /images/coronaai/main.png
images :
 - /images/coronaai/main.png
toc : false
---

# 

Can AI help in fighting against Corona?

### A call to action for fellow data professionals in this dire time

Feeling Helpless? I know I am.

With the whole shutdown situation, what I thought was once a paradise for my introvert self doesn’t look so good when it is actually happening.

I really cannot fathom being at home much longer. And this feeling of helplessness at not being able to do anything doesn’t help.

Honestly, I would like to help with so much more in this dire situation, but here are some small ideas around which we as AI practitioners and Data Scientists can be of use.

## Donate your Computing Power

NVIDIA is asking Gamers to donate their computing power to support folding@home.

<iframe src="https://medium.com/media/f3f42595af32b5099323c1b79811121e" frameborder=0></iframe>

I would say that*** we data scientists surely have the infrastructure at hand to help in this regard.***

And we can do pretty much with a few clicks. It sort of feels like instant gratification, but it still is better than doing nothing.

You just need to download and install their software [here](https://foldingathome.org/alternative-downloads/). I downloaded the [fah-installer_7.5.1_x86.exe](https://download.foldingathome.org/releases/public/release/fah-installer/windows-10-32bit/v7.5/fah-installer_7.5.1_x86.exe) file for my windows system. You can download it for MAC and Linux too. And you can help with CPU resources also if you don’t have GPUs.

When asked for “Custom Install” or “Express Install”, I went for the recommended option that is “Express Install”. You may want to give Team “PC Master Race — PCMR” number 225605. You can leave the passkey empty or you can get a passkey if you want to keep track of work done by you.

![](/images/coronaai/0.png)

You can also control the system resources donated to the cause. I recommend using full if you are not using any considerable compute. I am donating my two GPUs along with CPU. Till now I have been able to donate around 3 work units.

![](/images/coronaai/1.png)

## Come up with Novel Approaches to help

One thing that is causing a lot of concern is the lack of proper testing procedures. In the UK, for instance, the current advisory is to self isolate at minor symptoms of cold due to a shortage of tests. Also, due to this shortage of tests, a lot of numbers are not entirely reliable and may be false.

![[Source](https://www.pyimagesearch.com/2020/03/16/detecting-covid-19-in-x-ray-images-with-keras-tensorflow-and-deep-learning/)](/images/coronaai/2.png)*[Source](https://www.pyimagesearch.com/2020/03/16/detecting-covid-19-in-x-ray-images-with-keras-tensorflow-and-deep-learning/)*

So I was just pleasantly surprised when I saw the blog from Adrian Rosebrock, where he tried to create an automatic COVID-19 detector using the COVID-19 X-ray [image dataset](https://github.com/ieee8023/covid-chestxray-dataset) (curated by [**Dr. Joseph Cohen](https://josephpcohen.com/w/)) **along with normal X-Ray Images from the [**Kaggle’s Chest X-Ray Images (Pneumonia) dataset](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia)**.

As for the [results](https://www.pyimagesearch.com/2020/03/16/detecting-covid-19-in-x-ray-images-with-keras-tensorflow-and-deep-learning/), they seem promising:
> As you can see from the results above, our automatic COVID-19 detector is obtaining ~90–92% accuracy on our sample dataset based solely on X-ray images — no other data, including geographical location, population density, etc. was used to train this model. We are also obtaining 100% sensitivity and 80% specificity

These results are awesome. A 100% sensitivity means to be able to capture all the Positives. And it could be used as a preliminary test for Corona.But, I am not sure at what stage these X-rays were taken as that will also play a major role. You can check out the detailed post on [pyimagesearch](https://www.pyimagesearch.com/2020/03/16/detecting-covid-19-in-x-ray-images-with-keras-tensorflow-and-deep-learning/). A caveat ***he mentions is the lack of data,*** which is quite understandable at this point in time. But if this approach works and is worked upon with other variables at hand, it might help to detect corona.
> # Can we come up with other novel ways of helping those in need?

## Spread Awareness and Mitigate Rumors through data

One good thing about working with data is that we get in the habit of understanding various biases. Another essential thing that a lot of fellow data scientists have been doing is creating awareness and calling out different biases.

I particularly liked this [post, ](https://www.fast.ai/2020/03/09/coronavirus/)which provides a data science perspective on Coronavirus by fast.ai founder *Jeremy Howard and Rachel Thomas.*

Also, read up on this post by [Cassie Kozyrkov](undefined), which talks about the various biases around Corona and tries to take a hypothesis testing approach to the whole situation. I particularly liked this part in her post:
> If no relevant information comes in, keep doing what you were planning to do. When a different action is triggered, do it.
[**Smarter COVID-19 Decision-Making**
*How to apply sound principles from decision science to the pandemic*towardsdatascience.com](https://towardsdatascience.com/smarter-covid-19-decision-making-39dbff2ab2ba)

## It’s not enough, but …

I understand that it is still not enough and honestly very less.

A lot needs to be done on the ground to tackle this whole situation. But these are a few things that come to my mind apart from washing our hands.

Also, we can discuss any ideas in which the data science community can help to tackle this enormous challenge. I would like to do so much more.
