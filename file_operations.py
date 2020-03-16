from mediaServer.item import Item
from siaskynet import Skynet
import os
import logging

_log = logging.getLogger(__name__)

def clean_up(file):
    os.remove(file)

def download_then_upload(mediaserver, item_to_upload) -> Item:
    print(f"Downloading item: # {item_to_upload.id} - {item_to_upload.name}")
    try:
        file_to_upload, content_type = mediaserver.download_item(item_to_upload)
    except Exception as inst:
        _log.critical(inst)
    # TODO upload subtitle files for the media
    # TODO upload artwork for media i.e. album cover, movie poster, etc
    print(f"Uploading file to skynet: {file_to_upload}")
    try:
        skylink = Skynet.UploadFile(file_to_upload)
        print(f"Media is now available on skynet: {skylink}")
    except Exception as inst:
        _log.critical(inst)

    try:
        setattr(item_to_upload, "skylink", skylink)
        setattr(item_to_upload, "size", os.path.getsize(file_to_upload))
        setattr(item_to_upload, "mime_type", content_type)
        return item_to_upload
    except Exception as inst:
        _log.critical(inst)

    try:
        clean_up(file_to_upload)
    except Exception as inst:
        _log.critical(inst)