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
    
    # logger.debug(len(p_tag.contents))
    # logger.debug(p_tag.contents)
    # content = p_tag.contents[0].strip().replace('$$$', '$')

    content_list = []
    for index, item in enumerate(p_tag.contents):
        if hasattr(item, 'get') == False:
            tmp_str = item.strip().replace('$$$', '$')
            if index > 0:
                tmp_str = ' ' + tmp_str
            content_list.append(tmp_str)
        else:
            item_span_class = item.get('class')
            if item_span_class[0] == 'tex-font-style-tt':
                tmp_str = '$\\texttt{' + item.contents[0].strip().replace('$$$', '$') + '}$'
                if index > 0:
                    tmp_str = ' ' + tmp_str
                content_list.append(tmp_str)
            elif item_span_class[0] == 'tex-font-style-bf':
                tmp_str = '**' + item.contents[0].strip().replace('$$$', '$') + '**'
                if index > 0:
                    tmp_str = ' ' + tmp_str
                content_list.append(tmp_str)
            elif item_span_class[0] == 'tex_font_style-it':
                tmp_str = '*' + item.contents[0].strip().replace('$$$', '$') + '*'
                if index > 0:
                    tmp_str = ' ' + tmp_str
                content_list.append(tmp_str)
            else:
                logger.debug('=================')
                logger.debug(item_span_class)
                logger.debug(item.contents[0])
    
    content = ''.join(content_list)
    return content

def ul_handler(ul_tag, logger):
    if ul_tag.name != 'ul':
        raise TagNotUlError('Received a tag which is not <ul>.')

    ul_contents = [
        '- ' + item.contents[0].strip().replace('$$$', '$')
        for item
        in ul_tag.find_all('li')
    ]

    # ul_contents = []
    # for item in ul_tag.find_all('li'):
    #     for cont in item.contents:
    #         logger.debug('=======================')
    #         logger.debug(type(cont))
    #         a = cont.strip()
    #         logger.debug(type(a))
    #         a = cont.replace('$$$', '$')
    #         logger.debug(type(a))
    #         # ul_contents.append('-' + cont.strip().replace('$$$', '$'))
    #         ul_contents.append('-' + a)

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
        img_md = '| ![]({src}) |\n| :----------------------------------------------------------: |\n| {cap} |'.format(src=img_src, cap=caption_contents[0])
    
    return img_md