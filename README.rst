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

TODO: output rss feed file for the files that were uploaded

TODO: Stream the download to get around the requirement to have download permissions on the emby/jellyfin server

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

