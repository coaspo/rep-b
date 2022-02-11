import os

from wpy.webpage import WebPage


def test_webpage():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    page = WebPage('tests/w/topic1/links.html')
    actual = page.search_indexes
    expected = [('internet archive', 'https://archive.org'),
                ('free books', 'https://www.freebookcentre.net/'),
                ('coursera- free course', 'https://www.coursera.org/'),
                ('edx - mit, harvard', 'https://www.edx.org/')]
    assert expected == actual, 'contents_indexes() failed; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    actual = page.file_path
    expected = 'tests/w/topic1/links.html'
    assert expected == actual, 'invalid file_path; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.link
    expected = "<a href='./tests/w/topic1/links.html'>Links</a>"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.date_range
    expected = '2021-01-07'
    assert expected == actual, 'invalid date_range; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.kb_size
    expected = 0.4
    assert expected == actual, 'invalid num_of_lines; expected:\n' + str(expected) + '\nactual:\n' + str(actual)

    actual = page.topic
    expected = 'topic1'
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + str(actual)

    page = WebPage('tests/w/topic2/subtopic/word_list.html')
    actual = page.link
    expected = "<a href='./tests/w/topic2/subtopic/word_list.html'>Word list</a>"
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual

    actual = page.sub_dir
    expected = 'subtopic'
    assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + str(actual)

    # actual = page.excerpt
    # expected = "This is a test"
    # assert expected == actual, 'invalid search_indexes; expected:\n' + expected + '\nactual:\n' + actual
    # print(page)
