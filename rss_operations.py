from feedgen.feed import FeedGenerator
from siaskynet import Skynet


def write_rss(medias_with_sialinks, id, title, link, description, contributor, subtitle, upload_skynet) -> str:
    # TODO add <media:group> so that if a media item exists multiple times they are included in the same group
    # i.e. 480p, 720p, 1080p, 4k
    # TODO include actors as contributors to a media item
    # TODO include link to artwork for media as an RSS enclosure
    fg = FeedGenerator()
    fg.load_extension('media', atom=True, rss=True)
    fg.id(id)
    fg.title(title)
    fg.link(href=link)
    imdb_badge =
    description = description + '\n' +
    fg.description(description)
    fg.contributor(name=contributor)
    fg.subtitle(subtitle)
    for media in medias_with_sialinks:
        fe = fg.add_entry()
        fe.id(media.imdb_id)
        fe.title(media.name)
        fe.summary(media.description)
        fe.link(href=media.skylink)
        fe.media.content({'url': media.skylink,
                          'fileSize': str(media.size),
                          'type': media.mime_type,
                          'medium': media.media_type,
                          #                          'isDefault':'',
                          'expression': 'full',
                          'bitrate': str(media.totalbitrate),
                          'framerate': str(media.framerate),
                          'samplingrate': str(media.samplingrate),
                          'channels': str(media.channels),
                          'duration': str(media.duration_in_sec),
                          'height': str(media.height),
                          'width': str(media.width),
                          'lang': media.lang})

        fe.media.thumbnail({'url': media.skylink_image,
                            'height': '264',
                            'width': '176'})

    atomfeed = fg.atom_str(pretty=True)  # Get the ATOM feed as string
    fg.atom_file('atom.xml')  # Write the ATOM feed to a file
    # upload file to skynet
    if upload_skynet is True:
        skylink = Skynet.upload_file('atom.xml')
        return skylink
    else:
        return ''
