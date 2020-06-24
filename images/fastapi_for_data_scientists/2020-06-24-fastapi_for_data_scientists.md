
---
title:  A Layman’s Guide for Data Scientists to create APIs in minutes
date:  2020-06-24
draft: false
url : blog/2020/06/06/fastapi_for_data_scientists/
slug: fastapi_for_data_scientists
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: 

thumbnail : /images/fastapi_for_data_scientists/main.png
images :
 - /images/fastapi_for_data_scientists/main.png
toc : false
---

![](/images/fastapi_for_data_scientists/main.png)


Have you ever been in a situation where you want to provide your model predictions to a frontend developer without them having access to model related code? Or has a developer ever asked you to create an API that they can use? I have faced this a lot.

As Data Science and Web developers try to collaborate, API’s become an essential piece of the puzzle to make codes as well as skills more modular. In fact, in the same way, that a data scientist can’t be expected to know much about Javascript or nodeJS, a frontend developer should be able to get by without knowing any Data Science Language. And APIs do play a considerable role in this abstraction.

But, APIs are confusing. I myself have been confused a lot while creating and sharing them with my development teams who talk in their API terminology like GET request, PUT request, endpoint, Payloads, etc.

***This post will be about simplifying and understanding how APIs work, explaining some of the above terms, and creating an API using the excellent API building framework called FastAPI, which makes creating APIs a breeze.***

---
## What is an API?

Before we go any further, we need to understand what an API is. According to Wikipedia:
> An **application programming interface** (**API**) is a [computing interface](https://en.wikipedia.org/wiki/Interface_(computing)) which defines interactions between multiple software intermediaries. It defines the kinds of calls or requests that can be made, how to make them, the data formats that should be used, the conventions to follow, etc.

*The way I like to understand an API is that it’s an “online function,” a function that I can call online.*

For example:

I can have a movie API, which returns me names of drama movies when I pass the “animation” genre as input.

![](/images/fastapi_for_data_scientists/0.png)

***The advantage of using such a sort of mechanism is that the API user doesn’t get access to the whole dataset or source code and yet they can get all the information they need. **This is how many services on the internet like [Amazon Rekognition](https://aws.amazon.com/rekognition/), which is an image and video API, or [Google Natural Language API](https://cloud.google.com/natural-language/pricing), which is an NLP API works. They provide us access to some great functions without letting us have the source code, which is often valuable and kept hidden. For example, I can send an image to Amazon Rekognition API, and it can provide me with Face detection and Analysis.*

![[Source](https://aws.amazon.com/rekognition/?blog-cards.sort-by=item.additionalFields.createdDate&blog-cards.sort-order=desc)](/images/fastapi_for_data_scientists/1.png)*[Source](https://aws.amazon.com/rekognition/?blog-cards.sort-by=item.additionalFields.createdDate&blog-cards.sort-order=desc)*

For example, here is a free API floated by Open Movie DB, which lets us search for movies using parameters:

    [http://www.omdbapi.com/?i=tt3896198&apikey=9ea43e94](http://www.omdbapi.com/?i=tt3896198&apikey=9ea43e94)

Here I provided the IMDB id for the movie Guardians of the Galaxy 2, using the i parameter for the API. If you open this link in your browser, you will see the whole information of the movie as per the Open Movie Database

![Output from OMDB](/images/fastapi_for_data_scientists/2.png)*Output from OMDB*

But before we go any further, let’s understand some terms:

* **Endpoint:** In the above API call, the endpoint is : http://www.omdbapi.com/ . Simply this is the location of where the function code is running.

* **API Access Key**: Most of the public APIs will have some access key, which you can request. For OMDB API, I had to register and get the API key which is [9ea43e94](http://www.omdbapi.com/?i=tt3896198&apikey=9ea43e94).

* **? Operator: **This operator is used to specify the parameters we want to send to the API or our “online function.” Here we give two params to our API i.e., IMDB movie ID and API Access Key using the ? operator. Since there are multiple inputs, we use & operator also.

---
## Why FastAPI?

*“If you’re looking to learn one modern framework for building REST APIs, check out FastAPI […] It’s fast, easy to use and easy to learn […]*” — [spaCy](https://spacy.io/) creators

While Python has many frameworks to build APIs, the most common being Flask and Tornado, FastAPI is much better than available alternatives in its ease of usage as it seems much more pythonic in comparison with Flask.

Also, FastAPI is fast. As the Github docs say, ***“Very high performance, on par with NodeJS and Go.”** We can also check the latency [benchmarks](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=z8kflr-v&a=2) for ourselves.*

![[Source](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=z8kflr-v&a=23)](/images/fastapi_for_data_scientists/3.png)*[Source](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=z8kflr-v&a=23)*

That is around a speedup by a factor of 2 when compared to Flask and that too without a lot of code change. This means a huge deal when it comes to building an API that can serve millions of customers as it can reduce production efforts and also use less expensive hardware to serve.

So enough of comparison and talk, let’s try to use FastAPI to create our API.

---
## How to write an API with FastAPI?

One of the most common use cases for Data Science is how to create an API for getting a model’s prediction? Let us assume that we have a Titanic Survival model in place that predicts if a person will survive or not. And, it needs a person’s age and sex as input params to predict. We will create this API using FastAPI in two ways: GET and PUT. Don’t worry; I will explain each as we go.

**What is GET? — **In a GET request, we usually try to retrieve data using query parameters that are embedded in the query string itself. For example, in the OMDB API, we use the GET request to specify the movie id and access key as part of the query itself.

**What is PUT? — **An alternative to the GET request is the PUT request, where we send parameters using a payload, as we will see in the second method. The payload is not part of the query string, and thus PUT is more secure. It will become more clear when you see the second part.

But before we go any further, we need to install FastAPI and uvicorn ASGI server with:

    pip install fastapi
    pip install uvicorn

### 1. The GET Way:

A simple FastAPI method to writing a GET API for our titanic model use case is as follows:

    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/predict")
    def predict_complex_model(age: int,sex:str):
        # Assume a big and complex model here. For this test I am using a simple rule based model
        if age<10 or sex=='F':
            return {'survived':1}
        else:
            return {'survived':0}

Save the above code in a file named fastapiapp.py and then you can run it using the below command on terminal.

    $ uvicorn fastapiapp:app --reload

The above means that your API is now running on your server, and the --reload flag indicates that the API gets updated automatically when you change the fastapiapp.py file. This is very helpful while developing and testing, but you should remove this --reload flag when you put the API in production. Now you can visit the below path in your browser, and you will get the prediction results:

    [http://127.0.0.1:8000/predict?age=10&sex=M](http://127.0.0.1:8000/predict?age=10&sex=M)

![](/images/fastapi_for_data_scientists/4.png)

What happens is as you hit the command in your browser, it calls the [http://127.0.0.1:8000/](http://127.0.0.1:8000/predict?age=10&sex=M)predict endpoint which in turn calls the associated method predict_complex_model with the with params age=10 and sex='M'

So, it allows us to use our function from a browser, but that’s still not very helpful. Your developer friend needs to use your predict function to show output on a frontend website. How can you provide him with access to this function?

It is pretty simple. If your developer friend also uses Python, for example, he can use the requests module like below:

    import requests

    age = 15
    sex = "F"

    response = requests.get(f"[http://127.0.0.1:8000/predict?age={age}&sex={](http://127.0.0.1:8000/predict?age=10&sex=M)sex}")
    output = response.json()

![](/images/fastapi_for_data_scientists/5.png)

So we can get the output from the running API(on the server) into our Python Program. A Javascript user would use Javascript Request Library, and a nodeJS developer will use something similar to do this in nodeJS. We will just need to provide them with the endpoint and parameters required.

To test your API, you could also go to the:

    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Where you will find a GUI way to test your API.

![](/images/fastapi_for_data_scientists/6.png)

But as we said earlier, **THIS IS NOT SECURE** as GET parameters are passed via URL. This means that parameters get stored in server logs and browser history. This is not intended. Further, this toy example just had two input parameters, so we were able to do it this way, think of a case where we need to provide many parameters to our predict function.

In such a case or I dare say in most of the cases, we use the PUT API.

### 2. The PUT Way

Using the PUT API, we can call any function by providing a payload to the function. A payload is nothing but a JSON dictionary of input parameters that doesn’t get appended to the query string and is thus much more secure than GET.

Here is the minimal example where we do that same thing as before using PUT. We just change the content of fastapiapp.py to:

    from fastapi import FastAPI
    from pydantic import BaseModel

    class Input(BaseModel):
        age : int
        sex : str

    app = FastAPI()

    [@app](http://twitter.com/app).put("/predict")
    def predict_complex_model(d:Input):
        if d.age<10 or d.sex=='F':
            return {'survived':1}
        else:
            return {'survived':0}

note that we use app.put here in place of app.get previously. We also needed to provide a new class Input , which uses a library called pydantic to validate the input data types that we will get from the API end-user while previously in GET, we validated the inputs using the function parameter list. Also, this time you won’t be able to see your content using a URL on the web. For example, using the browser to point to the endpoint location gives:

![](/images/fastapi_for_data_scientists/7.png)

So, we can check using the programmatic way using requests in Python again:

    import requests,json
    payload = json.dumps({
      "age": 10,
      "sex": "F"
    })
    response = requests.put("[http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)",data = payload)
    response.json()

![](/images/fastapi_for_data_scientists/8.png)

Notice that we use requests.put here and we provide the payload using the data param in the requests.put function and we also make use of json library to convert our payload to JSON from a dict object.

We could also have used the GUI way as before using:

    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

![](/images/fastapi_for_data_scientists/9.png)

And, we are done with creating our API. It was simple for a change.

FastAPI makes the API creation, which used to be one of the dreaded parts of the Data Science process, much more intuitive, easy, and Fast.

You can find the code for this post as well as all my posts at my [GitHub](https://github.com/MLWhiz/data_science_blogs/tree/master/fastapi) repository.

---
## Continue Learning

If you want to learn more about building and putting a Machine Learning model in production, this [course on AWS](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.14884356434&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Faws-machine-learning) for implementing Machine Learning applications promises just that.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------) or Subscribe to my [blog](http://eepurl.com/dbQnuX?source=post_page---------------------------) to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
