from bs4 import BeautifulSoup
import codecs

class TagNotPError(Exception):
    pass
class TagNotUlError(Exception):
    pass
class TagNotCenterError(Exception):
    pass
class NoImgFoundError(Exception):
    pass

def p_handler(p_tag, logger):
    if p_tag.name != 'p':
        raise TagNotPError('Received a tag which is not <p>.')
    
    content = p_tag.contents[0].strip().replace('$$$', '$')
    return content

def ul_handler(ul_tag, logger):
    if ul_tag.name != 'ul':
        raise TagNotUlError('Received a tag which is not <ul>.')

    ul_contents = [
        '- ' + item.contents[0].strip().replace('$$$', '$')
        for item
        in ul_tag.find_all('li')
    ]
    
    return ul_contents

def img_handler(center_tag, logger):
    if center_tag.name != 'center':
        raise TagNotCenterError('Received a tag which is not <center>.')

    img_tags = center_tag.find_all(name='img', attrs={"class": "tex-graphics"})
    if len(img_tags) < 1:
        raise NoImgFoundError
    img_src = img_tags[0].get('src')

    caption_tags = center_tag.find_all(name='span', attrs={"class": "tex-font-size-small"})
    if len(caption_tags) < 1:
        caption_contents = []
    else:
        caption_contents = [
            item.contents[0].strip().replace('$$$', '$')
            for item
            in caption_tags
        ]
    
    if len(caption_contents) < 1:
        img_md = '![]({src})'.format(img_src)
    else:
        img_md = '''<figure>
          <img src="{src}" alt="">\n'.format(img_src)
          <figcaption>{cap}</figcaption>\n'.format(caption_contents[0])
        </figure>'''
    
    return img_md