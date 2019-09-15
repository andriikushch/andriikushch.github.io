---
layout: post
title:  "Transfer learning for traffic light detection"
date:   2019-09-15 12:00:09 +0200
categories: transfer learning traffic light detection
---

## Transfer learning

Transfer learning is one of the technics which can be in use while doing the machine learning that allows using already trained models to solve similar problems. For instance, given the model which can detect the traffic lights, we want to distinguish between traffic lights color.

## Environment

To complete a given task, we need to have a proper environment with GPU support. Possible solution providers might be Google Cloud or AWS.

If you don't have one, you still can try to do it with CPU on your local machine, but in most of the cases, this is not a very good idea, because it can take a lot of time.

## Installation

As the starting point, we can use the following repo. The full tutorial is [here](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md). Please consider to use python2 instead of python3, because a lot of examples are for python2.

## Try it

To see the object detection in action, we will need the Jupyter Notebook. When you have it, open the `models/research/object_detection/object_detection_tutorial.ipynb` and go through the book to see that you have all the necessary modules.

I used my image to see what current model can detect on the given image, for sure you can use yours:

![basic_network_recognition](/assets/images/basic_network_recognition.png)

As we see detected traffic light has a generic "traffic light" label. This result is what we want to change.

## Image labeling 

To retrain the model, we need to prepare the training data. For that, we can use any public data set like:

1. [https://www.uni-ulm.de/en/in/driveu/projects/driveu-traffic-light-dataset](https://www.uni-ulm.de/en/in/driveu/projects/driveu-traffic-light-dataset)
2. [https://www.kaggle.com/mbornoe/lisa-traffic-light-dataset](https://www.kaggle.com/mbornoe/lisa-traffic-light-dataset)

Or we can create our own. If you decide to go this way,  this process can be done in an automated way or manually. In case if we would like to do it manually, there are some tools which can help us, for example [https://github.com/opencv/cvat](https://github.com/opencv/cvat). Here is a screenshot of cvat UI:

![label_creation](/assets/images/label_creation.png)

I like this tool because there is a possibility to run it inside a docker container without any extra installation steps, and it is easy to use.

After you finish, you can export results as `COCO JSON` format. And convert to TFRecords with `research/object_detection/dataset_tools/create_coco_tf_record.py` from the `tensorflow/models` repository.

## Learning 

This step is a crucial part of the whole process. At this step, we need to retrain our model to learn what is a traffic light color is. Luckily a lot of people did it already, and we can use their experience. One of the possible ways how to do it using Google Cloud is described [here](https://medium.com/tensorflow/training-and-serving-a-realtime-mobile-object-detector-in-30-minutes-with-cloud-tpus-b78971cf1193).

You need to adjust the process for your needs, and that's all. In the end, you will have a new model which then you can use for your needs.

The precision and speed of learning depend on your model setting. If you want to read more about, this might be a good starting point: [detection_model_zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

## Validate and visualize the result

At the last step you, probably would like to see your new model in action, for that, we can use an already familiar `ipynb` file [here](https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb). You will need to change a few things there:
 1. Test image 
 2. Path to your labels map
 3. Path to the newly created frozen graph

For my example result looks like this:

![green_detection](/assets/images/green_detection.png)

Looks pretty good!


## Conclusion

This article was a brief overview of resources and approaches to transfer learning using existing AI tools. How, without an in-depth knowledge of Cloud Computing and Deep Learning in a short time, you can create an outstanding production-ready solution. Area of application is limited only by the imagination and passion for learning and creating.

Thank you for reading and I wish you all the best!