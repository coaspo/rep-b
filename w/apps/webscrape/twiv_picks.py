#!/usr/bin/env python3
import bs4

import util
import requests
from bs4 import BeautifulSoup

TWIV_URL = 'https://www.microbe.tv/twiv/weekly-picks/'


def is_bad_link(url):
    try:
        ret = requests.head(url)
        status = ret.status_code
        yes = status >= 400
        if yes:
            print('   bad link, status=', status)
        return yes
    except requests.exceptions.ConnectionError:
        print('ERR while looking at header')
        return True


def has_javascript(url):
    try:
        yes = 'javascript' in get_web_page_txt(url)
        if yes:
            print('   has javascript')
        return yes
    except requests.exceptions.ConnectionError:
        print('ERR while looking for javascript')
        return True


def get_web_page_txt(url: str):
    try:
        page = requests.get(url)
        return page.text
    except requests.exceptions.RequestException:
        return 'NOT FOUND'


def get_web_page_links(url: str):
    txt = get_web_page_txt('https://www.microbe.tv/twiv/weekly-picks/')
    soup = BeautifulSoup(txt, 'html.parser')
    links = soup.findAll('a')
    links = [x for x in links if x['href'].startswith('http') and
             len(x.get_text()) > 0 and
             'astore.amazon.com' not in x['href']]
    urls = []
    unique_links = []
    for link in links:
        link = link.replace('\n', '').replace('<br />', '')
        if link['href'] not in urls:
            urls.append(link['href'])
            unique_links.append(link)
    print('Found', len(unique_links), 'unique web links')
    return unique_links


def create_pick_link_dict(links):
    pick_link_dict = {'NEWS': [], 'BOOK': [], 'EDU': [], 'GOV': [], 'VIDEO': [], 'COM': [], 'SPACE': [], 'MISC': [],
                      'ORG': [], 'AUDIO': [], 'WIKIPED': [], 'PHOTO': [], 'COM-JS': []}
    pick_labels = [('amazon.com', 'BOOK'),
                   ('ted.com', 'TED'),
                   ('amzn.', 'BOOK'),
                   ('youtu.be', 'VIDEO'),
                   ('youtube.com', 'VIDEO'),
                   ('imdb.com', 'VIDEO'),
                   ('video', 'VIDEO'),
                   ('nikon', 'PHOTO'),
                   ('image', 'PHOTO'),
                   ('picture', 'PHOTO'),
                   ('photo', 'PHOTO'),
                   ('podcast', 'AUDIO'),
                   ('esa.int', 'ESA'),
                   ('nasa.gov', 'NASA'),
                   ('space', 'SPACE'),
                   ('npr.org', 'NPR'),
                   ('wikipedia.org', 'WIKIPED'),
                   ('.gov', 'GOV'),
                   ('news', 'NEWS'),
                   ('.com', 'COM'),
                   ('.net', 'NET'),
                   ('.org', 'ORG'),
                   ('.edu', 'EDU')]  # .com is filtered out
    url_black_list = ['microbe.tv', 'virology.ws', 'nyti.ms', 'twit.tv', 'facebook.com']
    soup = BeautifulSoup('', 'html.parser')
    blacklist_count = 0
    non_existant_count = 0
    com_javascript_count = 0
    for link in links:
        url = link['href']
        url_desc = link.get_text()
        print(url)
        if is_url_blacklisted(url):
            blacklist_count += 1
            continue
        if is_bad_link(url):
            non_existant_count += 1
            continue
        new_link = bs4.Tag(builder=soup.builder,
                           name='a',
                           attrs={'href': url})

        new_link.string = url_desc.strip()
        known_link = False
        for pick_label in pick_labels:
            if pick_label[0] in url or pick_label[0] in url_desc.lower():
                if pick_label[1] not in new_link.string:
                    new_link.string += ' ' + pick_label[1]
                if pick_label[0] == '.com' and has_javascript(url):
                    new_link.string += '-JS'
                    update_pick_link_dict(new_link, pick_link_dict, 'COM-JS')
                else:
                    update_pick_link_dict(new_link, pick_link_dict, pick_label[1])
                known_link = True
                break
                # https://twit.tv/
        if not known_link:
            # for example find uk in: http://www.bbc.co.ukcience/programmes/b00bw51j
            country, domain = find_country(url)
            new_link.string += ' ' + domain.upper()
            if len(country) > 0:
                new_link.string += ' (' + country + ')'
            pick_link_dict.get('MISC').append(new_link)
    print(blacklist_count, 'links were black listed')
    print(non_existant_count, 'links  skipped; not available')
    print(com_javascript_count, '.com links  with javascript')
    return pick_link_dict


def update_pick_link_dict(new_link, pick_link_dict, pick_label_url):
    if pick_label_url == 'BOOK':
        pick_link_dict.get('BOOK').append(new_link)
    elif pick_label_url == 'EDU':
        pick_link_dict.get('EDU').append(new_link)
    elif pick_label_url == 'GOV':
        pick_link_dict.get('GOV').append(new_link)
    elif pick_label_url == 'VIDEO' or pick_label_url == 'TED':
        pick_link_dict.get('VIDEO').append(new_link)
    elif pick_label_url == 'PHOTO':
        pick_link_dict.get('PHOTO').append(new_link)
    elif pick_label_url == 'COM-JS':
        pick_link_dict.get('COM-JS').append(new_link)
    elif pick_label_url == 'COM' or pick_label_url == 'NET':
        pick_link_dict.get('COM').append(new_link)
    elif pick_label_url == 'WIKIPED':
        pick_link_dict.get('WIKIPED').append(new_link)
    elif pick_label_url == 'AUDIO':
        pick_link_dict.get('AUDIO').append(new_link)
    elif pick_label_url == 'ORG':
        pick_link_dict.get('ORG').append(new_link)
    elif pick_label_url == 'NPR' or pick_label_url == 'NEWS':
        pick_link_dict.get('NEWS').append(new_link)
    elif pick_label_url == 'NASA' or pick_label_url == 'ESA' or pick_label_url == 'SPACE':
        pick_link_dict.get('SPACE').append(new_link)
    else:
        print('err; invalid pick label:', pick_label_url, 'new_link=', new_link)


def find_country(url):
    i = url.find('//') + 4
    i2 = url.find('/', i)
    i2 = i2 if i2 > 0 else len(url)
    i = url.rfind('.', i, i2) + 1  # http://www.overv.eu/
    domain = url[i:i2]
    country = util.get_country(domain)
    return country, domain.upper()


def is_url_blacklisted(url):
    url_black_list = ['microbe.tv', 'virology.ws', 'nyti.ms', 'twit.tv', 'facebook.com']
    for black_url in url_black_list:
        if black_url in url:
            print('   site is blacklisted; ', black_url)
            return True
    return False


def create_web_page(pick_links, link_type):
    html = '<html><title>Scannable TWIV picks</title>\n<body>'
    html += link_type + " picks from: "
    html += "<a href=\"{0}\">{1}</a><pre>".format(TWIV_URL, TWIV_URL)
    i = 0
    for link in pick_links:
        i += 1
        html += str(i) + '  ' + str(link).replace('\n', '') + '\n'
    html += '</pre></body></html>'
    return html


def create_link_files(pick_link_dict):
    link_count = 0
    for link_type in pick_link_dict.keys():
        links = pick_link_dict.get(link_type)
        link_count += len(links)
        if len(links) == 0:
            print('did not find', link_type, 'links')
            continue
        file_path = create_link_file(link_type, links)
        # webbrowser.open_new_tab(file_path)
        print('created', file_path)
    return link_count


def create_link_file(link_type, links):
    html_page = create_web_page(links, link_type)
    file_path = './TWIV_PICKS/' + link_type + '.html'
    with open(file_path, 'w') as f:
        f.write(html_page)
    return file_path


def main():
    try:
        print('start')
        links = get_web_page_links(TWIV_URL)
        pick_link_dict = create_pick_link_dict(links)
        link_count = create_link_files(pick_link_dict)
        print('done; saved', link_count, 'links into files')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()
        return str(exc)


if __name__ == "__main__":
    print('Script creates html files with links from TWIV picks\n',
          'Each file contains one type of URLs - for example; NEWS, BOK...\n',
          'Script blacklists facebook and some web sites of no interest\n',
          'which use javascript')
    main()
