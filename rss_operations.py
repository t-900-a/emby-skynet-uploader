from feedgen.feed import FeedGenerator
import siaskynet as skynet
import requests

def rewrite_skylink(skynet_instance, skylink):
    if skynet_instance is not None and skylink[6:] == 'sia://':
        return skylink.replace('sia://', skylink)
    else:
        return skylink

def write_rss(medias_with_sialinks, id, title, link, description, contributor, subtitle, skynet_instance) -> str:
    # TODO add <media:group> so that if a media item exists multiple times they are included in the same group
    # i.e. 480p, 720p, 1080p, 4k
    # TODO include actors as contributors to a media item
    fg = FeedGenerator()
    fg.load_extension('media', atom=True, rss=True)
    fg.id(id)
    fg.title(title)
    fg.link(href=rewrite_skylink(link))
    fg.description(description)
    fg.contributor(name=contributor)
    fg.subtitle(subtitle)
    for media in medias_with_sialinks:
        fe = fg.add_entry()
        fe.id(media.imdb_id)
        fe.title(media.name)
        fe.summary(media.description)
        fe.link(href=rewrite_skylink(media.skylink))
        # TODO add critic rating to xml tags
        fe.media.content({'url': rewrite_skylink(media.skylink),
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

        fe.media.thumbnail({'url': rewrite_skylink(media.skylink_image),
                            'height': '264',
                            'width': '176'})
        # build summary
        # TODO figure out embedding an svg for the imdb rotten tomatoes logo and the associated rating
        # imdb_rating = '7.8'
        # imdb_badge = requests.get(
        #     f"https://img.shields.io/static/v1?"
        #     f"label=Imdb&message={imdb_rating}&color=gold"
        #     f"&logo=imdb&link=https://www.imdb.com/title/{media.imdb_id}/").text
        # tomatoe_score = '74'
        # rotten_tomatoes_base64_png = 'data:image/png;base64,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'
        # rotten_tomatoes_badge = requests.get(
        #     f"https://img.shields.io/static/v1?"
        #     f"label=Rotten%20Tomatoes&message={tomatoe_score}%"
        #     f"&color=red&logo={rotten_tomatoes_base64_png}"
        # ).text
        # description_with_ratings = media.description + '\n' + '<![CDATA[' + imdb_badge + rotten_tomatoes_badge + '</html>]]>'
        # fe.summary(description_with_ratings)

    atomfeed = fg.atom_str(pretty=True)  # Get the ATOM feed as string
    fg.atom_file('atom.xml')  # Write the ATOM feed to a file
    # upload file to skynet
    if skynet_instance is not None:
        skylink = skynet.upload_file('atom.xml')
        print(f'RSS feed is now available on skynet: {skylink}')
        return skylink
    else:
        return ''
