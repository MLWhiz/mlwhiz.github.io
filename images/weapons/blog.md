---
title: Demystifying Object Detection and Instance Segmentation for Data Scientists
date:  2019-12-04
draft: false
url : blog/2019/12/04/weapons/
slug: weapons
Category: Python

Keywords:
- Pandas
- Statistics

Tags: 
- Python
- Statistics

description: this post is explaining how permutation importance works and how we can cweaponse it using ELI5

thumbnail : /images/weapons/main.jpeg
images :
 - /images/weapons/main.jpeg
toc : false
---
![](/images/weapons/main.jpeg)

# Creating a Weapon Detector in 5 simple steps

Object Detection

## Creating a Weapon Detector in 5 simple steps

### Object detection using mask-RCNN on custom Dataset

Object Detection is a helpful tool to have in your coding repository.

It forms the backbone of many fantastic industrial applications. Some of them being self-driving cars, medical imaging and face detection.

In my last [post](https://towardsdatascience.com/a-hitchhikers-guide-to-object-detection-and-instance-segmentation-ac0146fe8e11) on Object detection, I talked about how Object detection models evolved.

But what good is theory, if we can’t implement it?

***This post is about implementing and getting an object detector on our custom dataset of weapons.***

The problem we will specifically solve today is that of Instance Segmentation using Mask-RCNN.

## Instance Segmentation

*Can we create ***masks*** for each object in the image? Specifically something like:*

![](/images/weapons/0.png)

The most common way to solve this problem is by using Mask-RCNN. The architecture of Mask-RCNN looks like below:

![[Source](https://medium.com/@jonathan_hui/image-segmentation-with-mask-r-cnn-ebe6d793272)](/images/weapons/1.png)*[Source](https://medium.com/@jonathan_hui/image-segmentation-with-mask-r-cnn-ebe6d793272)*

Essentially, it comprises of:

* A backbone network like resnet50/resnet101

* A Region Proposal network

* ROI-Align layers

* Two output layers — one to predict masks and one to predict class and bounding box.

There is a lot more to it. If you want to learn more about the theory, read my last post.
[**Demystifying Object Detection and Instance Segmentation for Data Scientists**
*Easy Explanation!!! I tried*towardsdatascience.com](https://towardsdatascience.com/a-hitchhikers-guide-to-object-detection-and-instance-segmentation-ac0146fe8e11)

This post is mostly going to be about the [code](https://github.com/MLWhiz/object_detection).

## 1. Creating your Custom Dataset for Instance Segmentation

![Our Dataset](/images/weapons/2.png)*Our Dataset*

The use case we will be working on is a weapon detector. A weapon detector is something that can be used in conjunction with street cameras as well as CCTV’s to fight crime. So it is pretty nifty.

So, I started with downloading 40 images each of guns and swords from the [open image dataset](https://storage.googleapis.com/openimages/web/index.html) and annotated them using the VIA tool. Now setting up the annotation project in VIA is petty important, so I will try to explain it step by step.

### 1. Set up VIA

VIA is an annotation tool, using which you can annotate images both bounding boxes as well as masks. I found it as one of the best tools to do annotation as it is online and runs in the browser itself.

To use it, open [http://www.robots.ox.ac.uk/~vgg/software/via/via.html](http://www.robots.ox.ac.uk/~vgg/software/via/via.html)

You will see a page like:

![](/images/weapons/3.png)

The next thing we want to do is to add the different class names in the region_attributes. Here I have added ‘gun’ and ‘sword’ as per our use case as these are the two distinct targets I want to annotate.

![](/images/weapons/4.png)

### 2. Annotate the Images

I have kept all the files in the folder data. Next step is to add the files we want to annotate. We can add files in the data folder using the “Add Files” button in the VIA tool. And start annotating along with labels as shown below after selecting the polyline tool.

![Click, Click, Enter, Escape, Select](/images/weapons/5.png)*Click, Click, Enter, Escape, Select*

### 3. Download the annotation file

Click on save project on the top menu of the VIA tool.

![](/images/weapons/6.png)

Save file as via_region_data.json by changing the project name field. This will save the annotations in COCO format.

### 4. Set up the data directory structure

We will need to set up the data directories first so that we can do object detection. In the code below, I am creating a directory structure that is required for the model that we are going to use.

<iframe src="https://medium.com/media/511fb7325bf81c542e79630bd50c031a" frameborder=0></iframe>

After running the above code, we will get the data in the below folder structure:

    - procdata
         - train
             - img1.jpg
             - img2.jpg
             - via_region_data.json
         - val
             - img3.jpg
             - img4.jpg
             - via_region_data.json

## 2. Setup the Coding Environment

We will use the code from the [matterport/Mask_RCNN](https://github.com/matterport/Mask_RCNN) GitHub repository. You can start by cloning the repository and installing the required libraries.

    git clone [https://github.com/matterport/Mask_RCNN](https://github.com/matterport/Mask_RCNN)
    cd Mask_RCNN
    pip install -r requirements.txt

Once we are done with installing the dependencies and cloning the repo, we can start with implementing our project.

We make a copy of the samples/balloon directory in Mask_RCNN folder and create a ***samples/guns_and_swords ***directory where we will continue our work:

    cp -r samples/balloon ***samples/guns_and_swords***

### Setting up the Code

![Yes. We are doing AI](/images/weapons/7.png)*Yes. We are doing AI*

We start by renaming and changing balloon.py in the ***samples/guns_and_swords directory to gns*.py**. The balloon.py file right now trains for one target. I have extended it to use multiple targets. In this file, we change:

1. balloonconfig to gnsConfig

1. BalloonDataset to gnsDataset : We changed some code here to get the target names from our annotation data and also give multiple targets.

1. And some changes in thetrain function

Showing only the changedgnsConfig here to get you an idea. You can take a look at the whole [gns.py](https://github.com/MLWhiz/object_detection/blob/master/guns_and_swords/gns.py) code here.

<iframe src="https://medium.com/media/62f6d59bb1a6771e5d453cc7acfc805b" frameborder=0></iframe>

## 3. Visualizing Images and Masks

Once we are done with changing the gns.py file,we can visualize our masks and images. You can do simply by following this [Visualize Dataset.ipynb](https://github.com/MLWhiz/object_detection/blob/master/guns_and_swords/1.%20Visualize%20Dataset.ipynb) notebook.

![](/images/weapons/8.png)

![](/images/weapons/9.png)

![](/images/weapons/10.png)

![](/images/weapons/11.png)

## 4. Train the MaskRCNN Model with Transfer Learning

To train the maskRCNN model, on the Guns and Swords dataset, we need to run one of the following commands on the command line based on if we want to initialise our model with COCO weights or imagenet weights:

    # Train a new model starting from pre-trained COCO weights
     python3 gns.py train — dataset=/path/to/dataset — weights=coco

    # Resume training a model that you had trained earlier
     python3 gns.py train — dataset=/path/to/dataset — weights=last

    # Train a new model starting from ImageNet weights
     python3 gns.py train — dataset=/path/to/dataset — weights=imagenet

The command with weights=last will resume training from the last epoch. The weights are going to be saved in the logs directory in the Mask_RCNN folder.

This is how the loss looks after our final epoch.

![](/images/weapons/12.png)

### Visualize the losses using Tensorboard

You can take advantage of tensorboard to visualise how your network is performing. Just run:

    tensorboard --logdir ~/objectDetection/Mask_RCNN/logs/gns20191010T1234

You can get the tensorboard at

    [https://localhost:6006](https://localhost:6006)

Here is how our mask loss looks like:

![](/images/weapons/13.png)

We can see that the validation loss is performing pretty abruptly. This is expected as we only have kept 20 images in the validation set.

## 5. Prediction on New Images

Predicting a new image is also pretty easy. Just follow the [prediction.ipynb](https://github.com/MLWhiz/object_detection/blob/master/guns_and_swords/2.%20predict.ipynb) notebook for a minimal example using our trained model. Below is the main part of the code.

<iframe src="https://medium.com/media/2377c842c5fea836a91aea682be87bd5" frameborder=0></iframe>

This is how the result looks for some images in the validation set:

![](/images/weapons/14.png)

![](/images/weapons/15.png)

## Improvements

The results don’t look very promising and leave a lot to be desired, but that is to be expected because of very less training data(60 images). One can try to do the below things to improve the model performance for this weapon detector.

1. We just trained on 60 images due to time constraints. While we used transfer learning the data is still too less — Annotate more data.

1. Train for more epochs and longer time. See how validation loss and training loss looks like.

1. Change hyperparameters in the mrcnn/config file in the Mask_RCNN directory. For information on what these hyperparameters mean, take a look at my previous post. The main ones you can look at:

    # if you want to provide different weights to different losses
    LOSS_WEIGHTS ={'rpn_class_loss': 1.0, 'rpn_bbox_loss': 1.0, 'mrcnn_class_loss': 1.0, 'mrcnn_bbox_loss': 1.0, 'mrcnn_mask_loss': 1.0}

    # Length of square anchor side in pixels
    RPN_ANCHOR_SCALES = (32, 64, 128, 256, 512)

    # Ratios of anchors at each cell (width/height)
    # A value of 1 represents a square anchor, and 0.5 is a wide anchor
    RPN_ANCHOR_RATIOS = [0.5, 1, 2]

## Conclusion

![Photo by [Christopher Gower](https://unsplash.com/@cgower?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)](/images/weapons/16.png)*Photo by [Christopher Gower](https://unsplash.com/@cgower?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

***In this post, I talked about how to implement Instance segmentation using Mask-RCNN for a custom dataset.***

I tried to make the coding part as simple as possible and hope you find the code useful. In the next part of this post, I will deploy this model using a web app. So stay tuned.

You can download the annotated weapons data as well as the code at [Github](https://github.com/MLWhiz/object_detection).

If you want to know more about various*** Object Detection techniques, motion estimation, object tracking in video etc***., I would like to recommend this awesome course on [Deep Learning in Computer Vision](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0) in the [Advanced machine learning specialization](https://www.coursera.org/specializations/aml?siteID=lVarvwc5BD0-AqkGMb7JzoCMW0Np1uLfCA&utm_content=2&utm_medium=partners&utm_source=linkshare&utm_campaign=lVarvwc5BD0).

Thanks for the read. I am going to be writing more beginner-friendly posts in the future too. Follow me up at [**Medium](https://medium.com/@rahul_agarwal)** or Subscribe to my [**blog](http://eepurl.com/dbQnuX)** to be informed about them. As always, I welcome feedback and constructive criticism and can be reached on Twitter [@mlwhiz](https://twitter.com/MLWhiz).

Also, a small disclaimer — There might be some affiliate links in this post to relevant resources as sharing knowledge is never a bad idea.
