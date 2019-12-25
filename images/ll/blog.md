
# A simple introduction to Linked Lists for Data Scientists

ALGORITHMS INTERVIEWS

## A Simple Introduction to Linked Lists for Data Scientists

### Or, What are linked lists and why do I need to learn about them?

Algorithms and data structures are an integral part of data science. While most of us data scientists don’t take a proper algorithms course while studying, they are important all the same.

Many companies ask data structures and algorithms as part of their interview process for hiring data scientists.

Now the question that many people ask here is what is the use of asking a data scientist such questions. ***The way I like to describe it is that a data structure question may be thought of as a coding aptitude test.***

*We all have given aptitude tests at various stages of our life, and while they are not a perfect proxy to judge someone, almost nothing ever really is. *So, why not a standard algorithm test to judge people’s coding ability.

But let’s not kid ourselves, they will require the same zeal to crack as your Data Science interviews, and thus, you might want to give some time for the study of algorithms and Data structure questions.

***This post is about fast-tracking this study and explaining linked list concepts for the data scientists in an easy to understand way.***

## What are Linked Lists?

The linked list is just a very simple data structure that represents a sequence of nodes.

![](/images/ll/0.png)

Each node is just an object that contains a value and a pointer to the next node. For example, In the example here we have a node that contains the data 12 and points to the next node 99. Then 99 points to node 37 and so on until we encounter a NULL Node.

![](/images/ll/1.png)

There are also doubly linked lists in which each node contains the address of the next as well as the previous node.

## But why would we ever need Linked Lists?

![](/images/ll/2.png)

We all have worked with Lists in Python.*** But have you ever thought of the insertion time for the list data structure?***

Lets say we need to insert an element at the start of a list. Inserting or removing elements at the start in a python list requires an *O(n)* copy operation.

***What if we are faced with the problem in which there are a lot of such inserts and we need a data structure that actually does inserts in constant O(1) time?***

There are many practical applications of a linked list that you can think about. ***One can use a doubly-linked list to implement a system where only the location of previous and next nodes are needed.*** For example, the previous page and next page functionality in the chrome browser. Or the previous and next photo in a photo editor.

***Another benefit of using a linked list is that we don’t need to have contiguous space requirements for a linked list i.e. the nodes can reside anywhere in the memory while for a data structure like an array the nodes need to be allocated a sequence of memory.***

## How do we create a Linked list in Python?

We first start by defining a class that can be used to create a single node.

    class Node:
        def __init__(self,val):
            self.val = val
            self.next = None

We then use this class object to create multiple nodes and stitch them together to form a linked list.

    head = Node(12)
    a = Node(99)
    b = Node(37)

    head.next = a
    a.next = b

And we have our linked list, starting at head. In most cases, we only keep the variable head to define our linked list as it contains all the information we require to access the whole list.

## Common Operations or Interview Questions with the Linked Lists

### 1. Insert a new Node

In the start, we said that we can insert an element at the start of the linked list in a constant O(1) time. Let’s see how we can do that.

    def insert(head,val):
        new_head = Node(val)
        new_head.next = head
        return new_head

So given the head of the node, we just create a new_head object and set its pointer to the previous head of the linked list. We just create a new node and just update a pointer.

### **2. Print**/Traverse** the linked list**

Printing the elements of a linked list is pretty simple. We just go through the linked list in an iterative fashion till we encounter the None node(or the end).

    def print(head):
        while head:
            print(head.val)
            head = head.next

### 3. Reverse a singly linked list

This is more of a very common interview [question](https://leetcode.com/problems/reverse-linked-list) on linked lists. If you are given a linked list, can you reverse that linked list in O(n) time?

    **For Example:
    Input:** 1->2->3->4->5->NULL
    **Output:** 5->4->3->2->1->NULL

***So how do we deal with this?***

We start by iterating through the linked list and reversing the pointer direction while moving the head to the next node until there is a next node.

    def reverseList(head):
        newhead = None
        while head:
            tmp = head.next
            head.next = newhead
            newhead = head
            head = tmp
        return newhead

## Conclusion

***In this post, I talked about Linked List and its implementation.***

Linked lists form the basis of some of the most asked questions in Data Science interviews, and a good understanding of these might help you land your dream job.

And while you can go a fair bit in data science without learning them, you can learn them just for a little bit of fun and maybe to improve your programming skills.

Here is a small [notebook](https://www.kaggle.com/mlwhiz/linked-list-code-sample) for you where I have put all these small concepts.

I will leave you with solving this problem by yourself — ***Implement a function to check if a linked list is a palindrome.***

Also take a look at my other posts in the [series](https://towardsdatascience.com/tagged/algorithms-interview), if you want to learn about algorithms and Data structures.

## Continue Learning

If you want to read up more on Algorithms and Data structures, here is an [**Algorithm Specialization on Coursera by UCSanDiego](https://click.linksynergy.com/deeplink?id=lVarvwc5BD0&mid=40328&murl=https%3A%2F%2Fwww.coursera.org%2Fspecializations%2Fdata-structures-algorithms), **which I highly recommend.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX?source=post_page---------------------------)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
