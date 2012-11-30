Is that french? Oui, monsieur! That means "This is a doorbell" and if it feels like a *Déjà vu* to you, you may have seen Magritte's famous painting [The Treachery of Images](https://en.wikipedia.org/wiki/Ceci_n%27est_pas_une_pipe)

This is indeed a working doorbell, using Twitter as a wire between the push-button and the bell. This is made possible with the help of a very small and pretty cheap computer: the [Raspberry Pi](http://www.raspberrypi.org). We used two Raspberry's here, one at each end of the wire: one does the knock and one does the ring.

This tutorial will cover everything to do that! We'll go through 

* writing the python scripts to tweet and monitor tweets using the Twitter API
* writing a log file with Python
* wrapping those scripts into daemons. Daemons are services that run in the background of your operating system. 
* build a ssh tunnel to monitor your raspberry when you're out of home, *without* doing some boring configuration in your router's interface to enable port forwarding

# What You'll Need

* 2 Raspberry Pi Model B
* 1 push-button (I found mine in an old doorbell system but you can use any simple push-button)
* 1 MTA connector and some wires
* 2 speakers (like some cheap usb powered speakers with a mini-jack)
* 2 ethernet cables to connect your raspberry pi's to your local network

# Getting started

## Get Raspbian on a SD card

Raspberry py comes has an SD card reader in place of a hard drive you'll find on a normal computer. However it works the same, your Raspberry Pi will lauch the Operating System on your SD card.
The Raspberry Pi Foundation has made available a version linux for the Raspberry Pi, it's a derivate of debian and is called Raspbian.
If you don't have a preloaded SD card with Raspbian, you need to download and write your SD card. The Raspberry Pi has written a [guide for beginners](http://elinux.org/RPi_Easy_SD_Card_Setup) that has instructions to write the SD card from Windows, OS X or Linux.

## Are you confortable with a terminal? ssh? vim? git?

In this tutorial, we will always connect to the raspberry's remotely using [ssh](https://en.wikipedia.org/wiki/Secure_Shell)

Our favourite text editor is vim. If you don't know vim yet, follow vim's own quick interactive tutorial by typing *vimtutor* in your terminal 

It's not mandatory to use git in this tutorial, but if you want to learn, follow the steps in [tryGit](http://try.github.com)

# Monitor a hashtag with the Twitter API
