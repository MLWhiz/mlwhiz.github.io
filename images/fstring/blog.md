---
title: How and Why to use f strings in Python3?
date:  2020-05-24
draft: false
url : blog/2020/05/24/fstring/
slug: fstring
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: This post is specifically about using f strings in Python that was introduced in Python 3.6

thumbnail : /images/fstring/main.png
images :
 - /images/fstring/main.png
toc : false
---


# 

Python Shorts

## How and Why to use f strings in Python3

### A simple guide to use the new functionality in Python 3

[Python](https://amzn.to/2XPSiiG) provides us with many styles of coding.

And with time, Python has regularly come up with new coding standards and tools that adhere even more to the coding standards in the Zen of Python.
> # Beautiful is better than ugly.

In this series of posts named[ **Python Shorts](https://towardsdatascience.com/tagged/python-shorts)**, I will explain some simple but very useful constructs provided by Python, some essential tips, and some use cases I come up with regularly in my Data Science work.

This post is specifically ***about using f strings in Python **that was introduced in Python 3.6**.***

## 3 Common Ways of Printing:

Let me explain this with a simple example. Suppose you have some variables, and you want to print them within a statement.

    name = 'Andy'
    age = 20
    print(?)
    ----------------------------------------------------------------
    Output: I am Andy. I am 20 years old

You can do this in various ways:

**a) Concatenate: **A very naive way to do is to simply use + for concatenation within the print function. But that is clumsy. We would need to convert our numeric variables to string and keep care of the spaces while concatenating. And it doesn’t look good as the code readability suffers a little when we use it.

    name = 'Andy'
    age = 20
    print("I am " + name + ". I am " + str(age) + " years old")
    ----------------------------------------------------------------
    I am Andy. I am 20 years old

![Source: [Pixabay](https://pixabay.com/photos/art-art-supplies-artist-blue-brush-1478831/)](/images/fstring/0.png)*Source: [Pixabay](https://pixabay.com/photos/art-art-supplies-artist-blue-brush-1478831/)*

**b) % Format: **The second option is to use % formatting. But it also has its problems. For one, it is not readable. You would need to look at the first %s and try to find the corresponding variable in the list at the end. And imagine if you have a long list of variables that you may want to print.

    print("I am %s. I am %s years old" % (name, age))

**c) str.format(): **Next comes the way that has been used in most Python 3 codes and has become the standard of printing in Python. Using str.format()

    print("I am {}. I am {} years old".format(name, age))

Here we use {} to denote the placeholder of the object in the list. It still has the same problem of readability, but we can also use str.format :

    print("I am {name}. I am {age} years old".format(name = name, age = age))

If this seems a little too repetitive, we can use dictionaries too:

    data = {'name':'Andy','age':20}
    print("I am {name}. I am {age} years old".format(**data))

## The Fourth Way with f

![Photo by [Willem-Jan Huisman](https://unsplash.com/@willemjanhuisman?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/fstring/1.png)*Photo by [Willem-Jan Huisman](https://unsplash.com/@willemjanhuisman?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Since Python 3.6, we have a new formatting option, which makes it even more trivial. We could simply use:

    print(f"I am {name}. I am {age} years old")

We just append f at the start of the string and use {} to include our variable name, and we get the required results.

An added functionality that f string provides is that** we can put expressions** in the {} brackets. For Example:

    num1 = 4
    num2 = 5
    print(f"The sum of {num1} and {num2} is {num1+num2}.")
    ---------------------------------------------------------------
    The sum of 4 and 5 is 9.

This is quite useful as you can use any sort of expression inside these brackets. ***The expression can contain dictionaries or functions. ***A simple example:

    def totalFruits(apples,oranges):
        return apples+oranges

    data = {'name':'Andy','age':20}

    apples = 20
    oranges = 30

    print(f"{data['name']} has {totalFruits(apples,oranges)} fruits")
    ----------------------------------------------------------------
    Andy has 50 fruits

Also, you can use ’’’ to use*** multiline strings***.

    num1 = 4
    num2 = 5
    print(f'''The sum of 
    {num1} and 
    {num2} is 
    {num1+num2}.''')

    ---------------------------------------------------------------
    The sum of 
    4 and 
    5 is 
    9.

An everyday use case while formatting strings is to** format floats**. You can do that using f string as following

    numFloat = 10.23456678
    print(f'Printing Float with 2 decimals: {numFloat:.2f}')

    -----------------------------------------------------------------
    Printing Float with 2 decimals: 10.23

## Conclusion

Until recently, I had been using Python 2 for all my work, and so was not able to check out this new feature.

But now, as I am shifting to Python 3, f strings has become my go-to syntax to format strings. It is easy to write and read with the ability to incorporate arbitrary expressions as well. In a way, this new function adheres to at least 3 [PEP](https://www.python.org/dev/peps/pep-0020/) concepts —
> # Beautiful is better than ugly, Simple is better than complex and Readability counts.

If you want to learn more about [Python](https://amzn.to/2XPSiiG) 3, I would like to call out an excellent course on Learn [**Intermediate level Python](https://bit.ly/2XshreA)** from the University of Michigan. Do check it out.

I am going to be writing more of such posts in the future too. Let me know what you think about the series. Follow me up at [**Medium](https://medium.com/@rahul_agarwal)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
