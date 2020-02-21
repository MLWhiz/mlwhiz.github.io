
# How to Deploy a Streamlit App using an Amazon Free ec2 instance?

How to Deploy a Streamlit App using an Amazon Free ec2 instance?

### Data Apps on the web in 10 minutes

A Machine Learning project is never really complete if we don’t have a good way to showcase it.

***While in the past, a well-made visualization or a small PPT used to be enough for showcasing a data science project, with the advent of dashboarding tools like RShiny and Dash, a good data scientist needs to have a fair bit of knowledge of web frameworks to get along.***

And Web frameworks are hard to learn. I still get confused in all that HTML, CSS, and Javascript with all the hit and trials, for something seemingly simple to do.

Not to mention the many ways to do the same thing, making it confusing for us data science folks for whom web development is a secondary skill.

This is where ***StreamLit*** comes in and delivers on its promise to create web apps just using Python.

In my [last post on Streamlit](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582), I talked about how to write Web apps using simple Python for Data Scientists.

***But still, a major complaint, if you would check out the comment section of that post, was regarding the inability to deploy Streamlit apps over the web.***

And it was a valid complaint.
> # A developer can’t show up with his laptop every time the client wanted to use the app. What is the use of such an app?

***So in this post, we will go one step further deploy our Streamlit app over the Web using an Amazon Free ec2 instance.***

## Setting up the Amazon Instance

Before we start with using the amazon ec2 instance, we need to set one up. You might need to sign up with your email ID and set up the payment information on the [AWS website](https://aws.amazon.com). Works just like a simple sign-on. From here, I will assume that you have an AWS account and so I am going to explain the next essential parts so you can follow through.

* Go to AWS Management Console using [https://us-west-2.console.aws.amazon.com/console](https://us-west-2.console.aws.amazon.com/console).

* On the AWS Management Console, you can select “Launch a Virtual Machine”. Here we are trying to set up the machine where we will deploy our Streamlit app.

* In the first step, you need to choose the AMI template for the machine. I select the 18.04 Ubuntu Server since it is applicable for the Free Tier. And Ubuntu.

![](/images/streamlitec2/0.png)

* In the second step, I select the t2.micro instance as again it is the one which is eligible for the free tier. As you can see t2.micro is just a single CPU instance with 512 MB RAM. You can opt for a bigger machine if you are dealing with a powerful model or are willing to pay.

![](/images/streamlitec2/1.png)

* Keep pressing Next until you reach the “6. Configure Security Group” tab. You will need to add a rule with Type: “Custom TCP Rule”, Port Range:8501, and Source: Anywhere. We use the port 8501 here since it is the custom port used by Streamlit.

![](/images/streamlitec2/2.png)

* You can click on “Review and Launch” and finally on the “Launch” button to launch the instance. Once you click on Launch you might need to create a new key pair. Here I am creating a new key pair named streamlit and downloading that using the “Download Key Pair” button. Keep this key safe as it would be required every time you need to login to this particular machine. Click on “Launch Instance” after downloading the key pair

![](/images/streamlitec2/3.png)

* You can now go to your instances to see if your instance has started. Hint: See the Instance state, it should be showing “Running”

![](/images/streamlitec2/4.png)

* Select your instance, and copy the ***Public DNS(IPv4) Address*** from the description. It should be something starting with ec2.

* Once you have that run the following commands in the folder you saved the streamlit.pem file. I have masked some of the information here.

    chmod 400 streamlit.pem

    ssh -i "streamlit.pem" ubuntu@<Your Public DNS(IPv4) Address>

![](/images/streamlitec2/5.png)

## Installing Required Libraries

Whoa, that was a handful. After all the above steps you should be able to see the ubuntu prompt for the virtual machine. We will need to set up this machine to run our app. I am going to be using the same streamlit_football_demo app that I used in my [previous post](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582).

We start by installing miniconda and adding its path to the environment variable.

    sudo apt-get update

    wget [https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh](https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh) -O ~/miniconda.sh

    bash ~/miniconda.sh -b -p ~/miniconda

    echo "PATH=$PATH:$HOME/miniconda/bin" >> ~/.bashrc

    source ~/.bashrc

We then install additional dependencies for our app to run. That means I install streamlit and [plotly_express](https://towardsdatascience.com/pythons-one-liner-graph-creation-library-with-animations-hans-rosling-style-f2cb50490396).

    pip install streamlit
    pip install plotly_express

And our machine is now prepped and ready to run.

## Running Streamlit on Amazon ec2

As I am set up with the instance, I can get the code for my demo app from [Github](https://github.com/MLWhiz/streamlit_football_demo.git). Or you can choose to create or copy another app as you wish.

    git clone [https://github.com/MLWhiz/streamlit_football_demo.git](https://github.com/MLWhiz/streamlit_football_demo.git)

    cd streamlit_football_demo
    streamlit run helloworld.py

![](/images/streamlitec2/6.png)

Now you can go to a browser and type the external URL to access your app. In my case the address is [http://35.167.158.251:8501](http://35.167.158.251:8501). Here is the output. This app will be up right now if you want to play with it.

![](/images/streamlitec2/7.png)

## A Very Small Problem Though

We are up and running with our app for the world to see. ***But whenever you are going to close the SSH terminal window the process will stop and so will your app.***

***So what do we do?***

TMUX to the rescue. TMUX allows us to keep running our sessions even after we leave the terminal window. It also helps with a lot of other things but I will just go through the steps we need.

First, we stop our app using Ctrl+C and install tmux

    sudo apt-get install tmux

We start a new tmux session using the below command. We keep the name of our session as StreamSession. You could use any name here.

    tmux new -s StreamSession

![](/images/streamlitec2/8.png)

You can see that the session name is “StreamSession” at the bottom of the screen. You can now start running streamlit in the tmux session.

    streamlit run helloworld.py

![](/images/streamlitec2/9.png)

You will be able to see your app at the [External URL](http://35.167.158.251:8501/\). The ***next step is to detach our TMUX session ***so that it continues running in the background when you leave the SSH shell. To do this just press Ctrl+B and then D (Don’t press Ctrl when pressing D)

![](/images/streamlitec2/10.png)

***You can now close your SSH session and the app will continue running at the External URL.***

And Voila! We are up and running.

***Pro TMUX Tip: ***You can reattach to the same session by using the attach command below. The best part is that you can close your SSH shell and then maybe come back after some hours and reattach to a session and keep working from wherever you were when you closed the SSH shell.

    tmux attach -t StreamSession

## Simple Troubleshooting:

***If your app is not hosting at 8501,*** it means that an instance of streamlit app is already running on your system and you will need to stop that. You can do so by first finding the process ID

    ps aux | grep streamlit

You will see something like:

    ubuntu   **20927**  2.4 18.8 713780 189580 pts/3   Sl+  19:55   0:26 /home/ubuntu/miniconda/bin/python /home/ubuntu/miniconda/bin/**streamlit** run helloworld.py

You will need to*** kill this process.*** You can do this simply by

    kill -9 20947

## Conclusion

![Our Final App](/images/streamlitec2/11.png)*Our Final App*

Streamlit has democratized the whole process to create apps, and I couldn’t recommend it more. If you want to learn more about how to create awesome web apps with Streamlit then read up my [last](https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582) post.

***In this post, we [deployed](https://towardsdatascience.com/take-your-machine-learning-models-to-production-with-these-5-simple-steps-35aa55e3a43c) a simple web app on AWS using amazon ec2.***

In the process of doing this, we created our own Amazon ec2 instance, logged into the SSH shell, installed miniconda and dependencies, ran our Streamlit application and learned about TMUX. Enough learning for a day?

So go and show on these Mad skills. To end on a lighter note, as Sten Sootla says in his [satire piece](https://towardsdatascience.com/how-to-fake-being-a-good-programmer-cbef2c39764c) which I thoroughly enjoyed:
> # The secret: it’s not what you know, it’s what you show.

If you want to learn more about how to structure a Machine Learning project and the best practices, I would like to call out his excellent [third course](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.11421702016&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Fmachine-learning-projects) named Structuring Machine learning projects in the Coursera [Deep Learning Specialization](https://click.linksynergy.com/deeplink?id=lVarvwc5BD0&mid=40328&murl=https%3A%2F%2Fwww.coursera.org%2Fspecializations%2Fdeep-learning). Do check it out.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------) or Subscribe to my [blog](http://eepurl.com/dbQnuX?source=post_page---------------------------) to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
