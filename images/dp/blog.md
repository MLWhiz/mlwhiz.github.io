
# Dynamic Programming for Data Scientists

ALGORITHMS INTERVIEWS

## Dynamic Programming for Data Scientists

### How to solve DP problems easily?

Algorithms and data structures are an integral part of data science. While most of us data scientists don’t take a proper algorithms course while studying, they are important all the same.

Many companies ask data structures and algorithms as part of their interview process for hiring data scientists.

Now the question that many people ask here is what is the use of asking a data scientist such questions. ***The way I like to describe it is that a data structure question may be thought of as a coding aptitude test.***

*We all have given aptitude tests at various stages of our life, and while they are not a perfect proxy to judge someone, almost nothing ever really is. *So, why not a standard algorithm test to judge people’s coding ability.

But let’s not kid ourselves, they will require the same zeal to crack as your Data Science interviews, and thus, you might want to give some time for the study of algorithms and Data structure and algorithms questions.

***This post is about fast-tracking this study and explaining Dynamic Programming concepts for the data scientists in an easy to understand way.***

## How Dynamic Programming Works?

Let’s say that we need to find the nth Fibonacci Number.

Fibonacci series is a series of numbers in which each number ( *Fibonacci number* ) is the sum of the two preceding numbers. The simplest is the series 1, 1, 2, 3, 5, 8, etc. The answer is:

    def fib(n):
        if n<=1:
            return 1
        return fib(n-1) + fib(n-2)

This problem relates well to a recursive approach. But can you spot the problem here?

If you try to calculate fib(n=7) it runs fib(5) twice, fib(4) thrice, fib(3) five times. As n becomes larger, a lot of calls are made for the same number, and our recursive function calculates it again and again.

![[Source](https://www.rubyguides.com/2015/08/ruby-recursion-and-memoization/)](/images/dp/0.png)*[Source](https://www.rubyguides.com/2015/08/ruby-recursion-and-memoization/)*

Now, Recursion is essentially a top-down approach. As in when calculating Fibonacci number n we start from n and then do recursive calls for n-2 and n-1 and so on.

In ***Dynamic programming***, we take a bottom-up approach. It is essentially a way to write recursion iteratively. We start by calculating fib(0) and fib(1) and then use previous results to generate new results.

    def fib_dp(n):
        dp_sols = {0:1,1:1}
        for i in range(2,n+1):
            dp_sols[i] = dp_sols[i-1] + dp_sols[i-2] 
        return dp_sols[n]

## Why Dynamic Programming is Hard?

Recursion is a mathematical concept and it comes naturally to us. We try to find a solution to a bigger problem by breaking it into smaller ones.

Now Dynamic Programming entails exactly the same idea but in the case of Dynamic programming, we precompute all the subproblems that might need to be calculated in a bottom-up manner.

We human beings are essentially hard-wired to work in a top-down manner. Be it our learning where most people try to go into the breadth of things before going in-depth. Or be it the way we think.

So how does one start thinking in a bottom-up way?

***I found out that solving the below problem gives a lot of intuition in how DP works.*** I myself got highly comfortable with DP once I was able to solve this one and hope it helps you too.

Basically the idea is if you can derive/solve a bigger subproblem if you know the solution to a smaller one?

## Maximum Path Sum

Given a *m* x *n* grid filled with gold, find a path from top left to bottom right which *maximizes* the sum of gold along its path. We can only move down or right starting from (0,0)

Now there can be decidedly many paths. We can go all the way to the right and then the bottom. Or we can take a zigzag path?

![](/images/dp/1.png)

But only one/few paths are going to make you rich.

So how do you even start thinking about such a problem?

When we think of Dynamic Programming questions, we take a bottom-up approach. So we start by thinking about the simplest of problems. In our case, the simplest of problems to solve is the base case. What is the maximum value of Gold we can acquire if we just had to reach cell (0,0)?

And the answer to that is pretty simple — It is the cell value itself.

![](/images/dp/2.png)

So we move on to a little harder problem.

![](/images/dp/3.png)

What about cell (0,1) and cell (1,0)?

These are also pretty simple. We can reach (0,1)and (1,0) through only (0,0) and hence the maximum gold we can obtain is the value in cell (0,1)/(1,0) plus the maximum gold we can have when we reach cell(0,0)

What about cell(0,2)? Again only one path. So if we know the solution to (0,1) we can just add the value of cell (0,2) to get the solution for (0,2)

Let’s now try to do the same for an arbitrary cell. We want to derive a relation here.

![](/images/dp/4.png)

***So in the case of an arbitrary cell, we can reach it from the top or from the left. ***If we know the solutions to the top and left of the cell, we can definitely compute the solution to the arbitrary current target cell.

### Coding

Once we have the intuition the coding exercise is pretty straightforward. We start by calculating the solutions for the first row and first column. And then we continue to calculate the other values in the grid using the relation we got previously.

    def maxPathSum(grid):
        m = len(grid)
        n = len(grid[0])
        # sol keeps the solutions for each point in the grid.
        sol = list(grid)
        # we start by calculating solutions for the first row
        for i in range(1,n):
            sol[0][i] += sol[0][i-1]
        # we then calculate solutions for the first column
        for i in range(1,m):
            sol[i][0] += sol[i-1][0]
        # we then calculate all the solutions in the grid
        for i in range(1,m):
            for j in range(1,n):
                sol[i][j] += max(sol[i-1][j],sol[i][j-1])
        # return the last element
        return sol[-1][-1]

## Conclusion

***In this post, I talked about how I think about Dynamic Programming questions.***

***I start by asking myself the simplest problem I could solve and if I can solve the bigger problem by using the solutions to the simpler problem.***

Dynamic Programming forms the basis of some of the most asked questions in Data Science/Machine Learning job interviews, and a good understanding of these might help you land your dream job.

So go out there and do some problems with Leetcode/HackerRank. The problems are surely interesting.

Also take a look at my other posts in the [series](https://towardsdatascience.com/tagged/algorithms-interview), if you want to learn about algorithms and Data structures.

## Continue Learning

If you want to read up more on Algorithms and Data structures, here is an [**Algorithm Specialization on Coursera by UCSanDiego](https://click.linksynergy.com/deeplink?id=lVarvwc5BD0&mid=40328&murl=https%3A%2F%2Fwww.coursera.org%2Fspecializations%2Fdata-structures-algorithms), **which I highly recommend.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea
