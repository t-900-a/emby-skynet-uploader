from configurator.mediaserver import mediaServer_config
from mediaServer.server import MediaServer
from mediaServer.item import Item
import logging
import argparse
from datetime import *
import hashlib
from file_operations import download_then_upload
from rss_operations import write_rss

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

parser.add_argument('--rss_id', dest='rss_id', default=hashlib.md5(bytes(datetime.now().__str__(), "ascii")).hexdigest()[:8], type=str,
                    help="Id for your channel"
                        " i.e. 4c6ca4f7")

parser.add_argument('--rss_title', dest='rss_title', default=None, type=str,
                    help="The name of your rss channel, if none is specified an rss feed will not be generated"
                        " i.e. anon's Media")

parser.add_argument('--rss_link', dest='rss_link', default='sia://fALzGYpbWAhwBu3Qs5z0MUbTbBUQ117rnERnqlRmaR-HiA',
                    type=str, help="Include a link if you would like your site to be referenced")

parser.add_argument('--rss_description', dest='rss_description', default='Information wants to be free',
                    type=str, help="Choose the description of the feed")

parser.add_argument('--rss_contributor', dest='rss_contributor', default='anon',
                    type=str, help="Specify a contributor")

parser.add_argument('--rss_subtitle', dest='rss_subtitle', default='',
                    type=str, help="Addition comment for your site if you want it"
                                   "i.e. For more content, please donate _cryptocurrency_symbol to _cryptocurrency_address")

args = parser.parse_args()
# TODO add argument for the script to choose between local or remote file operations
# TODO Add support for tv shows and anime
# you'll need to add a function for direct upload within file_operations.py
# i.e. if your the server admin, you want to use the full path as there is no need to download from your server
# i.e. if your a user, you want to download the file from the remote server, then upload to skynet
def main():
    medias_with_sialinks = []
    config = mediaServer_config(cfg_file=args.media_server_config)
    try:
        mediaserver = MediaServer(config)
    except Exception as inst:
        _log.critical(inst)

    if args.import_all == True:
        medias = mediaserver.get_items(include_item_types=args.media_type_to_upload, recursive="true", fields="Path")
        for item_to_upload in medias:
            item_with_sialink = download_then_upload(mediaserver, item_to_upload)
            medias_with_sialinks.append(item_with_sialink)

    if args.item_id_to_upload is not None:
        item_to_upload = mediaserver.get_item(int(args.item_id_to_upload), fields="Path,MediaSources")
        item_with_sialink = download_then_upload(mediaserver, item_to_upload)
        medias_with_sialinks.append(item_with_sialink)

    if args.date_created is not None:
        medias = mediaserver.get_items(include_item_types=args.media_type_to_upload, sort_by="DateCreated",
                                       sort_order="Descending", recursive="true", fields="DateCreated%2C%20Path")

        for item_to_upload in medias:
            if (datetime.strptime(item_to_upload.date_created[:10], '%Y-%m-%d') >= datetime.strptime(args.date_created, '%Y-%m-%d')):
                item_with_sialink = download_then_upload(mediaserver, item_to_upload)
                medias_with_sialinks.append(item_with_sialink)
            else:
                break

    if args.rss_title is not None:
        write_rss(medias_with_sialinks, args.rss_id, args.rss_title, args.rss_link,
                  args.rss_description, args.rss_contributor, args.rss_subtitle)

    exit(0)



if __name__ =="__main__":
    main()
