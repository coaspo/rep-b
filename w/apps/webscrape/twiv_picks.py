#!/usr/bin/env python3
import re

import requests
import webbrowser
import util

TWIV_URL = 'https://www.microbe.tv/twiv/weekly-picks/'


def get_web_page(url: str):
    try:
        page = requests.get(url)
        txt = page.text
        if '<title>Page Not Found</title>' in txt:
            return 'NOT FOUND'
        return txt
    except Exception as exc:
        return 'NOT FOUND'


def scrape_pick_links(html: str):
    pick_links ={'BOOK':[], 'EDU':[], 'GOV':[], 'VIDEO':[], 'COM':[], 'MISC':[] }
    pick_types = [('amazon.com', 'BOOK'),
            ('amzn.', 'BOOK'),
            ('youtu.be', 'VIDEO'),
            ('nasa.gov', 'NASA'),
            ('napr.org', 'NPR'),
            ('wikipedia.org', 'WIKI'),
            ('.gov', 'GOV'),
            ('.com', 'COM'),
            ('.net', 'COM'),
            ('.org', 'ORG'),
            ('.edu', 'EDU')]  # .com is filtered out
    lines=html.split('\n')
    print('will scan', len(lines), 'lines')
    start_scanig = False
    special_urls = ['microbe.tv','virology.ws','nyti.ms','twit.tv']
    for line in lines:
       if not start_scanig:
          start_scanig = 'Weekly Science Picks' in line
       if  start_scanig:
         i = line.find('<a href="http')
         if i > -1:
            i2 = line.find('</a>', i)
            if i2 > -1:
               link = line[i: i2+4]
               if 'astore.amazon.com' in link:
                 # skip link because it does not work
                 i = link.find('">')
                 i2 = link.find('</a', i)
                 pick_links.get('BOOK').append(link[i+2:i2]+ ' BOOK')
               else:
                 known_link = False
                 for pick_type in pick_types:
                   if pick_type[0] in link:
                     link = link + ' '+ pick_type[1]
                     if pick_type[1] == 'BOOK':
                        pick_links.get('BOOK').append(link)
                     elif pick_type[1] == 'EDU' or pick_type[1] == 'WIKI':
                        pick_links.get('EDU').append(link)
                     elif pick_type[1] == 'NASA' or pick_type[1] == 'GOV':
                        pick_links.get('GOV').append(link)
                     elif pick_type[1] == 'VIDEO':
                        pick_links.get('VIDEO').append(link)
                     elif pick_type[1] == 'COM' or pick_type[1] == 'ORG':
                        pick_links.get('COM').append(link)
                     else:
                       print('err; invalid pick type:', pick_type[1], 'link=', link)
                     known_link = True
                     break
                     #https://twit.tv/
                 if not known_link:
                    for url in special_urls:
                      if url in link:
                        link = link + ' ' + url
                        break
                    else:
                      # for example find uk in: http://www.bbc.co.uk/programmes/b00bw51j
                      i = link.find('//') + 4
                      i2 = link.find('/', i)
                      i = link.rfind('.', i2-5, i2) + 1  #http://www.overv.eu/
                      domain = link[i:i2]
                      country = util.get_country(domain)
                      link = link + ' ' + domain + ' ' + country
                    pick_links.get('MISC').append(link.strip())
    return pick_links


def create_web_page(pick_links,link_type):
    html = '<html><title>Scannable TWIV picks</title>\n<body>'
    html += link_type + " picks from: "
    html += "<a href=\"{0}\">{1}</a><pre>".format(TWIV_URL, TWIV_URL)
    i = 0
    for link in pick_links:
        i += 1
        html += str(i)+ '  '+link +'\n'
    html += '</pre></body></html>'
    return html


def main():
    try:
        print('start')
        html = get_web_page(TWIV_URL)
        print('read ', len(html), 'characters from', TWIV_URL)
        pick_links = scrape_pick_links(html)
        link_types =['BOOK', 'EDU', 'GOV', 'VIDEO', 'COM', 'MISC']
        i = 0
        for link_type in link_types:
           links = pick_links.get(link_type)
           if len(links) == 0:
             print('did not find', link_type, 'links')
           html_page = create_web_page(links, link_type)
           file_path = './twiv_picks_'+link_type+'.html'
           with open(file_path, 'w') as f:
              f.write(html_page)
           #webbrowser.open_new_tab(file_path)
           print('created', file_path)
           i+=1
        print('done')

    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()
        return str(exc)

if __name__ == "__main__":
    main()
