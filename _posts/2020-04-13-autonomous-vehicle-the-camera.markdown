---
layout: post
title:  "Autonomous vehicle: The Camera"
date:   2020-04-13 12:00:09 +0200
categories: posts
---

After the implementation of the speed control in the last [article](https://andriikushch.com/posts/2020/04/05/autonomous-vehicle-the-speed.html), the next logical step is to add some perception to the RC car. I have two cameras which I could use fo this purpose: 

1. Regular USB WebCam
2. Raspberry Pi Camera

## Goal

Add a possibility to drive an RC vehicle from the first-person view using the camera.

## Plan

The plan is the following:

{:.text-align-center}
![dia1.png](/assets/images/3/dia1.png)

1. Connect a camera to the Raspberry Pi
2. Expose video stream via HTTP
3. Connect via browser to the Raspberry Pi and enjoy driving.
4. Enjoy the result.

## Configuring

### Connect

There is no problem with connecting USB WebCam to the RC car. After plugging it to the free USB port, OS should recognize it.

In the case of the Raspberry Pi camera, there are few extra steps required:

1. In the terminal, run `sudo raspi-config`
2. Follow the instructions and reboot after:

![step1.png](/assets/images/3/step1.png)

![step2.png](/assets/images/3/step2.png)

{:.text-align-center}
![step3.png](/assets/images/3/step3.png)


### Transmit
 
Looking for the solution, how to expose video stream from the USB cam via HTTP, I found this repo [mjpg-streamer](https://github.com/jacksonliam/mjpg-streamer). It provides exactly the functionally I need. If you also want to use it, please check the documentation at the repo's web page. Or you can follow the commands I wrote bellow if you only want to install and start using it right now.

From the Raspberry Pi terminal run:

```
sudo apt-get update 
sudo apt-get install cmake libjpeg8-dev libgphoto2-dev gcc g++
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
make
sudo make install
export LD_LIBRARY_PATH=.
```
If you use USB web cam:

```
./mjpg_streamer -o "output_http.so" -i "input_uvc.so"
```
For Raspberry Pi camera:

```
./mjpg_streamer -o "output_http.so" -i "input_raspicam.so"
```

In my case, the output is the following:

```
... some output omitted
 o: www-folder-path......: disabled
 o: HTTP TCP port........: 8080
 o: HTTP Listen Address..: (null)
 o: username:password....: disabled
 o: commands.............: enabled
```

Now on your PC, which should be in the same network as Raspberry PI, open browser and navigate to the URL:

```
http://<YOUR_RASPBERRY_PI_IP_ADDRESS>:8080/?action=stream
```

There you should see the video stream from the camera.

{:.text-align-center}
![anim.gif](/assets/images/3/anim.gif)
## Conclusion

Just with a few simple steps, you can turn your RC car into an FPV RC car.
