from bs4 import BeautifulSoup
from lxml import etree
import codecs

def LimitMessageParser(selector, logger):
    time_lim_title = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[2]/div/text()')[0]
    time_lim_content = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[2]/text()')[0]
    mem_lim_title = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[3]/div/text()')[0]
    mem_lim_content = selector.xpath('//*[@id="pageContent"]/div[3]/div[2]/div/div[1]/div[3]/text()')[0]

    return [(time_lim_title, time_lim_content), (mem_lim_title, mem_lim_content)]

def ContentParser(soup, logger, scheme, start=1):
    P_SCHEME = 'p{nth}'
    NTH_CHILD_SCHEME = ':nth-child({num})'
    LI_SCHEME = 'ul > li:nth-child({num})'

    p_counter = start
    statement_list = []
    lists_list = []
    
    # while len(p_content := soup.select(scheme.format(nth=NTH_CHILD_SCHEME.format(num=p_counter)))) > 0:
    #     statement_list.append(p_content)
    #     p_counter += 1

    while True:
        p_url = scheme + P_SCHEME.format(nth=NTH_CHILD_SCHEME.format(num=p_counter))
        p_content = soup.select(p_url)
        statement_list.append(p_content)
        p_counter += 1

        li_counter = 1
        while 



    if len(statement_list) < 1:
        p_content = soup.select(scheme.format(nth=''))
        statement_list.append(p_content)

    logger.debug('{} <p>{} found.'.format(len(statement_list), ('s' if len(statement_list) > 1 else '')))

    text_list = []
    for p_content in statement_list:
        for item in p_content:
            text = item.text.strip()
            text_list.append(text)
    
    return text_list

def StatementParser(soup, logger):
    STATEMENT_SELECTOR_SCHEME = '#pageContent > div.problemindexholder > div.ttypography > div > div:nth-child(2) > '
    logger.info('Start to parse problem statement.')

    return ContentParser(soup, logger, STATEMENT_SELECTOR_SCHEME)
    # STATEMENT_SCHEME = '//*[@id="pageContent"]/div[3]/div[2]/div/div[2]/p[{num}]'

    # state_list = []
    # p_counter = 1
    # while len(state := selector.xpath(STATEMENT_SCHEME.format(num=p_counter))) > 0:
    #     state_list.append(state.xpath('string(.)').extract()[0])
    #     p_counter += 1

    # return state_list

def InputStateParser(soup, logger):
    INPUT_STATE_SCHEME = '#pageContent > div.problemindexholder > div.ttypography > div > div.input-specification > '
    logger.info('Start to parse input statement.')

    return ContentParser(soup, logger, INPUT_STATE_SCHEME, start=2)

def OutputStateParser(soup, logger):
    OUTPUT_STATE_SCHEME = '#pageContent > div.problemindexholder > div.ttypography > div > div.output-specification > '
    logger.info('Start to parse output statement.')

    return ContentParser(soup, logger, OUTPUT_STATE_SCHEME, start=2)