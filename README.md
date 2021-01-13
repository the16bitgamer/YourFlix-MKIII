# YourFlix-MKIII

Update 2020-09-27: YourFlix MKIII is now in Beta!

Update 2020-10-16: Added a Wiki to install and configure YourFlix for a Raspberry Pi https://github.com/the16bitgamer/YourFlix-MKIII/wiki

# What is YourFlix?

As an idea, YourFlix is a tool to let you watch _your_ _flicks_. Now this can be done with just a neatly organized file folder system, but that's not what I've done.

YourFlix MKIII is a combination of open source server programs (Apache 2.0, MiniDlna, OpenSSH), server side scripts (Python, PHP), and Web Code, to allow you to watch _your_ _flicks_ on your devices.

The Web Site is designed to run on **Apache 2.0**, so it can be compatible with almost every device with a web browser that can play Videos, Apache 2.0 also handles the Video Stream so we don't need an adition stream client.

If you have some older devices which cannot run a Web Browser that can play Videos, this is where **MiniDlna** comes in and can be used to stream your Videos.

**PHP** is used to handle Database requests to dynamically build the Website (don't forget php-sqlite3)

**Python3** is used to automate building and populating the database. I have an install Python Script located in the **YourFlix Setup** folder. This will install and configure a systemctl service called *yourflix.service*. This code will automatically build, update, and maintain the yourflix database. Adding/Updating/Removing files and folders as you use it. The *yourflix.service* is designed to start on boot. (python3-pip, with pip3 install pysqlite3 & inotify)

**Web Code** the web code designed for YourFlix is a creation of my own. Designed in React it will take the structure of created by the database and present it to you in a (in my view) nice and easy to understand UI. It has a search feature!

You'll also need to enable Apache2 RewriteEngine in /etc/httpd/conf.d\vhosts.conf

# What do you need to Run YourFlix?

I've designed this code to run on a Raspberry Pi 3 without a cooling fan, so if it's about as powerful as that it should handle it, if you are looking for specs:

- CPU 1.2GHz

- RAM 1GB

- Ethernet with atlease 100Mbps

- OS Debian or a fork of it

- Storage Min 4MB - Recomended Portable Storage 4TB - Recomended total storage 8TB

# Can you Bring YourFlix with you?

Yes and no. YourFlix is designed to be a local media streaming solution. Meaning that it's not designed to be exposed to the outside world, though if you know how to set up a VPN you're good to go.

But a VPN isn't the only way YourFlix can be mobile. If you are running a Raspberry Pi, you can reverse the WiFi and use it not only as a WiFi hot spot, but also as a means so stream YourFlix, any where you go. With a 5000mah battery you can run YourFlix for around 4 hours.

# What Video Files is YourFlix compatible with?

Whatever HTML5/MiniDlna is compatible with. I have it set up in the YourFlix config to handle the most common HTML5 video types, mp4, WebM, and Ogg. Though it theoretically can handle MKV if you have the right streaming server.

# How do I install YourFlix?

Follow the guide in the [Install Guide](https://github.com/the16bitgamer/YourFlix-MKIII/tree/master/Install%20Guide). I will be updating it as more features are added in.

[Or checkout the Wiki if you want hyperlinks](https://github.com/the16bitgamer/YourFlix-MKIII/wiki)
