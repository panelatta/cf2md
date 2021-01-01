from bs4 import BeautifulSoup
from lxml import etree
import codecs
import element_handler
import traceback
from collections import Iterable

# def LimitMessageParser(selector, logger):
#     time_lim_title = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[2]/div/text()')[0]
#     time_lim_content = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[2]/text()')[0]
#     mem_lim_title = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[3]/div/text()')[0]
#     mem_lim_content = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[3]/text()')[0]

#     return [(time_lim_title, time_lim_content), (mem_lim_title, mem_lim_content)]

# def ContentParser(soup, logger, scheme, start=1):
#     P_SCHEME = 'p{nth}'
#     NTH_CHILD_SCHEME = ':nth-child({num})'
#     LI_SCHEME = 'ul > li:nth-child({num})'

#     p_counter = start
#     statement_list = []
#     lists_list = []
    
#     # while len(p_content := soup.select(scheme.format(nth=NTH_CHILD_SCHEME.format(num=p_counter)))) > 0:
#     #     statement_list.append(p_content)
#     #     p_counter += 1

#     while True:
#         p_url = scheme + P_SCHEME.format(nth=NTH_CHILD_SCHEME.format(num=p_counter))
#         p_content = soup.select(p_url)
#         logger.debug(type(p_content))
#         logger.debug(p_content.__dict__)
#         statement_list.append(p_content)
#         p_counter += 1

#         li_counter = 1
#         # while 



#     if len(statement_list) < 1:
#         p_content = soup.select(scheme.format(nth=''))
#         statement_list.append(p_content)

#     logger.debug('{} <p>{} found.'.format(len(statement_list), ('s' if len(statement_list) > 1 else '')))

#     text_list = []
#     for p_content in statement_list:
#         for item in p_content:
#             text = item.text.strip()
#             text_list.append(text)
    
#     return text_list

# def StatementParser(soup, logger):
#     # STATEMENT_SELECTOR_SCHEME = '#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2) > '
#     # logger.info('Start to parse problem statement.')

#     # return ContentParser(soup, logger, STATEMENT_SELECTOR_SCHEME)
#     state_soup = soup.find(class_="problem-statement")

#     # with codecs.open('test.in', 'w', encoding='utf-8') as f:
#     #     for item in tag_soup.contents:
#     #         if isinstance(item, Iterable):
#     #             for it in item:
#     #                 print(it, file=f)
#     #                 print('\n-------------\n', file=f)
#     #         else:
#     #             print(item, file=f)
#     #         print('\n================\n', file=f)

#     try:
#         for item in state_soup.contents[1]:
#             # logger.debug(item.name)
#             if item.name == 'p':
#                 # logger.debug('len = {}'.format(len(item.contents)))
#                 # logger.debug(item.contents)
#                 element_handler.p_handler(item, logger)
#             elif item.name == 'ul':
#                 element_handler.ul_handler(item, logger)
#             elif item.name == 'center':
#                 element_handler.img_handler(item, logger)
#     except element_handler.TagNotUlError:
#         traceback.print_exc()



# def InputStateParser(soup, logger):
#     INPUT_STATE_SCHEME = '#pageContent > div.problemindexholder > div.ttypography > div > div.input-specification > '
#     logger.info('Start to parse input statement.')

#     return ContentParser(soup, logger, INPUT_STATE_SCHEME, start=2)

# def OutputStateParser(soup, logger):
#     OUTPUT_STATE_SCHEME = '#pageContent > div.problemindexholder > div.ttypography > div > div.output-specification > '
#     logger.info('Start to parse output statement.')

#     return ContentParser(soup, logger, OUTPUT_STATE_SCHEME, start=2)

def test(soup, logger):
    tag_soup = soup.find(class_="problem-statement")

    # with codecs.open('test.in', 'w', encoding='utf-8') as f:
    #     for item in tag_soup.contents:
    #         if isinstance(item, Iterable):
    #             for it in item:
    #                 print(it, file=f)
    #                 print('\n-------------\n', file=f)
    #         else:
    #             print(item, file=f)
    #         print('\n================\n', file=f)

    try:
        for item in tag_soup.contents[1]:
            # logger.debug(item.name)
            if item.name == 'p':
                # logger.debug('len = {}'.format(len(item.contents)))
                # logger.debug(item.contents)
                element_handler.p_handler(item, logger)
            elif item.name == 'ul':
                element_handler.ul_handler(item, logger)
            elif item.name == 'center':
                element_handler.img_handler(item, logger)
    except element_handler.TagNotUlError:
        traceback.print_exc()

def LimitMessageParser(limit_soup, logger):
    time_limit = limit_soup.find_all(name='div', attrs={'class': 'time-limit'})[0].contents[1]
    memory_limit = limit_soup.find_all(name='div', attrs={'class': 'memory-limit'})[0].contents[1]

    time_limit_str = '> Time Limit: {}'.format(time_limit)
    memory_limit_str = '> Memory Limit: {}'.format(memory_limit)
    return (time_limit_str, memory_limit_str)

def StatementParser(state_soup, logger):
    ret_list = []
    try:
        for item in state_soup:
            if item.name == 'p':
                ret_list.append(element_handler.p_handler(item, logger))
            elif item.name == 'ul':
                ret_list.append(element_handler.ul_handler(item, logger))
            elif item.name == 'center':
                ret_list.append(element_handler.img_handler(item, logger))
    except element_handler.TagNotPError:
        traceback.print_exc():
    except element_handler.TagNotUlError:
        traceback.print_exc()
    except element_handler.TagNotCenterError:
        traceback.print_exc()
    except element_handler.NoImgFoundError:
        traceback.print_exc()
    else:
        return ret_list

def ContentParser(soup, logger, level):
    content_soup = soup.find(class_='problem-statement')

    content_list = []
    content_list.append('{} Description {}'.format('#' * level, '#' * level))

    limit_tuple = LimitMessageParser(content_soup.contents[0], logger)
    content_list.append(limit_tuple)

    description_list = StatementParser(content_soup.contents[1], logger)
    content_list.extend(description_list)

    section_title_list = content_soup.find_all(name='div', attrs={})

    input_state_list = StatementParser(content_soup.contents[2], logger)
    content_list.append('{} Input {}'.format('#' * (level + 1), '#' * (level + 1)))
    content_list.extend(input_state_list)

    output_state_list = StatementParser(content_soup.contents[3], logger)
    content_list.append('{} Output {}'.format('#' * (level + 1), '#' * (level + 1)))
    content_list.extend(output_state_list)



def MdGen(content_list):
    content = ''
    for item in content_list:
        if isinstance(item, Iterable):
            for item2 in item:
                content += item
                content += '\n'
            content += '\n'
        else:
            content += item
            content += '\n\n'
    return content