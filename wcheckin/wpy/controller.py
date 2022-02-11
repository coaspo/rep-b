#!/usr/bin/env python3
import logging
import os
from datetime import datetime

from wpy.util import Util
from wpy.contentspage import ContentsPage
from wpy.indexpage import IndexPage
from wpy.website import WebSite


def _update_index_and_contents_pages():
    target_dirs = ('../w/projects', '../w/tech', '../w/food', '../w/art', '../w/science', '../w/apps')
    website = WebSite(target_dirs)
    website.save_search_file_paths('../w/search_file_paths.txt')
    website.save_search_labels('../w/search_labels.txt')
    IndexPage.update_links(website, '../w/index.html')
    version = ContentsPage.update(website, '../w/contents.html')
    return version


def _check_in(version, git_branch):
    logging.info('_' * 80 + '\n----- 1. cwd: ' + os.getcwd())
    Util.check_into_repository(version, git_branch)
    os.chdir('../w')
    logging.info('_' * 80 + '\n----- 2. cwd: ' + os.getcwd())
    Util.check_into_repository(version, git_branch)
    os.chdir('../wcheckin')
    logging.info('Done.')


def main(git_branch):
    Util.run_tests()
    version = _update_index_and_contents_pages()
    _check_in(version, git_branch)

