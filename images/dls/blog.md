---
title: Stop Worrying and Create your Deep Learning Server in 30 minutes
date:  2020-05-25
draft: false
url : blog/2020/05/25/dls/
slug: dls
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: In this piece, I want to point out five of the most common types of cognitive biases. I will also offer some suggestions on how data scientists can work to avoid them and make better, more reasoned decisions.

thumbnail : /images/dls/main.png
images :
 - /images/dls/main.png
toc : false
---

![](/images/dls/main.png)

I have found myself creating a Deep Learning Machine time and time again whenever I start a new project.

You start with installing Anaconda and end up creating different environments for Pytorch and Tensorflow, so they don’t interfere. And in the middle of it, you inevitably end up messing up and starting from scratch. And this often happens multiple times.

It is not just a massive waste of time; it is also mighty(trying to avoid profanity here) irritating. Going through all those Stack Overflow threads. Often wondering what has gone wrong.

So is there a way to do this more efficiently?

It turns out there is. ***In this blog, I will try to set up a deep learning server on EC2 with minimal effort so that I could focus on more important things.***

*This blog consists explicitly of two parts:*

1. *Setting up an Amazon EC2 Machine with preinstalled deep learning libraries.*

1. *Setting Up Jupyter Notebook using TMUX and SSH tunneling.*

*Don’t worry; it’s not as difficult as it sounds. Just follow the steps and click Next.*

---

## Setting up Amazon EC2 Machine

I am assuming that you have an AWS account, and you have access to the [AWS Console](https://aws.amazon.com/console/). If not, you might need to sign up for an Amazon AWS account.

1. First of all, we need to go to the Services tab to access the EC2 dashboard.

![](/images/dls/1.png)

2. On the EC2 Dashboard, you can start by creating your instance.

![](/images/dls/2.png)

3. Amazon provides Community AMIs(Amazon Machine Image) with Deep Learning software preinstalled. To access these AMIs, you need to look in the community AMIs and search for “Ubuntu Deep Learning” in the Search Tab. You can choose any other Linux flavor, but I have found Ubuntu to be most useful for my Deep Learning needs. In the present setup, I will use The Deep Learning AMI (Ubuntu 18.04) Version 27.0

![](/images/dls/3.png)

4. Once you select an AMI, you can select the Instance Type. It is here you specify the number of CPUs, Memory, and GPUs you will require in your system. Amazon provides a lot of options to choose from based on one’s individual needs. You can filter for GPU instances using the “Filter by” filter.

In this tutorial, I have gone with p2.xlarge instance, which provides NVIDIA K80 GPU with 2,496 parallel processing cores and 12GiB of GPU memory. To know about different instance types, you can look at the [documentation](https://aws.amazon.com/ec2/instance-types/) here and the pricing [here](https://aws.amazon.com/emr/pricing/).

![](/images/dls/4.png)

5. You can change the storage that is attached to the machine in the 4th step. It is okay if you don’t add storage upfront, as you can also do this later. I change the storage from 90 GB to 500 GB as most of the deep learning needs will require proper storage.

![](/images/dls/5.png)

6. That’s all, and you can Launch the Instance after going to the Final Review instance settings Screen. Once you click on Launch, you will see this screen. Just type in any key name in the Key Pair Name and click on “Download key pair”. Your key will be downloaded to your machine by the name you provided. For me, it got saved as “aws_key.pem”. Once you do that, you can click on “Launch Instances”.

![](/images/dls/6.png)

Keep this key pair safe as this will be required whenever you want to login to your instance.

7. You can now click on “View Instances” on the next page to see your instance. This is how your instance will look like:

![](/images/dls/7.png)

8. To connect to your instance, Just open a terminal window in your Local machine and browse to the folder where you have kept your key pair file and modify some permissions.

    chmod 400 aws_key.pem

Once you do that, you will be able to connect to your instance by SSHing. The SSH command will be of the form:

    ssh -i "aws_key.pem" ubuntu@<Your PublicDNS(IPv4)>

For me, the command was:

    ssh -i "aws_key.pem" ubuntu@ec2-54-202-223-197.us-west-2.compute.amazonaws.com

![](/images/dls/8.png)

Also, keep in mind that the Public DNS might change once you shut down your instance.

9. You have already got your machine up and ready. This machine contains different environments that have various libraries you might need. This particular machine has MXNet, Tensorflow, and Pytorch with different versions of python. And the best thing is that we get all this preinstalled, so it just works out of the box.

![](/images/dls/9.png)

---

## Setting Up Jupyter Notebook

But there are still a few things you will require to use your machine fully. One of them being Jupyter Notebooks. To set up Jupyter Notebooks with your Machine, I recommend using TMUX and tunneling. Let us go through setting up the Jupyter notebook step by step.

### 1. Using TMUX to run Jupyter Notebook

We will first use TMUX to run the Jupyter notebook on our instance. We mainly use this so that our notebook still runs even if the terminal connection gets lost.

To do this, you will need to create a new TMUX session using:

    tmux new -s StreamSession

Once you do that, you will see a new screen with a green border at the bottom. You can start your Jupyter Notebook in this machine using the usual jupyter notebook command. You will see something like:

![](/images/dls/10.png)

It will be beneficial to copy the login URL so that we will be able to get the token later when we try to login to our jupyter notebook later. In my case, it is:

    [http://localhost:8888/?token=5ccd01f60971d9fc97fd79f64a5bb4ce79f4d96823ab7872](http://localhost:8888/?token=5ccd01f60971d9fc97fd79f64a5bb4ce79f4d96823ab7872&token=5ccd01f60971d9fc97fd79f64a5bb4ce79f4d96823ab7872)

The ***next step is to detach our TMUX session*** so that it continues running in the background even when you leave the SSH shell. To do this just press Ctrl+B and then D (Don’t press Ctrl when pressing D)You will come back to the initial screen with the message that you have detached from your TMUX session.

![](/images/dls/11.png)

If you want, you can reattach to the session again using:

    tmux attach -t StreamSession

### 2. SSH Tunneling to access the notebook on your Local Browser

The second step is to tunnel into the Amazon instance to be able to get the Jupyter notebook on your Local Browser. As we can see, the Jupyter Notebook is actually running on the localhost on the Cloud instance. How do we access it? We use SSH tunneling. Worry not, it is straightforward fill in the blanks. Just use this command on your local machine terminal window:

    ssh -i "aws_key.pem" -L <Local Machine Port>:localhost:8888 [ubuntu@](mailto:ubuntu@ec2-34-212-131-240.us-west-2.compute.amazonaws.com)<Your PublicDNS(IPv4)>

For this case, I have used:

    ssh -i "aws_key.pem" -L 8001:localhost:8888 [ubuntu@](mailto:ubuntu@ec2-34-212-131-240.us-west-2.compute.amazonaws.com)ec2-54-202-223-197.us-west-2.compute.amazonaws.com

This means that I will be able to use the Jupyter Notebook If I open the localhost:8001 in my local machine browser. And I surely can. We can now just input the token that we already have saved in one of our previous steps to access the notebook. For me the token is [5ccd01f60971d9fc97fd79f64a5bb4ce79f4d96823ab7872](http://localhost:8888/?token=5ccd01f60971d9fc97fd79f64a5bb4ce79f4d96823ab7872&token=5ccd01f60971d9fc97fd79f64a5bb4ce79f4d96823ab7872)

![](/images/dls/12.png)

You can just login using your token and voila we get the notebook in all its glory.

![](/images/dls/13.png)

You can now choose to work on a new project by selecting any of the different environments you want. You can come from Tensorflow or Pytorch or might be willing to get the best of both worlds. This notebook will not disappoint you.

![](/images/dls/14.png)

---

## Troubleshooting

It might happen that once the machine is restarted, you face some problems with the NVIDIA graphics card. Specifically, in my case, the nvidia-smi command stopped working. If you encounter this problem, the solution is to download the graphics driver from the NVIDIA [website](https://www.nvidia.in/Download/index.aspx?lang=en-in).

![](/images/dls/15.png)

Above are the settings for the particular AMI I selected. Once you click on Search you will be able to see the next page:

![](/images/dls/16.png)

Just copy the download link by right-clicking and copying the link address. And run the following commands on your machine. You might need to change the link address and the file name in this.

    # When nvidia-smi doesnt work:

    wget [https://www.nvidia.in/content/DriverDownload-March2009/confirmation.php?url=/tesla/410.129/NVIDIA-Linux-x86_64-410.129-diagnostic.run&lang=in&type=Tesla](https://www.nvidia.in/content/DriverDownload-March2009/confirmation.php?url=/tesla/410.129/NVIDIA-Linux-x86_64-410.129-diagnostic.run&lang=in&type=Tesla)

    sudo sh NVIDIA-Linux-x86_64-410.129-diagnostic.run --no-drm --disable-nouveau --dkms --silent --install-libglvnd

    modinfo nvidia | head -7

    sudo modprobe nvidia

---

## Stop Your Instance

And that’s it. You have got and up and running Deep Learning machine at your disposal, and you can work with it as much as you want. Just keep in mind to stop the instance whenever you stop working, so you won’t need to pay Amazon when you are not working on your instance. You can do it on the instances page by right-clicking on your instance. Just note that when you need to log in again to this machine, you will need to get the Public DNS (IPv4) address from the instance page back as it might have changed.

![](/images/dls/17.png)

---

## Conclusion

I have always found it a big chore to set up a deep learning environment.

In this blog, we set up a new Deep Learning server on EC2 in minimal time by using Deep Learning Community AMI, TMUX, and Tunneling for the Jupyter Notebooks. This server comes preinstalled with all the deep learning libraries you might need at your work, and it just works out of the box.

So what are you waiting for? Just get started with Deep Learning with your own server.

If you want to learn more about AWS and how to use it in production settings and deploying models, I would like to call out an excellent [course on AWS](https://click.linksynergy.com/link?id=lVarvwc5BD0&offerid=467035.14884356434&type=2&murl=https%3A%2F%2Fwww.coursera.org%2Flearn%2Faws-machine-learning). Do check it out.

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [Medium](https://medium.com/@rahul_agarwal?source=post_page---------------------------) or Subscribe to my [blog](http://eepurl.com/dbQnuX?source=post_page---------------------------) to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz?source=post_page---------------------------)

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources, as sharing knowledge is never a bad idea.
