from bs4 import BeautifulSoup, element
import codecs
import re

class TagNotPError(Exception):
    pass
class TagNotUlError(Exception):
    pass
class TagNotCenterError(Exception):
    pass
class NoImgFoundError(Exception):
    pass
class TagNotOlError(Exception):
    pass

def space_add(contents: list, tmp_str, index):
    '''
    When a piece of text *a* is followed by a piece of bold/italic/ \
    typewriter-fonted text *b*, checking whether a[-1] is '"' is \
    needed. If not so, *b* should be added a space at its beginning.
    '''

    is_not_quote = lambda ch: ch not in ('"', '\'')
    
    if is_not_quote(tmp_str[0]):
        if index > 0:
            prev_item = contents[index - 1]
            if isinstance(prev_item, element.Tag):
                if is_not_quote(prev_item.contents[0][-1]):
                    tmp_str = ' ' + tmp_str
            else:
                if is_not_quote(prev_item[-1]):
                    tmp_str = ' ' + tmp_str

    return tmp_str

def interline_formula_process(tmp_str):
    '''
    When a latex formula is presented as a interline block, the \
    string '$$' at its both ends need to be processed as '$$\\n' and '\\n$$'. \
    
    That's because some Markdown parsing engines cannot process \
    the '$$...$$' correctly, and just parse it as an inline formula, like
    Typora.
    '''

    matcher = re.search(r'^\$\$([^\$]*)\$\$$', tmp_str)
    if matcher is not None:
        tmp_str = '$$\n' + matcher.group(1) + '\n$$'

    return tmp_str

def font_process(tag_list: list, logger):
    '''
    Processing texts in a list. Replacing all '$$$' to '$' and all \
    span tags with class of 'tex-font-style-{}' to the corresponding \
    markdown or tex expressions.
    '''

    content_list = []
    for index, item in enumerate(tag_list):
        if not hasattr(item, 'get'):
            tmp_str = item.strip().replace('$$$', '$')
            tmp_str = interline_formula_process(tmp_str)
            tmp_str = space_add(tag_list, tmp_str, index)
            content_list.append(tmp_str)
        else:
            item_span_class = item.get('class')
            if item_span_class[0] == 'tex-font-style-tt':
                tmp_str = '$\\texttt{' + item.contents[0].strip().replace('$$$', '$') + '}$'
                tmp_str = space_add(tag_list, tmp_str, index)
                content_list.append(tmp_str)
            elif item_span_class[0] == 'tex-font-style-bf':
                tmp_str = '**' + item.contents[0].strip().replace('$$$', '$') + '**'
                tmp_str = space_add(tag_list, tmp_str, index)
                content_list.append(tmp_str)
            elif item_span_class[0] == 'tex-font-style-it':
                tmp_str = '*' + item.contents[0].strip().replace('$$$', '$') + '*'
                tmp_str = space_add(tag_list, tmp_str, index)
                content_list.append(tmp_str)

    return content_list

def p_handler(p_tag, logger):
    '''
    Handling tag <p>.
    '''

    if p_tag.name != 'p':
        raise TagNotPError('Received a tag which is not <p>.')

    content_list = font_process(p_tag.contents, logger)    
    content = ''.join(content_list)

    return content

def ul_handler(ul_tag, logger):
    '''
    Handling tag <ul>. (i.e. unordered list)
    '''

    if ul_tag.name != 'ul':
        raise TagNotUlError('Received a tag which is not <ul>.')

    ul_contents = [
        ''.join(font_process(item.contents, logger))
        for item
        in ul_tag.find_all('li')
    ]
    ul_contents = [ '- ' + item for item in ul_contents ]

    return ul_contents

def ol_handler(ol_tag, logger):
    '''
    Handling tag <ol>. (i.e. ordered list)
    '''

    if ol_tag.name != 'ol':
        raise TagNotOlError('Received a tag which is not <ol>.')

    ol_contents = [
        ''.join(font_process(item.contents, logger))
        for item
        in ol_tag.find_all('li')
    ]

    ol_contents = [
        '{}. '.format(index) + item
        for index, item
        in enumerate(ol_contents, start=1)
    ]

    return ol_contents

def img_handler(center_tag, logger):
    '''
    Handling tag <center>. (i.e. usually images)
    '''

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