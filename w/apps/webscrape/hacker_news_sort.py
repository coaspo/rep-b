#!/usr/bin/env python3
"""
>>> create_web_page(['l3', '<li>', '<a href="l2">l2</a>'], [10, 100, 50], [5, 10, 3])
'<html><head></head><title>Sorted Hacker news from</title>\\n\
<body>Sorted <a href="https://news.ycombinator.com/">https://news.ycombinator.com/</a><br><table>\\n\
<tr><td><li> 100 pts, 10 hrs ago</td><td><a href="l2">l2</a> 17 pts/hr, 50 pts, 3 hrs ago</td><tr>\\n\
<tr><td><a href="l2">l2</a> 50, 3</td><td><li> 10, 100, 10</td><tr>\\n\
<tr><td>l3 10, 5</td><td>l3 2, 10, 5</td><tr>\\n\
</table></body></html>'
"""

import requests
import bs4
import webbrowser
import datetime

HACKER_NEWS_URL = 'https://news.ycombinator.com/'
HACKER_NEWS_URL = 'https://news.ycombinator.com/'
#https://news.ycombinator.com/front?day=2022-01-01
#https://news.ycombinator.com/front?day=2022-01-01&p=1


def get_web_page(url: str):
    page = requests.get(url)
    print(url,'\n---', page.text)
    return page.text



def parse_web_page(html: str):
    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[0]

    links = table.findAll('a', {"class": "titlelink"})
    descs = table.findAll('td', {"class": "subtext"})
    if len(links) != len(descs):
        raise ValueError('ERR len links/descs: ' + str(len(links)) + '!=' + str(len(descs)))
    i = 0
    scores = []
    while i < len(links):
        score_spans = descs[i].find_all('span', {"class": "score"})
        if len(score_spans) == 0 or 'ycombinator.com' in links[i] \
               or 'http' not in str(links[i]):
            print('removed link #', i, links[i])
            del (descs[i])
            del (links[i])
            continue
        score = int(score_spans[0].text[:-7])
        if score < 200:
            del (descs[i])
            del (links[i])
            continue
        scores.append(int(score_spans[0].text[:-7]))
        i += 1
    return links, scores


def scape_links(day_range):
    links = []
    scores = []
    now = datetime.datetime.now()
    #https://news.ycombinator.com/front?day=2022-01-29
    for day_count in range(day_range):
      date = now - datetime.timedelta(days=day_count)
      publish_date =str(date)[0:10]
      url_sfx = 'front?day='+publish_date
      print(url_sfx)
      ith_page=1
      while True:
          url = HACKER_NEWS_URL + url_sfx+ '&p=' + str(ith_page)
          #example: https://news.ycombinator.com/front?day=2022-01-01&p=1
          print('  ',ith_page, 'scrapping:', url)
          html = get_web_page(url)
          links_i, scores_i = parse_web_page(html)
          if len(links_i) == 0:
              break
          elif ith_page > 4:
              print('possible ERR, more than 4 pages scanned')
              break
          for j in range(len(links_i)):
             link = str(links_i[j])
             i = link.find('//') + 4
             i2 = link.find('/', i)
             i = link.rfind('.', i2-5, i2) + 1  #http://www.overv.eu/
             domain = link[i:i2].upper()
             title = '" '+'title="'+publish_date+',  '+str(scores_i[j])+ ' pts"''>'
             link = link.replace('">', title)
             links_i[j] = link + ('' if domain=='COM' else ' <b>' + domain + '</b>')
          links += links_i
          scores += scores_i
          ith_page += 1
    print('scape_links: len of links, scores: ', len(links))
    return links, scores


def create_web_page(links, scores):
    html = "<html><head></head><title>Sorted Hacker news from</title>\n<body>Sorted <a href=\"{0}\">{1}" \
           "</a><pre>".format(HACKER_NEWS_URL, HACKER_NEWS_URL)
    del scores[200:]
    del links[200:]
    zipped = zip(scores, links)
    links_score_sorted = list(zipped)
    links_score_sorted.sort(reverse=True, key=lambda y: y[0])

    for link in links_score_sorted:
      html += link[1] + '\n'
    html += '</pre></body></html>'
    return html.replace('\r', '')


def main():
    try:
        print('start')
        day_range = 7
        links, scores = scape_links(day_range)
        html = create_web_page(links, scores)
        file_path = './hacker_news_HIGH_SCORES_'+str(day_range)+'-days.html'
        with open(file_path, 'w') as f:
           f.write(html)
        webbrowser.open_new_tab(file_path)

        print('done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
