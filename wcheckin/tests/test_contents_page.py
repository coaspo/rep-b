import os
from tkinter import simpledialog

import mock

from wpy.contentspage import ContentsPage
from wpy.website import WebSite


def test_contents_page():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('./tests/w/topic1', './tests/w/topic2')
    website = WebSite(target_dirs)
    simpledialog.askstring = mock.Mock(return_value="ver-1")
    ContentsPage.update(website, './tests/contents.html')

    with open('./tests/contents.html') as f:
        source = f.read()
        assert "ver-1" in source, 'did not find "ver-1" in contents.html:\n' + source
        assert 'topic1' in source, 'did not find "topic1" in contents.html:\n' + source
        assert 'topic2' in source, 'did not find "topic2" in contents.html:\n' + source
