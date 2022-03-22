#!/usr/bin/env python3
"""
#>>> create_web_page(['l3', '<li>', '<a href="l2">l2</a>'], [10, 100, 50], [5, 10, 3], 2)
'<html><head><meta charset='UTF-8'></head><title>Hacker news sort</title>\\n<body>Top <a href="https://news.ycombinator.com/">https://news.ycombinator.com/</a> links\\n2 top points:\\n<li>, 100 points \\n<a href="l2">l2</a>, 50 points \\n\\n2 top comments:\\nl3, 5 comments \\n\\n2 top points*comments:\\n\\n2 top point non-🦜/\U0001fab5/📰:\\n\\n🦜 twitter/facebook   \U0001fab5 BLOG   📰 news</pre></body></html>'
"""
import calendar
import datetime
import glob
import webbrowser
import bs4
import requests
import util

HACKER_NEWS_URL = 'https://news.ycombinator.com/'
DEBUG = 1


def get_web_page(url: str):
    page = requests.get(url)
    text = page.text
    print('  read from url ', len(text), " CHARs")
    return text


def parse_web_page(html: str):
    soup = bs4.BeautifulSoup(html,  'lxml')
    table = soup.find_all('table')[0]
    links = table.findAll('a', {"class": "titlelink"})
    descs = table.findAll('td', {"class": "subtext"})

    print(f'BeautifulSoup extracted {len(links)} links, {len(descs)} desc')
    if len(links) != len(descs):
        raise ValueError('ERR len links/descs: ' + str(len(links)) + '!=' + str(len(descs)))
    points = []
    comments = []
    extract_points_and_comments(comments, descs, links, points)
    print(f'  after filtering {len(links)} links, {len(descs)} desc')
    return links, points, comments


def extract_points_and_comments(comments, descs, links, points):
    i = 0
    while i < len(links):
        point_spans = descs[i].find_all('span', {"class": "score"})

        if len(point_spans) == 0 or 'ycombinator.com' in links[i] \
                or 'http' not in str(links[i]):
            print('   removed invalid link', links[i])
            del (descs[i])
            del (links[i])
            continue
        point = int(point_spans[0].text[:-7])
        if point < 200:
            #print('   removed link with less than 200 pts')
            del (descs[i])
            del (links[i])
            continue
        points.append(point)
        txt = str(descs[i])
        i_end = txt.find('comments') - 1
        i_start = txt.find('>', i_end - 20) + 1
        comment = int(txt[i_start:i_end])
        comments.append(comment)
        links[i] = str(links[i]).replace('class="titlelink" ', '')
        i += 1


def get_url_desc(link):
    domain = util.get_domain(link).upper()
    desc = ''
    if 'twitter.com' in link or 'facebook.com' in link or 'linkedin.com' in link:
        desc = '🦜'
    elif 'youtube.com' in link:
        desc = '🎞️'
    elif '.edu' in link:
        desc = '🏫'
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
            'huffpost' in link or 'usatoday' in link or 'wsj.com' in link or \
            'politico' in link or 'reuters' in link or 'dailymail' in link or \
            'latimes' in link or 'reuters' in link or 'washingtonpost' in link or \
            'wsj.com' in link or 'theguardian' in link or 'usatoday' in link or \
            'npr.org' in link:
        desc += ' 📰'
    if 'java' in link or 'github' in link or 'linux' in link or 'computer' in link or \
            '.dev' in link or '.codes' in link or '.engineer' in link or '.software' in link:
        desc += ' 💻'
    if '.pdf' in link:
        desc += ' PDF'
    if 'video' in link or 'youtube' in link :
        desc += '🎞️'
    return desc.strip()


def get_url_legend(html):
    legend = 'Legend:   '
    if '🦜' in html:
        legend += '🦜 twitter/facebook'
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
    html = '\nBi-Weekly:  01-xxx  05-xxx  09-xxx  13-xxx  17-xxx  21-xxx\n' \
           '            02-xxx  06-xxx  10-xxx  14-xxx  18-xxx  24-xxx\n' \
           '            03-xxx  07-xxx  11-xxx  15-xxx  19-xxx  25-xxx\n' \
           '            04-xxx  08-xxx  12-xxx  16-xxx  20-xxx  26-xxx'
    return html


def scrape_ycombinator_links(month, day_start, day_end):
    year = datetime.datetime.today().year
    links = []
    points = []
    comments = []
    for day in range(day_start, day_end + 1):
        publish_date = f'{year}-{month:02d}-{day:02d}'
        print(' scraping', publish_date)
        url_sfx = 'front?day=' + publish_date
        ith_page = 1
        while True:
            url = HACKER_NEWS_URL + url_sfx + '&p=' + str(ith_page)
            # example: url = 'https://news.ycombinator.com/front?day=2022-01-01&p=1'
            if DEBUG:
                print(f'   page:{ith_page}, url:{url}')
            html = get_web_page(url)
            links_i, points_i, comments_i = parse_web_page(html)
            if len(links_i) == 0:
                break
            elif ith_page > 4:
                print('    possible ERR, more than 4 pages scanned')
                break
            annotate_links_i(links_i, comments_i, points_i, publish_date)
            links += links_i
            points += points_i
            comments += comments_i
            ith_page += 1
    return links, points, comments


def annotate_links_i(links_i, comments_i, points_i, publish_date):
    for j in range(len(links_i)):
        link = str(links_i[j])
        if '50-of-transactions-were-fraudulent' in link:
            print('[[[[link', link)
            print('====points', points_i[j])
            print('====comments', comments_i[j])
        title = '" ' + 'title="' + str(points_i[j]) + ' pts, ' \
                + str(comments_i[j]) + ' comments ' \
                + publish_date + '">'
        link = link.replace('">', title)
        desc = get_url_desc(link)
        if '50-of-transactions-were-fraudulent' in link:
            print('[[[[desc', desc)
            print('====link', link)
        if desc != '':
            link += ' <b>' + desc + '</b>'
        # if is_link_valid(link):
        links_i[j] = link


def append_lines(html, sort_order, links, sfx, max_link_cnt, web_page_links):
    zipped = zip(sort_order, links)
    links_sorted = list(zipped)
    links_sorted.sort(reverse=True, key=lambda y: y[0])
    # if DEBUG:
    #     print('    ---append_lines; links_sorted 1:\n     ', links_sorted[0:1])
    i = 0
    is_non_etc = sfx == '\n'
    for x in links_sorted:
        link = x[1]
        if is_non_etc and ('🦜' in link or '🪵' in link or '📰' in link):
            continue
        if link not in web_page_links:
            html += link + ', ' + "{:,}".format(x[0]) + sfx
            web_page_links.append(link)
            i += 1
            if i == max_link_cnt:
                break
    return html


def create_web_page(links, points, comments, top_count):
    html = "<html><head><meta charset='UTF-8'></head><title>Hacker news sort</title>\n" \
           "<body>Top <a href=\"{0}\">{1}" \
           "</a> links<pre>".format(HACKER_NEWS_URL, HACKER_NEWS_URL)
    html += '\n' + str(top_count) + ' top points:\n'
    web_page_links = []
    html = append_lines(html, points, links, ' points \n', top_count, web_page_links)

    html += '\n' + str(top_count) + ' top comments:\n'
    html = append_lines(html, comments, links, ' comments \n', top_count, web_page_links)

    point_comments = []
    for i in range(len(links)):
        point_comments.append(points[i] * comments[i])
    html += '\n' + str(top_count) + ' top points*comments:\n'
    html = append_lines(html, point_comments, links, ' points*comments\n', 5, web_page_links)

    html += '\n' + str(top_count) + ' top point non-🦜/🪵/📰:\n'
    html = append_lines(html, points, links, '\n', top_count, web_page_links)

    html += '\n' + get_url_legend(html)
    # if not is_weekly:
    #     html += '\n' + get_bi_week_links()
    html += '</pre></body></html>'
    return html.replace('\r', '')


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
            i1 = link.find('title="') + 7  # title="263 pts, 142 comments">
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


def write_file(html, file_path):
    with open(file_path, 'w') as f:
        f.write(html)
    print('Created ', file_path)


def date_parameters(month_abr, is_first_half_month):
    month_abrs = ['jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    if month_abr not in month_abrs:
        raise ValueError(month_abr + ' is not in: ' + str(month_abrs))
    month = month_abrs.index(month_abr) + 1
    year = datetime.datetime.today().year
    if is_first_half_month:
        day_start = 1
        day_end = 15
    else:
        day_start = 16
        test_date = datetime.datetime(year, month, 1)
        day_end = calendar.monthrange(test_date.year, test_date.month)[1]
    file_path = f'./HACKER_NEWS/{str(month).zfill(2)}_{month_abr}_{day_start}-{day_end}.html'
    if DEBUG:
        print(' --file_path', file_path)
    return file_path, month, day_start, day_end


def main():
    try:
        print('started')
        file_path, month, day_start, day_end = date_parameters('feb', 0)
        links, points, comments = scrape_ycombinator_links(month, day_start, day_end)
        html = create_web_page(links, points, comments, top_count=20)
        write_file(html, file_path)
        #webbrowser.open_new_tab(file_path)

        # file_path = './hacker_news_sort_all_weeks.html'
        # links, points, comments = read_all_weekly_sorts()
        # html = create_web_page(False, 20, start_date, links, points, comments)
        # write_file(html, file_path)
        # webbrowser.open_new_tab(file_path)

        print('done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
