---
title: 3 Programming concepts for Data Scientists
date:  2019-12-09
draft: false
url : blog/2019/12/09/pc/
slug: pc
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: This post is about fast-tracking that study and panning some essential algorithms concepts for the data scientists in an easy to understand way

thumbnail : /images/pc/main.png
images :
 - /images/pc/main.png
toc : false
---
![](/images/pc/main.png)


Algorithms are an integral part of data science. While most of us data scientists don’t take a proper algorithms course while studying, they are important all the same.

Many companies ask data structures and algorithms as part of their interview process for hiring data scientists.

Now the question that many people ask here is what is the use of asking a data scientist such questions. ***The way I like to describe it is that a data structure question may be thought of as a coding aptitude test.***

*We all have given aptitude tests at various stages of our life, and while they are not a perfect proxy to judge someone, almost nothing ever really is.*
So, why not a standard algorithm test to judge people’s coding ability.

But let’s not kid ourselves, they will require the same zeal to crack as your Data Science interviews, and thus, you might want to give some time for the study of algorithms.

***This post is about fast-tracking that study and panning some essential algorithms concepts for the data scientists in an easy to understand way.***

---

## 1. Recursion/Memoization

Recursion is where a function being defined is applied within its own definition. Put simply; recursion is when a function calls itself. Google does something pretty interesting when you search for recursion there.

![](/images/pc/0.png)

Hope you get the joke. While recursion may seem a little bit daunting to someone just starting, it is pretty simple to understand. And it is a beautiful concept once you know it.

The best example I find for explaining recursion is to calculate the factorial of a number.

```py
def factorial(n):
    if n==0:
        return 1
    return n*factorial(n-1)
```

We can see how factorial is a recursive function quite easily.

`Factorial(n) = n*Factorial(n-1)`

***So how does it translates to programming?***

A function for a recursive call generally consists of two things:

* A base case — The case where the recursion ends.

* A recursive formulation- a formulaic way to move towards the base case.

A lot of problems you end up solving are recursive. It applies to data science, as well.

For example, A decision tree is just a binary tree, and tree algorithms are generally recursive. Or, we do use sort in a lot of times. The algorithm responsible for that is called ***mergesort,*** which in itself is a recursive algorithm. Another one is ***binary search,*** which includes finding an element in an array.

Now we have got a basic hang of recursion, let us try to find the nth Fibonacci Number. Fibonacci series is a series of numbers in which each number ( *Fibonacci number* ) is the sum of the two preceding numbers. The simplest is the series 1, 1, 2, 3, 5, 8, etc. The answer is:

```py
def fib(n):
    if n<=1:
        return 1
    return fib(n-1) + fib(n-2)
```
***But do you spot the problem here?***

If you try to calculate fib(n=7) it runs fib(5) twice, fib(4) thrice, fib(3) five times. As n becomes larger, a lot of calls are made for the same number, and our recursive function calculates it again and again.

![[Source](https://www.rubyguides.com/2015/08/ruby-recursion-and-memoization/)](/images/pc/1.png)

Can we do better? Yes, we can. We can change our implementation a little bit an add a dictionary to add some storage to our method. Now, this memo dictionary gets updated any time a number has been calculated. If that number appears again, we don’t calculate it again but give results from the memo dictionary. This addition of storage is called ***Memoization***.

```py
memo = {}
def fib_memo(n):
    if n in memo:
        return memo[n]
    if n<=1:
        memo[n]=1
        return 1
    memo[n] = fib_memo(n-1) + fib_memo(n-2)
    return memo[n]
```
Usually, I like to write the recursive function first, and if it is making a lot of calls to the same parameters again and again, I add a dictionary to memorize solutions.

***How much does it help?***

![](/images/pc/2.png)

This is the run time comparison for different values of n. We can see the runtime for ***Fibonacci without Memoization*** increases exponentially, while for the memoized function, the time is linear.

---

## 2. Dynamic programming

![Bottoms Up](/images/pc/3.png)*Bottoms Up*

Recursion is essentially a top-down approach. As in when calculating Fibonacci number n we start from n and then do recursive calls for n-2 and n-1 and so on.

In Dynamic programming, we take a bottom-up approach. It is essentially a way to write recursion iteratively. We start by calculating fib(0) and fib(1) and then use previous results to generate new results.

```py
def fib_dp(n):
    dp_sols = {0:1,1:1}
    for i in range(2,n+1):
        dp_sols[i] = dp_sols[i-1] + dp_sols[i-2] 
    return dp_sols[n]
```

![](/images/pc/4.png)

Above is the comparison of runtimes for DP vs. Memoization. We can see that they are both linear, but DP still is a little bit faster.

Why? Because Dynamic Programming made only one call exactly to each subproblem in this case.

There is an excellent story on how Bellman who developed Dynamic Programming framed the term:

> Where did the name, dynamic programming, come from? The 1950s were not good years for mathematical research. We had a very interesting gentleman in Washington named [Wilson](https://en.wikipedia.org/wiki/Charles_Erwin_Wilson). He was Secretary of Defense, and he actually had a pathological fear and hatred of the word research. What title, what name, could I choose? In the first place, I was interested in planning, in decision making, in thinking. But planning, is not a good word for various reasons. I decided therefore to use the word “programming”. I wanted to get across the idea that this was dynamic, this was multistage, this was time-varying. I thought, let’s kill two birds with one stone. Thus, I thought dynamic programming was a good name. **It was something not even a Congressman could object to.** So I used it as an umbrella for my activities.

---

## 3. Binary Search

Let us say we have a sorted array of numbers, and we want to find out a number from this array. We can go the linear route that checks every number one by one and stops if it finds the number. The problem is that it takes too long if the array contains millions of elements. Here we can use a Binary search.


<div style="margin-top: 9px; margin-bottom: 10px;">
<center>
    <figure>
      <img src="/images/pc/5.gif">
      <figcaption style="font-size: 12px;">Source:mathwarehouse.com|Finding 37 — There are 3.7 trillion fish in the ocean, they’re looking for one</figcaption>
    </figure>
</center>
</div>

```py
# Returns index of target in nums array if present, else -1 
def binary_search(nums, left, right, target):   
    # Base case 
    if right >= left: 
        mid = int((left + right)/2)
        # If target is present at the mid, return
        if nums[mid] == target: 
            return mid 
        # Target is smaller than mid search the elements in left
        elif nums[mid] > target: 
            return binary_search(nums, left, mid-1, target) 
        # Target is larger than mid, search the elements in right
        else: 
            return binary_search(nums, mid+1, right, target) 
    else: 
        # Target is not in nums 
        return -1

nums = [1,2,3,4,5,6,7,8,9]
print(binary_search(nums, 0, len(nums)-1,7))
```

This is an advanced case of a recursion based algorithm where we make use of the fact that the array is sorted. Here we recursively look at the middle element and see if we want to search in the left or right of the middle element. This makes our searching space go down by a factor of 2 every step.

And thus the run time of this algorithm is O(logn) as opposed to O(n) for linear search.

How much does that matter? Below is a comparison in run times. We can see that the Binary search is pretty fast compared to Linear search.

![For n=10000, Binary search takes around 13 steps, and the Linear search takes 10000 steps.](/images/pc/6.png)

---

## Conclusion

***In this post, I talked about some of the most exciting algorithms that form the basis for programming.***

These algorithms are behind some of the most asked questions in Data Science interviews, and a good understanding of these might help you land your dream job.

And while you can go a fair bit in data science without learning them, you can learn them just for a little bit of fun and maybe to improve your programming skills.

Also take a look at my other posts in the [series](https://towardsdatascience.com/tagged/algorithms-interview), if you want to learn about algorithms and Data structures.

## Continue Learning

If you want to read up more on Algorithms, here is an [**Algorithm Specialization on Coursera by UCSanDiego**](https://click.linksynergy.com/deeplink?id=lVarvwc5BD0&mid=40328&murl=https%3A%2F%2Fwww.coursera.org%2Fspecializations%2Fdata-structures-algorithms), which I highly recommend to learn the basics of algorithms.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium**](https://medium.com/@rahul_agarwal?source=post_page---------------------------) or Subscribe to my [**blog**](http://eepurl.com/dbQnuX?source=post_page---------------------------) to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.