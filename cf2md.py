import argparse
import re
import requests
import traceback
from bs4 import BeautifulSoup
import logging
import coloredlogs
import codecs
import content_parser
from lxml import etree

# define logging.
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# set coloredlogs.
coloredlogs.install(
    fmt='%(asctime)s %(levelname)s %(message)s',
    level='debug'
)

# The problem url scheme.
PROBLEM_URL_SCHEME = 'http://codeforces.com/contest/{contest}/problem/{problem}'

class ProblemIdMissMatchError(Exception):
    pass
class EmptyLinkError(Exception):
    pass

def get_ids():
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_id', help='id of the problem')
    parser.add_argument('-l', '--level', type=int, help='the highest title level of generated markdown text')
    args = parser.parse_args()

    logger.info('Start to deal with problem {}.'.format(args.problem_id))

    try:
        parse_matcher = re.search(r'^([0-9]+)([A-Z]|[a-z])$', args.problem_id)
        if parse_matcher is None:
            raise ProblemIdMissMatchError
    except ProblemIdMissMatchError:
        traceback.print_exc()
        return None
    else:
        contest_id = parse_matcher.group(1)
        prob_id = parse_matcher.group(2).upper()
        return contest_id, prob_id

def parse_problem(contest_id, prob_id):
    logger.debug('Parsing problem {}{}'.format(contest_id, prob_id))

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    url = PROBLEM_URL_SCHEME.format(contest=contest_id, problem=prob_id)
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    selector = etree.HTML(page.content);

    for br in soup.find_all('br'):
        br.replace_with('\n')

    content_parser.ContentParser(soup, logger, 2)

    # limit_list = content_parser.LimitMessageParser(selector, logger)
    # state_list = content_parser.StatementParser(soup, logger)
    # input_state_list = content_parser.InputStateParser(soup, logger)
    # output_state_list = content_parser.OutputStateParser(soup, logger)

    # for item in state_list:
    #     item = item.replace('$$$', '$')
    # for item in input_state_list:
    #     item = item.replace('$$$', '$')
    # for item in output_state_list:
    #     item = item.replace('$$$', '$')

    # with codecs.open('test.txt', 'w', encoding='utf-8') as f:
    #     print('### Description ###\n', file=f)
    #     print('> {}: {}'.format(limit_list[0][0], limit_list[0][1]), file=f)
    #     print('> {}: {}'.format(limit_list[1][0], limit_list[1][1]), file=f)
    #     print('\n', end='', file=f)
    #     for item in state_list:
    #         print(item, file=f)
    #         print('\n', end='', file=f)
    #     print('#### Input ####\n', file=f)
    #     for item in input_state_list:
    #         print(item, file=f)
    #         print('\n', end='', file=f)
    #     print('#### Output ####\n', file=f)
    #     for item in output_state_list:
    #         print(item, file=f)
    #         print('\n', end='', file=f)

    

if __name__ == '__main__':
    contest_id, prob_id = get_ids()
    parse_problem(contest_id, prob_id)