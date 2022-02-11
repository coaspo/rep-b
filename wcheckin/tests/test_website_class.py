import os

from wpy.website import WebSite


def test_website():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    target_dirs = ('./tests/w/topic1', './tests/w/topic2')
    website = WebSite(target_dirs)

    if os.path.exists("./tests/search_file_paths__t.txt"):
        os.remove("./tests/search_file_paths__t.txt")
    website.save_search_file_paths('./tests/search_file_paths__t.txt')
    with open('./tests/search_file_paths__t.txt') as f:
        actual = f.read()
    expected = """topic1/links-2.html
topic1/links.html
topic2/problems-examples.html
topic2/problems-solutions.html
topic2/recipe.html
topic2/subtopic/word_list.html
"""
    assert expected == actual, 'save_search_file_paths() failed;\n actual:\n' + actual + '\nexpected:\n' + expected

    if os.path.exists("./tests/search_labels__t.txt"):
        os.remove("./tests/search_labels__t.txt")
    website.save_search_labels('./tests/search_labels__t.txt')

    with open('./tests/search_labels__t.txt') as f:
        actual = f.read()
    expected = """wolfram$$0$$https://www.wolfram.com/
worldometers$$0$$https://www.worldometers.info/
week in virology$$0$$https://www.microbe.tv/twiv/archive/
internet archive$$1$$https://archive.org
free books$$1$$https://www.freebookcentre.net/
coursera- free course$$1$$https://www.coursera.org/
edx - mit, harvard$$1$$https://www.edx.org/
pizza$$4
serve done$$4"""  # anchor label, file index, url
    assert expected == actual, 'search_labels__t.txt failed:\n actual:\n' + actual + '\nexpected:\n' + expected

    actual = str(len(website.web_page_dict))
    expected = "2"
    assert expected == actual, 'len(website.web_pages) failed:\n actual:\n' + actual + '\nexpected:\n' + expected

    actual = str(website.topic_names)
    expected = "['topic1', 'topic2']"
    assert expected == actual, 'website.topic_names failed:\n actual:\n' + actual + '\nexpected:\n' + expected

    actual = str(len(website.web_page_dict['topic1']))  # num of web pages
    expected = "2"
    assert expected == actual, "len(website.web_pages['tests']) failed:\n actual:\n" + actual + "\nexpected:\n" + \
                               expected

    actual = str(website.web_page_dict['topic2'][3])
    expected = "WebPage: file_path = ./tests/w/topic2/subtopic/word_list.html, link = "\
               "<a href='././tests/w/topic2/subtopic/word_list.html'>Word list</a>,  "\
               "date_range = 2021-01-11, kb_size = 0.2,  search_indexes = [] topic = topic2  sub_dir = subtopic"
    assert expected == str(
        actual), "website.topics['tests'][0] failed:\n actual:\n" + actual + "\nexpected:\n" + expected
