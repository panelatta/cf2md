from bs4 import BeautifulSoup
import codecs
import element_handler
import traceback

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
        traceback.print_exc()
    except element_handler.TagNotUlError:
        traceback.print_exc()
    except element_handler.TagNotCenterError:
        traceback.print_exc()
    except element_handler.NoImgFoundError:
        traceback.print_exc()
    else:
        return ret_list

def ExampleParser(example_soup, logger, level):
    input_soup = example_soup.find(class_='input').find(name='pre').contents[0]
    input_soup = '```{data}```'.format(data=input_soup)
    output_soup = example_soup.find(class_='output').find(name='pre').contents[0]
    output_soup = '```{data}```'.format(data=output_soup)

    example_list = []
    example_list.append('{} Input {}'.format('#' * (level + 2), '#' * (level + 2)))
    example_list.append(input_soup)
    example_list.append('{} Output {}'.format('#' * (level + 2), '#' * (level + 2)))
    example_list.append(output_soup)

    return example_list

def ContentParser(soup, logger, level):
    logger.info('Start to parse contents.')

    content_soup = soup.find(class_='problem-statement')

    content_list = []
    content_list.append('{} Description {}'.format('#' * level, '#' * level))

    logger.info('Start to parse limits.')
    limit_tuple = LimitMessageParser(content_soup.contents[0], logger)
    content_list.append(limit_tuple)

    logger.info('Start to parse descriptions.')
    description_list = StatementParser(content_soup.contents[1], logger)
    content_list.extend(description_list)

    logger.info('Start to parse input statements.')
    input_speci_soup = content_soup.find(name='div', attrs={'class': 'input-specification'})
    input_state_list = StatementParser(input_speci_soup, logger)
    content_list.append('{} Input {}'.format('#' * (level + 1), '#' * (level + 1)))
    content_list.extend(input_state_list)

    logger.info('Start to parse output statements.')
    output_speci_soup = content_soup.find(name='div', attrs={'class': 'output-specification'})
    output_state_list = StatementParser(output_speci_soup, logger)
    content_list.append('{} Output {}'.format('#' * (level + 1), '#' * (level + 1)))
    content_list.extend(output_state_list)

    logger.info('Start to parse examples.')
    example_soup = content_soup.find(class_='sample-test')
    content_list.append('{} Example {}'.format('#' * (level + 1), '#' * (level + 1)))
    example_list = ExampleParser(example_soup, logger, level)
    content_list.extend(example_list)

    if (note_soup := content_soup.find(name='div', attrs={'class': 'note'})) is not None:
        logger.info('Start to parse notes.')
        note_list = StatementParser(note_soup, logger)
        content_list.append('{} Note {}'.format('#' * (level + 1), '#' * (level + 1)))
        content_list.extend(note_list)
    
    return content_list

def MdGen(content_list, logger):
    logger.info('Start to generate markdown.')
    content = ''
    for item in content_list:
        if isinstance(item, list) or isinstance(item, tuple):
            for item2 in item:
                content += item2
                content += '\n'
            content += '\n'
        else:
            content += item
            content += '\n\n'
    return content