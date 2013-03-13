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

Raspberry Pi has an SD card reader in place of a hard drive you'll find on a normal computer. However it works the same, your Raspberry Pi will lauch the Operating System on your SD card.
The Raspberry Pi Foundation has made available a version linux for the Raspberry Pi, it's a derivate of debian and is called Raspbian.
If you don't have a preloaded SD card with Raspbian, you need to download and write your SD card. The Raspberry Pi has written a [guide for beginners](http://elinux.org/RPi_Easy_SD_Card_Setup) that has instructions to write the SD card from Windows, OS X or Linux.

## Are you confortable with a terminal? ssh? vim? git?

In this tutorial, we will always connect to the raspberry's remotely using [ssh](https://en.wikipedia.org/wiki/Secure_Shell)

Our favourite text editor is vim. If you don't know vim yet, follow vim's own quick interactive tutorial by typing *vimtutor* in your terminal. But you're free to use emacs or nano. If you want a config file to get color syntax, correct tab width, etc.. you can use mine:
```
$ wget https://raw.github.com/emmanuelgeoffray/dotfiles/master/.vimrc
```

It's not mandatory to use git in this tutorial, but if you want to learn, follow the steps in [tryGit](http://try.github.com)

## Give ssh a try

Connect you Raspberry Pi to the network, and access it remotely via ssh. By default, the hostname is 'raspberrypi' and user/password is pi/raspberry
```
$ ssh pi@raspberrypi
```

If you don't have a DNS resolver on your network, you computer can't find raspberrypi.
You can use [avahi](https://en.wikipedia.org/wiki/Avahi_%28software%29).
Plug a keyboard and a screen to your Raspberry Pi, login and then install avahi-daemon
```
$ sudo apt-get update
$ sudo apt-get install avahi-daemon
```

You can now go back to your computer and run
```
$ ssh pi@raspberrypi.local
```

# Tweet from the Raspberry Pi

You toctoc will be tweeting from a twitter account. You can choose to use your own twitter account or create a new one [here](https://twitter.com/signup).

We will authenticate to Twitter using OAuth. The toctoc twitter application exists, so you can use it's consumer_key and consumer_secret. But if you want to register your own application, you can do that on [Twitter Developer Page](https://dev.twitter.com/apps/new).

# Get the python scripts to start tweeting

## Get the twitter library

```
$ sudo apt-get update
$ sudo apt-get install git python-dev python-pip vim mpg321
$ git clone https://github.com/sixohsix/twitter.git
$ cd twitter
$ sudo python setup.py install
$ cd ..
```

We have no all the tools to start tweeting!

## Get toctoc

```
$ git clone https://github.com/soixantecircuits/toctoc.git
$ cd toctoc
$ sudo sh install.sh toctoc
$ cd tests
$ sudo python tweet.py
```

You are now running the test script that tweets with your account. Nothing more. Nothing less.
As it's the first time you are tweeting within the application, you need to authorize it.
Follow the instructions: open your brower and copy the PIN code. 
That's it, you only have to do that once!

Congrats for your first tweet from your Raspberry Pi!
Let's try to wire a button to that now!

# Wire a button to the Raspberry Pi

## Solder a push-button

First find a push-button, that can be anything with two conductive parts that touches each other when you press on it.
You can get a simple button at your local electronic parts shop, or order it on [Adafruit](https://www.adafruit.com/index.php?main_page=adasearch&q=button).

Personaly, I recycled an old ringer button that was on the wall next to my door, and not wired to anything :)

Solder two wires on each plates of the button, and connect them to the Raspberry.

To connect to the raspberry, you can use an [Adafruit Pi Cobbler Breakout Kit for Raspberry Pi](http://adafruit.com/products/914). Or simply get two [jumper wires](http://adafruit.com/products/824).

Personaly, I used an MTA connector. I hate to solder small wires on tiny contacts, so MTA is good no-soldering solution and it is not too expensive. Get more info on [LinderLabs' Tips](http://linderlabs.wordpress.com/2010/01/24/basic-interconnection-pin-headers-mta-connectors-banana-jacks/). You can buy MTA connectors and the T-handle tool from [Farnell](http://www.farnell.com/)

Now, we have to figure out which pin to use. Look at the [drawing](http://4.bp.blogspot.com/-qiYvZxYWk8U/UND3TWrMMsI/AAAAAAAAAEI/Z6RtugmJ5_w/s1600/Raspberry-Pi-GPIO-Layout.png)
We can use any GPIO, but check GPIO14, it's next to GROUND, so it's going to be easy to wire the two cables next to each other. One on ground, the other one on GPIO14.

We'll use the internal pull up resistor to set GPIO14's default value to HIGH. If you press the button, the two plates will be connected, GPIO14 will be connected to GROUND and take the LOW value.

Let's try it with a test script!

## Test your button

Install the Raspberr PY GPIO library:
```
sudo pip install RPi.GPIO
```

Run the test script

```
$ sudo python push-button.py
```

Press the button, and see a cross between the brackets, yay!
Plug some speakers to the Pi and you'll hear a sound too, wouhou!
Press Ctrl+C to close.

# Run toctoc as a daemon

Install the python daemon library

```
$ cd
$ git clone https://github.com/serverdensity/python-daemon.git
$ sudo cp python-daemon/daemon.py /usr/local/lib/python2.7/dist-packages/
```


We can tweet. We can push a button. We have both run together in the toctoc script.
Check it out here:

```
$ sudo vim /usr/share/toctoc/toctoc.py
```

You can edit it for you own convenience. Remember that you can't tweet twice the same message!
And then start the daemon:

```
$ sudo service toctoc start
```

The toctoc service will now start each time you power your Raspberry Pi.

# What's going on with the daemon? What is it doing?

A daemon is running in the background, so it's pretty hard to know what it's doing. How can you know there is a bug with the network? That your account is not allowed to tweet anymore...
No worries, check the log:

```
$ tail -f /var/log/toctoc/toctoc.log
```

Press Ctrl+C to close.

# Remotely connect

You're in a local network with your Raspberry Pi now. You know how to do a ssh pi@raspberrypi.
But what if you want to connect to it from a remote location. Your office, your home, in the bus...
Well, you can do some annoying port forwarding in your router.
Or you can simply open a ssh tunnel from the raspberry to a computer you know is always connected, e.g. a server.
You can do a ssh to your server and then ssh from that server to your raspberry.

We got you covered, the install.sh script installed this for you, but now you need to edit the script for your server.

```
sudo vim /etc/init.d/autossh_tunnel 
```

Set you server's adress, ssh port, your login, etc.
Give a port number. It will be used to connect from your server.
The default value is 60000.
Number your ports with a step of 3, ie. host1: port 60000 for the tunnel, 60001 and 60002 will be used for autossh monitoring
host2: port 60003, 60004 and 60005 will be used for port monitoring, etc.

## Register your Raspberry Pi to allow connecting it to your server:

```
ssh-keygen -t rsa -C "$(whoami)@$(hostname)-$(date -I)"
ssh-copy-id 'username@remote-server.org -p 22'
```

Press enter for both questions.


Test that the info you entered in autossh_tunnel are corrects:
```
 ssh -p SERVERPORT -R TUNNELPORT:localhost:22 -f -N RUSER@RSERVER
```

Try to connect from your server:

```
$ ssh you@yourserver
$ ssh pi@localhost -p 60000
```

If everything is okay, you can run the daemon,
```
$ sudo service autossh_tunnel start
```

If
tail -f /var/log/syslog | grep autossh






#TODO

* script to test tweet
* script to test button
* add git etc to the script install.sh
* get the tools first in the overview
