from configurator.mediaserver import mediaServer_config
from mediaServer.server import MediaServer
from mediaServer.item import Item
from siaskynet import Skynet
import logging
import os
import argparse
from datetime import *

_log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Process mediaserver files and upload to skynet')
parser.add_argument('--datecreated', dest='date_created', default=None, type=str,
                    help=f"iso-8601 date format i.e. {date.today()}"
                         " all media that was created on or after that date will be uploaded to skynet")
parser.add_argument('--itemid', dest='item_id_to_upload',default=None, type=int, help="the itemid from emby/jellyfin"
                                                             "that you would like to upload to skynet")
parser.add_argument('--all',
                    default=False, dest='import_all', action='store_const', const=True,
                    help="include this argument if you would like to upload all media found on the server to skynet")

parser.add_argument('--mediatype', default="Movie,Episode",
                    dest='media_type_to_upload', type=str,
                    help="specify the type of media from the media server you would like to upload"
                         " i.e. Movie"
                         " default: Movie,Episode")
parser.add_argument('--mediaserverconfig', dest='media_server_config', default='mediaserver-config.json', type=str,
                    help="config file for the emby/jellyfin server connection"
                         " file will be generated if none exists")

args = parser.parse_args()

def download_then_upload(mediaserver, item_to_upload):
    print(f"Downloading item: # {item_to_upload.id} - {item_to_upload.name}")
    try:
        file_to_upload = mediaserver.download_item(item_to_upload)
    except Exception as inst:
        _log.critical(inst)

    print(f"Uploading file to skynet: {file_to_upload}")
    try:
        skylink = Skynet.UploadFile(file_to_upload)
        print(f"Media is now available on skynet: {skylink}")
    except Exception as inst:
        _log.critical(inst)

    try:
        clean_up(file_to_upload)
    except Exception as inst:
        _log.critical(inst)

def clean_up(file):
    os.remove(file)
    exit(0)

def main():
    config = mediaServer_config(cfg_file=args.media_server_config)

    try:
        mediaserver = MediaServer(config)
    except Exception as inst:
        _log.critical(inst)

    if args.import_all == True:
        medias = mediaserver.get_items(include_item_types=args.media_type_to_upload, recursive="true", fields="Path")
        for item_to_upload in medias:
            download_then_upload(mediaserver, item_to_upload)
        exit(0)

    if args.item_id_to_upload is not None:
        item_to_upload = Item(id=args.item_id_to_upload)
        download_then_upload(mediaserver, item_to_upload)
        exit(0)

    if args.date_created is not None:
        medias = mediaserver.get_items(include_item_types=args.media_type_to_upload, sort_by="DateCreated",
                                       sort_order="Descending", recursive="true", fields="DateCreated%2C%20Path")

        for item_to_upload in medias:
            if (datetime.strptime(item_to_upload.date_created[:10], '%Y-%m-%d') >= datetime.strptime(args.date_created, '%Y-%m-%d')):
                download_then_upload(mediaserver, item_to_upload)
            else:
                break
        exit(0)



if __name__ =="__main__":
    main()
