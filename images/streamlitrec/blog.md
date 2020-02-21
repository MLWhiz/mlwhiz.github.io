---
title: Share your Projects even more easily with this New Streamlit Feature
date:  2020-02-21
draft: false
url : blog/2020/02/23/streamlitrec/
slug: streamlitrec
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: So, have you ever had a problem with explaining how the app works to the stakeholders/business partners? Having to set up multiple calls with different stakeholders in different countries and explaining the whole process again and again?

thumbnail : /images/streamlitrec/main.png
images :
 - /images/streamlitrec/main.png
toc : false
---

![](/images/streamlitrec/main.png)

Share your Projects even more easily with this New Streamlit Feature

### Record and Share for Data Scientists

A Machine Learning project is never really complete if we don’t have a good way to showcase it.

While in the past, a well-made visualization or a small PPT used to be enough for showcasing a data science project, with the advent of dashboarding tools like RShiny and Dash, a good data scientist needs to have a fair bit of knowledge of web frameworks to get along.

As Sten Sootla says in his [satire piece](https://towardsdatascience.com/how-to-fake-being-a-good-programmer-cbef2c39764c) which I thoroughly enjoyed:
> # The secret: it’s not what you know, it’s what you show.

This is where StreamLit comes in and provides a way to create web apps just using Python. I have been keeping close tabs on this excellent product for the past few months. In my last few posts, I talked about [Working with Streamlit](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582) and how to [Deploy the streamlit app using ec2](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3). I have also been in constant touch with the Streamlit team while they have been working continuously to make the user experience even better by releasing additional features.

***So, have you ever had a problem with explaining how the app works to the stakeholders/business partners? Having to set up multiple calls with different stakeholders in different countries and explaining the whole process again and again?***

***Or have you worked on a project that you want to share on social media? LinkedIn, Youtube, and the like?***

With their new version, Streamlit has released a new feature called “***Record a Screencast***” which will solve this problem for you.

How? Read on.

## Setting up

So to check this new feature out, which is a part of Streamlit’s version 0.55.0 offering, we need to first install or upgrade streamlit. Do this by using this command:

    pip install --upgrade streamlit

We also need to run Streamlit. Here I will use the demo app. You can also use any of your [own apps](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582).

    streamlit hello

You should see something like below:

![](/images/streamlitrec/0.png)

A tab also opens up in your browser, where you can try their demo. If that doesn’t open up in the browser, you can manually go to the Local URL [http://localhost:8501/](http://localhost:8501/) too.

![](/images/streamlitrec/1.png)

## Recording the Screencast

Now the time has come to record our screencast to share with the world. You can find the option to record the screencast using the top-right menu in Streamlit.

![](/images/streamlitrec/2.png)

Once you click on that, you will get the option to record audio, and you can select the aptly named “Start Recording” button to start recording.

![](/images/streamlitrec/3.png)

You can then choose what you want to share — just your streamlit app or your entire desktop. ***One can choose to share the whole desktop if they need to go forth between different programs like Excel sheets, powerpoints, and the streamlit app, for example.*** Here I choose to show just the “Streamlit” App and click share.

![](/images/streamlitrec/4.png)

Your screencast has now started, and you can record the explanation session for your shareholders now. Once you are done with the recording, you can click on the top-right menu again and select stop recording. Or conveniently press escape to end the recording session.

![](/images/streamlitrec/5.png)

You will be able to preview and **save the session video **you recorded as a .webm file, which you can aim to send to your shareholders and even share on LinkedIn/twitter/youtube for your personal projects.

![](/images/streamlitrec/6.png)

And that’s it. The process is pretty simple and doesn’t need any additional software installation from our side.

## Endnotes

Streamlit has democratized the whole process of creating apps.

I honestly like the way Streamlit is working on developing its product, keeping in mind all the pain points of its users. With this iteration, they have resolved one more pain point where users struggle to showcase their work in a meaningful way on social media sites or to explain the workings of an app multiple times to the shareholders.

**On top of that, Streamlit is a free and open-source rather than a proprietary web app that works out of the box. **I couldn’t recommend it more.

***Also, do let me know if you want to request any additional features in Streamlit in the comments section***. I will make sure to pass it on to the Streamlit team.

If you want to learn more about using Streamlit to create and deploy apps, take a look at my other posts:
[**How to write Web apps using simple Python for Data Scientists?**
*Convert your Data Science Projects into cool apps easily without knowing any web frameworks*towardsdatascience.com](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582)
[**How to Deploy a Streamlit App using an Amazon Free ec2 instance?**
*Data Apps on the web in 10 minutes*towardsdatascience.com](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3)

If you want to learn about the best strategies for creating Visualizations, I would like to call out an excellent course about [**Data Visualization and applied plotting](https://www.coursera.org/specializations/data-science-python?ranMID=40328&ranEAID=lVarvwc5BD0&ranSiteID=lVarvwc5BD0-SAQTYQNKSERwaOgd07RrHg&siteID=lVarvwc5BD0-SAQTYQNKSERwaOgd07RrHg&utm_content=3&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0)** from the University of Michigan, which is a part of a pretty good [**Data Science Specialization with Python](https://www.coursera.org/specializations/data-science-python?ranMID=40328&ranEAID=lVarvwc5BD0&ranSiteID=lVarvwc5BD0-SAQTYQNKSERwaOgd07RrHg&siteID=lVarvwc5BD0-SAQTYQNKSERwaOgd07RrHg&utm_content=3&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0)** in itself. Do check it out.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
