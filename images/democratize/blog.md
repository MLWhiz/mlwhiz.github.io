---
title: Don’t Democratize Data Science
date:  2020-05-25
draft: false
url : blog/2020/05/25/democratize/
slug: democratize
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: In this piece, I want to briefly look at some of these problems and the adverse effect they could have on the field

thumbnail : /images/democratize/main.png
images :
 - /images/democratize/main.png
toc : false
---

![](/images/democratize/main.png)

Every few years, some academic and professional field gets a lot of cachet in the popular imagination. Right now, that field is data science. As a result, a lot of people are looking to get into it. Add to that the news outlets calling data science sexy and various academic institutes promising to make a data scientist out of you in just a few months, and you’ve got the perfect recipe for disaster.

Of course, as a data scientist myself, I don’t think the problem lies in people choosing data science as a profession. If you’re interested in working with data, understanding business problems, grappling with math, and you love coding, you’re probably going to thrive in data science. You’ll get a lot of opportunities to use math and coding to develop innovative solutions to problems and will likely find the work rewarding. The main issue here is that the motivations people have for entering the field are often flawed.

For some, the appeal is money, while others like the way the title sounds. Even worse, some people are probably just responding to the herd mentality that our society has instilled. For instance, not long ago, every graduate aspired to do an MBA. And I myself am guilty of the same. It took me a GMAT test and a couple of rejections to realize that I didn’t really want the degree. Ultimately, those rejections were the best thing that happened to me because, after that, I finally looked at data science as an option. Once I got into it, I found that I love the math involved and all the different ways in which I get to use data science to help solve problems for businesses.
> # Today, I see that data science has somehow acquired the same stature that the MBA once had.

A lot of people want to do it, but they don’t know what the job really entails. And this has resulted in a lot of people calling themselves data scientists and a lot of bad decision making. In fact, a lot of people considering entering the profession probably don’t even know what data science is.

Today, the whole field has been democratized by the availability of so much material. A plethora of MOOCs from the best instructors cover concepts from basic to advanced, and you can easily find packages that let you create models with just a few lines of code.

I genuinely love the fact that there are so many resources to learn and practice data science. But this democratization has created a few problems of its own. ***In this piece, I want to briefly look at some of these problems and the adverse effect they could have on the field.***

## Automated Data Science?

A lot of AutoML packages aim at democratizing data science. They provide a repository of models, automate the hyperparameter tuning process, and sometimes offer a way to put these models into production. The availability of such packages has led a lot of people to think that data science could be fully automated, eliminating the need for data scientists altogether. Or, if the processes can’t be automated, these tools will allow anyone to become a data scientist.

I sincerely disagree. I have found such codebases useful at times, but they look at data science purely from a coding perspective.
> # ***In my view, data science involves a lot of work apart from modeling.***

The work of data science includes understanding and identifying the problem at hand and setting up the right evaluation metrics. You also have to analyze the profitability of the project: most businesses don’t want to spend money on projects that don’t positively affect the bottom line. You can work with existing data, but sometimes you might need to come up with ways to set up new data pipelines to gather data to solve the problem. This requires talking to the stakeholders and gaining a holistic understanding of the problem. A data scientist also needs to be able to carry out data munging and feature creation to churn more performance out of existing models. In the end, model testing and setting the feedback loop require endless hours of discussions with the business and are pretty specific to each project. Someone who just runs code might not be able to add value to such discussions as they don’t really understand what goes behind the models they have used in AutoML.

Then there comes the issue of domain knowledge. Processes that are acceptable in a retail domain are not applicable in the finance domain where a small change could result in your customers losing a lot of money. Some things just can’t be automated since they require domain knowledge and an understanding of the business you’re working with.
> # More importantly, an automated pipeline can’t be held responsible if a project doesn’t work or if your model fails in production.

A good data scientist will try to figure out ways to sort out production issues as they arise as well as creating a machine learning pipeline specific to the project to mitigate such issues.

## The Code-Runner Mentality

I have become skeptical of what I call the New Data Scientist. Almost every day, I seem to meet a person calling themselves a data scientist when they are just glorified code runners, which refers to a person who just runs the code without understanding what goes on behind it. With so many academies and institutes providing boot-camp-based courses, ***code runners are in abundance right now.***

I get a lot of requests where someone asks me whether they should take a certified course from XYZ institute or a boot camp from ABC academy. My answer is neither. I find that these institutes that promise to make data scientists in droves are mainly just in the money-making business. Ultimately, going through a few notebooks and running somebody else’s code doesn’t truly make a person a data scientist.

Now, don’t get me wrong. If someone learns best through a top-down approach where they run some code first and then read in-depth about the principles behind it, that’s perfectly fine. Data science is about more than just running code, though. Until you really understand the math and theory behind all the code, you haven’t mastered data science.

## The Dunning-Kruger Effect

![[Source](https://commons.wikimedia.org/wiki/File:Dunning%E2%80%93Kruger_Effect_01.svg): Wikipedia Commons](/images/democratize/0.png)*[Source](https://commons.wikimedia.org/wiki/File:Dunning%E2%80%93Kruger_Effect_01.svg): Wikipedia Commons*

The Dunning-Kruger effect is a type of [cognitive bias](https://builtin.com/data-science/cognitive-biases-data-science) in which a person with a little bit of knowledge about some subject overestimates their abilities because they’re unaware of how little they actually know. I see this in action constantly in data science. In fact, it might be more pronounced in this field than any other!

I tend to think of this as a novice effect. It’s a problem that plagues people in the early stages of learning a new skill. In my view, there are three stages to a data scientist’s journey.

* **The Dunning-Kruger Stage — **You created your first model and think you know everything there is to know about data science.

* **The “I Don’t Know Anything” Stage — **You go to a conference or talk to your peers and suddenly realize that there is so much more to learn.

* **The “Lifelong Learning” Stage — **You give in to the fact that there are always going to be some things you won’t know that just got introduced and so there is lifelong learning involved in pursuing data science.

Now, the Dunning-Kruger effect is something that most of the beginners will face. The joy of running your first program and executing it perfectly really takes you to the top of the world. And it’s totally fine to be at this stage. The problem comes when newcomers are incapable of leaving this stage and moving on to the next ones in a timely fashion. I have seen a few people who get stuck at this stage because they got into data science with the wrong expectations, thinking that it’s sexy and exciting, without understanding the field’s depth. ***These types of people tend to think they can just use existing models to solve problems and that they get by without understanding the math.***

For instance, I recently interviewed a guy who had two years of experience in the field. He seemed confident. He had used data science in his job and had worked on a couple of Kaggle projects. The first few minutes of the interview went really well. He explained the higher-level concepts well enough that I decided to dig a little deeper into his mathematical understanding of the techniques he had applied in his projects. And that was where things changed. I asked him to tell me about the log loss function. When he said, *“*But we have packages for doing all this*,*”* *I realized that this guy had never left the first stage.

## Conclusion

The availability of ready-made packages and courses is democratizing the field of data science. But there is just so much more to the job that comes from hands-on experience, communicating with people, and being able to listen to different perspectives.

So, while some people may think of data science as a pure coding job, it’s not just about becoming a coding superstar.

It’s about finding the right problems that are useful for the business and coming up with best ways to solve them. To do that, you need domain knowledge, humility, a little bit of math, and, most importantly, a lifelong desire to learn.

If you want to learn about Data Science, I would like to call out this [***excellent course](https://www.coursera.org/learn/machine-learning?ranMID=40328&ranEAID=lVarvwc5BD0&ranSiteID=lVarvwc5BD0-btd7XBdF681VKxRe2H_Oyg&siteID=lVarvwc5BD0-btd7XBdF681VKxRe2H_Oyg&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0)*** by Andrew Ng. This was the one that got me started.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.

*This story was first published [here](https://builtin.com/data-science/dont-democratize-data-science).*
