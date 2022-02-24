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
import calendar
from pathlib import Path
import glob
import util

HACKER_NEWS_URL = 'https://news.ycombinator.com/'
DEBUG = 1


def get_web_page(url: str):
    page = requests.get(url)
    text = page.text
    print('  read from url ', len(text), " CHARs")
    return text



def parse_web_page(html: str):
    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[0]

    links = table.findAll('a', {"class": "titlelink"})
    descs = table.findAll('td', {"class": "subtext"})
    if len(links) != len(descs):
        raise ValueError('ERR len links/descs: ' + str(len(links)) + '!=' + str(len(descs)))
    i = 0
    points = []
    comments = []
    while i < len(links):
        point_spans = descs[i].find_all('span', {"class": "point"})
        if len(point_spans) == 0 or 'ycombinator.com' in links[i] \
               or 'http' not in str(links[i]):
            print('   removed invalid link')
            if 'ycombinator.com' in links[i]:
              print ('   ', links[i])
            del (descs[i])
            del (links[i])
            continue
        point = int(point_spans[0].text[:-7])
        if point < 200:
            del (descs[i])
            del (links[i])
            continue
        points.append(point)
        txt = str(descs[i])
        i_end = txt.find('comments') - 1
        i_start = txt.find('>', i_end-20) + 1
        comment = int(txt[i_start:i_end])
        comments.append(comment)
        links[i] = str(links[i]).replace('class="titlelink" ','')
        i += 1
    if DEBUG:
      print('  ---parse_web_page\n   ', len(points), len(comments), len(links),\
        '\n   ', points[0:5], '\n   ', comments[0:5], '\n   ', links[0:1])
    return links, points, comments

def get_url_desc(link):
   i = link.find('//') + 4
   i2 = link.find('/', i)
   i = link.rfind('.', i2-5, i2) + 1  #http://www.overv.eu/
   domain = link[i:i2].upper()

   desc = ''
   if 'twitter.com' in link or 'facebook.com' in link or 'linkedin.com' in link:
     desc ='🦜'
   elif 'youtube.com' in link:
     desc ='🎞️'
   elif '.edu' in link:
     desc ='🏫'
   elif domain != 'COM':
     desc = domain + ' ' + util.get_country(domain)

   if 'blog' in link:
     desc += ' 🪵'
   elif 'nature.com' in link or 'sien' in link or 'sci-news' in link or \
        'kolabtree' in link or 'scidev' in link or 'labbulletin' in link or \
        'popsci.com' in link or 'nasa' in link or 'nationalgeog' in link or \
        'aaas.org' in link or 'space.com' in link or 'pnas.org' in link or \
        'howstuffworks' in link or 'nautil.us' in link or 'pnas.org' in link or \
        'smithsonian' in link or 'wired' in link or 'phys.org' in link or \
        'sien' in link:
     desc += ' ⚛️'
   elif 'news' in link or 'cnn.com' in link or 'nytimes.com' in link or \
        'huffpost' in link or 'usatoday' in link or 'wsj.com' in link  or \
        'politico' in link or 'reuters' in link or 'dailymail' in link  or \
        'latimes' in link or 'reuters' in link or 'washingtonpost' in link  or \
        'wsj.com' in link or 'theguardian' in link or 'usatoday' in link or \
        'npr.org' in link:
     desc += ' 📰'
   if 'java' in link or 'github' in link or 'linux' in link or 'computer' in link or \
      '.dev' in link or '.codes' in link or '.engineer' in link or '.software' in link:
     desc += ' 💻'
   if '.pdf' in link:
     desc += ' PDF'
   return desc.strip()


def get_url_legend(html):
   legend = ''
   if '🦜' in html:
     legend = '🦜 twitter/facebook'
   if '🪵' in html:
     legend += '   🪵 BLOG'
   if '🎞️' in html:
     legend += '   🎞️ youtube'
   if '🏫' in html:
     legend += '   🏫 .edu'
   if '⚛️' in html:
     legend += '   ⚛️ science'
   if '📰' in html:
     legend += '   📰 news'
   if '💻' in html:
     legend += '   💻 computer'
   return legend


def get_bi_week_links():
  html = '\nBi-Weekly:  01-xxx  05-xxx  09-xxx  13-xxx  17-xxx  21-xxx\n'\
           '            02-xxx  06-xxx  10-xxx  14-xxx  18-xxx  24-xxx\n'\
           '            03-xxx  07-xxx  11-xxx  15-xxx  19-xxx  25-xxx\n'\
           '            04-xxx  08-xxx  12-xxx  16-xxx  20-xxx  26-xxx'
  return html


def scrape_ycombinator_links(start_date):
    links = []
    points = []
    comments = []
    now = datetime.datetime.now()
    for day_count in range(14):
      date = start_date + datetime.timedelta(days=day_count)
      publish_date =str(date)[0:10]
      print(' scraping', publish_date)
      url_sfx = 'front?day='+publish_date
      ith_page=1
      while True:
          url = HACKER_NEWS_URL + url_sfx+ '&p=' + str(ith_page)
          #example: https://news.ycombinator.com/front?day=2022-01-01&p=1
          if DEBUG:
            print('   scrape_ycombinator_links\n    ', publish_date, ith_page, url)
          html = get_web_page(url)
          links_i, points_i , comments_i = parse_web_page(html)
          if len(links_i) == 0:
              break
          elif ith_page > 4:
              print('    possible ERR, more than 4 pages scanned')
              break
          for j in range(len(links_i)):
             link = str(links_i[j])
             title = '" ' + 'title="' + str(points_i[j])+ ' pts, '\
                                      + str(comments_i[j])+ ' comments '\
                                      + publish_date+ '">'
             link = link.replace('">', title)
             desc = get_url_desc(link)
             if desc != '':
                link += ' <b>' + desc + '</b>'
             links_i[j] = link
          links += links_i
          points += points_i
          comments += comments_i
          ith_page += 1
    if DEBUG:
      print('   ---scrape_ycombinator_links\n    ', len(points), len(comments), len(links),\
        '\n    ', points[0:5], '\n    ', comments[0:5])
    return links, points, comments


def append_lines(html, sort_order, links, sfx, max_link_cnt, web_page_links):
    zipped = zip(sort_order, links)
    links_sorted = list(zipped)
    links_sorted.sort(reverse=True, key=lambda y: y[0])
    if DEBUG:
      print('    ---append_lines; links_sorted 1:\n     ', links_sorted[0:1])
    i = 0
    is_non_etc = sfx == '\n'
    for x in links_sorted:
      link = x[1]
      if is_non_etc and ('🦜' in link or '🪵' in link or '📰' in link):
         continue
      if link not in web_page_links:
         html += link +  ', ' + str(x[0]) + sfx
         web_page_links.append(link)
         i += 1
         if i == max_link_cnt:
           break
    return html


def create_web_page(is_weekly, count, start_date, links, points, comments):
    html = "<html><head></head><title>Hacker news sort</title>\n"\
           "<body>Top <a href=\"{0}\">{1}" \
           "</a> links".format(HACKER_NEWS_URL, HACKER_NEWS_URL)
    if is_weekly:
       html = html.replace('Top', 'Bi-weekly top')
       html += " for 7 days starting {0}:<pre>".format(str(start_date)[0:10])
    else:
       html = html.replace('Top', 'All-week top')
       html += " ; up to week starting {0}:<pre>".format(str(start_date)[0:10])
    html += '\n' + str(count) + ' top points:\n'
    web_page_links = []
    html = append_lines(html, points, links, ' points \n', count, web_page_links)

    html += '\n' + str(count) + ' top comments:\n'
    html = append_lines(html, comments, links, ' comments \n', count, web_page_links)

    point_comments = []
    for i in range(len(links)):
        point_comments.append(points[i]*comments[i])
    html += '\n' + str(count) + ' top points*comments:\n'
    html = append_lines(html, point_comments, links, ' points*comments\n', 5, web_page_links)

    html += '\n' + str(count) + ' top point non-🦜\🪵\📰:\n'
    html = append_lines(html, points, links, '\n', count, web_page_links)

    html += '\n' + get_url_legend(html)
    if not is_weekly:
      html += '\n' + get_bi_week_links()
    html += '</pre></body></html>'
    return html.replace('\r', '')


def date_parameters():
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=21)
    week = last_week.strftime("%W")
    i_week = int(week)
    if i_week % 2 == 0:
      return None, None  # sorts are done bi-weekly when week is odd
    year = last_week.strftime("%Y")
    month = last_week.strftime("%b")[0:3].lower()
    d = str(year) + '-W' +week
    start_date = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    i = (i_week + 1) // 2
    num = f"{i:02d}"
    file_path = './hacker_news_sort_' + num + '_' + month + '.html'
    if DEBUG:
       print(' --file_path', file_path, start_date)
    return file_path, start_date


def write_file(html, file_path):
    with open(file_path, 'w') as f:
       f.write(html)
    print('Created ', file_path)


def read_all_weekly_sorts():
  links = []
  points = []
  comments = []
  bi_weekly_files = glob.glob('./hacker_news_sort_w*.html')
  print(bi_weekly_files)
  for file_i in bi_weekly_files:
    print('read_all_weekly_sorts', file_i)
    with open(file_i) as f:
      lines = f.readlines()
    links_i = [x for x in lines if x.startswith('<a href="http')]
    for link in links_i:
      i2 = link.find('</a>') + 4
      link = link[:i2]
      desc = get_url_desc(link)
      if desc != '':
          link += ' <b>' + desc + '</b>'
      links.append(link)
      i1 = link.find('title="') + 7  #title="263 pts, 142 comments">
      i2 = link.find(' pts,', i1)
      point = int(link[i1:i2])
      points.append(point)
      i1 = i2 + 6
      i2 = link.find(' comments', i1)
      comment = int(link[i1:i2])
      comments.append(comment)
  if DEBUG:
     print(' ---read_all_weekly_sorts; ', len(points), len(comments), len(links))
  return links, points, comments


def main():
    try:

        ('=== Start ===\n')
        file_path, start_date = date_parameters()
        if file_path is None:
            print('Cannot create file - 2nd previous week number is not odd')
        elif True:#not Path(file_path).exists():
            '''            links, points, comments = scrape_ycombinator_links(start_date)
            html = create_web_page(True, 10, start_date, links, points, comments)
            write_file(html, file_path)
            webbrowser.open_new_tab(file_path)'''

            file_path = './hacker_news_sort_all_weeks.html'
            links, points, comments = read_all_weekly_sorts()
            html = create_web_page(False, 20, start_date, links, points, comments)
            write_file(html, file_path)
            webbrowser.open_new_tab(file_path)
        else:
            print('No file created; ', file_path, ' already exists.')

        print('=== Done ====')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
