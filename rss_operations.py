from feedgen.feed import FeedGenerator

def write_rss(medias_with_sialinks, id, title, link, description, contributor, subtitle):
    # TODO add <media:group> so that if a media item exists multiple times they are included in the same group
    # i.e. 480p, 720p, 1080p, 4k
    # TODO include actors as contributors to a media item
    # TODO include link to artwork for media as an RSS enclosure
    fg = FeedGenerator()
    fg.load_extension('media', atom=True, rss=True)
    fg.id(id)
    fg.title(title)
    fg.link(link)
    fg.description(description)
    fg.contributor(name=contributor)
    fg.subtitle(subtitle)
    for media in medias_with_sialinks:
        fe = fg.add_entry()
        fe.id(media.id)
        fe.title(media.name)
        fe.summary(media.overview)
        fe.link(href=media.skylink)
        fe.media.content({'url': media.skylink,
                          'fileSize': media.size,
                          'type': media.mime_type,
                          'medium': media.media_type,
#                          'isDefault':'',
                          'expression':'full',
        # TODO rss media elements below bitrate
                          'bitrate':'10',
                          'framerate':'30',
                          'samplingrate':'180',
                          'channels':'2',
                          'duration':'1000',
                          'height':'480',
                          'width':'480',
         # TODO jellyfin-python.item doesn't return language of the media
         # https://emby.media/community/index.php?/topic/83733-retrieving-the-language-for-a-video-item/
                          'lang':'en'})