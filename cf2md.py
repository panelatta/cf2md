import argparse
import re
import requests
import traceback
from bs4 import BeautifulSoup
import logging
import coloredlogs

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

def get_link():
    parser = argparse.ArgumentParser()
    parser.add_argument('problem_id', help='id of the problem')
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
        link = PROBLEM_URL_SCHEME.format(contest=contest_id, problem=prob_id)
        return link

if __name__ == '__main__':
    link = get_link()
    if link is not None:
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }
        html = requests.get(link, headers=header)
        html.encoding = 'utf-8'
    else:
        print("yah")