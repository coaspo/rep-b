import os

from wpy.indexpage import IndexPage
from wpy.website import WebSite


def test_update_links():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('tests/w/topic1', 'tests/w/topic2')
    website = WebSite(target_dirs)
    IndexPage.update_links(website, './tests/index.html')

    with open('./tests/index.html') as f:
        source = f.read()
        assert "tests/w/topic1" in source, 'did not find "tests/w/topic1" in contents.html:\n' + source
        assert len(source) > 3000, 'index file too small; < 3,000 chars'
