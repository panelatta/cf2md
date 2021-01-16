import argparse
import re
import requests
import traceback
from bs4 import BeautifulSoup
import logging
import coloredlogs
import codecs
import content_parser
import os
import lxml

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
    '''
    Parsing the command line arguments to get contest id and problem id \
    (e.g. 1462A, 1463E1...).
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('problem_id', help='ID of the problem. (e.g. 1462A)')
    parser.add_argument('-l', '--level', type=int, default=2, help='The highest title level of generated markdown text. If this argument is not explicitly set, it will be 2.')
    parser.add_argument('-d', '--dir', nargs='?', default='./', help='Root directory of the generated markdown file. If this argument is not explicitly set, it will be current directory.')
    parser.add_argument('-f', '--filename', nargs='?', default='test.md', help='Name of the generated markdown file. If this argument is not explicitly set, it will be \"test.md\".')
    args = parser.parse_args()

    logger.info('Start to deal with problem {}.'.format(args.problem_id))

    try:
        parse_matcher = re.search(r'^([0-9]+)([A-Z]|[a-z]+)([0-9]*)$', args.problem_id)
        if parse_matcher is None:
            raise ProblemIdMissMatchError
    except ProblemIdMissMatchError:
        traceback.print_exc()
        return None
    else:
        contest_id = parse_matcher.group(1)
        prob_id = parse_matcher.group(2).upper()
        if (group_len := len(parse_matcher.groups())) > 2:
            for i in range(3, group_len + 1):
                prob_id += parse_matcher.group(i)
        return contest_id, prob_id, args.level, args.dir, args.filename


def parse_problem(contest_id, prob_id, level, root_dir, filename):
    '''
    Load the problem page and parse it, then generate corresponding \
    markdown text.
    '''
    
    logger.debug('Parsing problem {}{}'.format(contest_id, prob_id))

    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    url = PROBLEM_URL_SCHEME.format(contest=contest_id, problem=prob_id)
    page = requests.get(url, headers=header)
    logger.debug('Start to parse HTML.')
    soup = BeautifulSoup(page.content, 'lxml')

    for br in soup.find_all('br'):
        br.replace_with('\n')

    content_list = content_parser.ContentParser(soup, logger, level)
    content = content_parser.MdGen(content_list, logger)

    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    path = '{dir}/{file}'.format(dir=root_dir, file=filename)
    with codecs.open(path, 'w', encoding='utf-8') as f:
        print(content, file=f)

if __name__ == '__main__':
    contest_id, prob_id, level, root_dir, filename = get_ids()
    parse_problem(contest_id, prob_id, level, root_dir, filename)