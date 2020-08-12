from mediaServer.item import Item
from siaskynet import Skynet
import os
import logging
import ffmpeg

_log = logging.getLogger(__name__)


def clean_up(file):
    os.remove(file)


def download_then_upload(mediaserver, item_to_upload: Item, compression_size) -> Item:
    print(f"Downloading item: # {item_to_upload.id} - {item_to_upload.name}")
    try:
        downloaded_file, content_type = mediaserver.download_item(item_to_upload)
    except Exception as inst:
        _log.critical(inst)


    if compression_size:
        # item_to_upload.size is in bytes
        # compression_size is in megabytes
        if item_to_upload.size > compression_size * 1000000:
            file_to_upload = downloaded_file[:-4] + ".webm"
            print(f'{downloaded_file} file larger than skynet file size limit: Compressing before upload')
            print('THIS WILL TAKE A LONG TIME')
            # determine target bitrate (bits / sec)
            bitrate = (compression_size * 1000000 * 8) / item_to_upload.duration_in_sec
            ffmpeg.input(downloaded_file).\
                output(file_to_upload,
                       **{'c:v': 'libaom-av1'}, # file size small, slower encoding
                       # **{'c:v': 'libvpx-vp9'}, # file size too large, quicker encoding
                       **{'b:v': bitrate},
                       **{'strict': '-2'},
                       **{'cpu-used': '8'})\
                .run()
            file_to_upload_size = os.path.getsize(file_to_upload)
        else:
            file_to_upload = downloaded_file
            file_to_upload_size = item_to_upload.size
            bitrate = item_to_upload.totalbitrate / item_to_upload.duration_in_sec
    else:
        file_to_upload = downloaded_file
        file_to_upload_size = item_to_upload.size
        bitrate = item_to_upload.totalbitrate / item_to_upload.duration_in_sec


    # TODO upload subtitle files for the media
    # TODO upload artwork for media i.e. album cover, movie poster, etc
    print(f"Uploading file to skynet: {file_to_upload}")
    try:
        #skylink = Skynet.upload_file(file_to_upload)
        skylink = 'sia://AABj-Y4c2udHrr3h6-oufMlw_J-emE7_G3CTN1E1ulhP_A'
        print(f"Media is now available on skynet: {skylink}")
    except Exception as inst:
        _log.critical(inst)

    # upload primary image for item
    try:
        image_file = mediaserver.download_item_image(item_to_upload, width=176, height=264)
        print(image_file)
    except Exception as inst:
        _log.critical(inst)

    try:
        # skylink_image = Skynet.upload_file(image_file)
        skylink_image = 'sia://vAFrKIUSUBoGPb0wQZ1QK9INQDnx2M4yiPj-oc_dhTFlqQ'
        print(f"Primary Image is now available on skynet: {skylink_image}")
    except Exception as inst:
        _log.critical(inst)

    try:
        # clean up the compressed file
        clean_up(file_to_upload)
        if file_to_upload != downloaded_file:
            # clean up the uncompressed file if need be
            clean_up(downloaded_file)
        # clean up the primary image
        clean_up(image_file)
    except Exception as inst:
        _log.critical(inst)

    try:
        setattr(item_to_upload, "skylink", skylink)
        setattr(item_to_upload, "size", file_to_upload_size)
        setattr(item_to_upload, "mime_type", content_type)
        setattr(item_to_upload, "bitrate", bitrate)
        setattr(item_to_upload, "skylink_image", skylink_image)
        return item_to_upload
    except Exception as inst:
        _log.critical(inst)


