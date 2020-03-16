Script for uploading to skynet
===============================

Script to upload media files from a jellyfin or emby server to skynet

* release 0.1
* open source: https://github.com/t-900-a/jellyfin-skynet-uploader
* Jellyfin is the FREE & OPEN SOURCE media player
* works with Jellyfin 10 and Emby 4.*
* Python 3.x compatible
* What is skynet?
* * It's a decentralized CDN: https://siasky.net/

Copyrights
----------

Released under the BSD 3-Clause License. See `LICENSE.txt`_.

Copyright (c) 2020 t-900-a

.. _`LICENSE.txt`: LICENSE.txt

Want to help?
-------------

Merge requests are invited

There are many todo's in the code

TODO: Stream the download to get around the requirement to have download permissions on the emby/jellyfin server
TODO: Include additional information into the rss feed i.e. genre, actors, imdb rating, etc

Available Scripts
-----------------
* uploader.py : Media Uploader
* * Description: Script used to upload your media library items to skynet to share with the world

Parameters
----------
* --datecreated
* * iso-8601 date format i.e. 2020-03-08
* * all media that was created on or after that date will be uploaded to skynet
* --itemid
* * the itemid from emby/jellyfin that you would like to upload to skynet
* --all
* * include this argument if you would like to upload all media found on the server to skynet
* --mediatype
* * i.e. Movie
* * default: Movie,Episode
* * specify the type of media from the media server you would like to upload"
* --mediaserverconfig
* * config file for the emby/jellyfin server connection
* * script will prompt you via the command line for your current media server information (IP/PORT/ADMIN user)
* * file will be generated if none exists

* RSS related parameters
* * --rss_id
* * * Id for your channel
* * * default: random characters
* * --rss_title
* * * The name of your rss channel, if none is specified an rss feed will not be generated
* * * i.e. anon's Media
* * * Only required parameter to produce a rss atom feed
* * --rss_link
* * * Include a link if you would like your site to be referenced
* * * i.e. https://www.mysharedmedia.com/jellyfin/
* * --rss_description
* * * Choose the description of the feed
* * --rss_contributor
* * * Choose the description of the feed
* * --rss_subtitle
* * * Addition comment for your site if you want it
* * * i.e. For more content, please donate _cryptocurrency_symbol to _cryptocurrency_address

Usage
-----------

Presteps:
a. Have a jellyfin/emby server available with media on it.
b. Have an account with download permissions on that server. (Don't have to be an admin)

1. Clone the repo

2. Create virtualenv & activate it

.. code-block:: bash

    python3 -m venv .venv
    source .venv/bin/activate

3. Install dependencies

.. code-block:: bash

    pip install -r requirements.txt -r test_requirements.txt

4. python uploader.py --all

4a. The script may ask you for command line input

Examples
-------------
* Upload movies that were added to emby/jellyfin today (you could add this as a cron job to continually share to skynet)

.. code-block:: bash

    python uploader.py --datecreated `date --iso-8601` --mediatype "Movie"
    read config media server
    ./cfg/mediaserver-config.json read successfully
    Configuring media server connection...
    Admin user Password needed to continue:
    Downloading item: # 5 - Big Buck Bunny
    Uploading file to skynet: big_buck_bunny_480p_surround-fix.avi
    Media is now available on skynet: sia://AAApJJPnci_CzFnddB076HGu1_C64T6bfoiQqvsiVB5XeQ

* Upload all TV episodes

.. code-block:: bash

    python uploader.py --all --mediatype "Episode"

* Example RSS Feed

.. code-block:: xml

    <?xml version='1.0' encoding='UTF-8'?>
    <feed xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">
    <id>7371fbee</id>
    <title>Open source Movie Feed</title>
    <updated>2020-03-16T02:51:23.343056+00:00</updated>
    <link href="sia://fALzGYpbWAhwBu3Qs5z0MUbTbBUQ117rnERnqlRmaR-HiA"/>
    <contributor>
        <name>t-900</name>
    </contributor>
    <generator uri="https://lkiesow.github.io/python-feedgen" version="0.9.0">python-feedgen</generator>
    <entry>
        <id>5</id>
        <title>Big Buck Bunny</title>
        <updated>2020-03-16T02:51:23.343951+00:00</updated>
        <link href="sia://AAApJJPnci_CzFnddB076HGu1_C64T6bfoiQqvsiVB5XeQ" rel="alternate"/>
        <media:group>
            <media:content url="sia://AAApJJPnci_CzFnddB076HGu1_C64T6bfoiQqvsiVB5XeQ" fileSize="220514438" type="video/x-msvideo" medium="Video" expression="full" bitrate="2500431" framerate="24" samplingrate="48000" channels="6" duration="596.458" height="480" width="854"/>
        </media:group>
    </entry>
    </feed>


Integration Ideas
-----------------

Get multiple emby/jellyfin server admins together and have each admin create an rss feed on their own server.
Then have a centralized server that index and makes the media searchable.
This project could be used as an inspiration: https://www.datorss.com/
https://github.com/davidesantangelo/datorss
