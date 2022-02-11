import logging
import tkinter
import traceback
from datetime import datetime
from tkinter import simpledialog
from typing import List

from wpy.webpage import WebPage
from wpy.website import WebSite
from wpy.util import Util


class ContentsPage:
    UPDATE_LINE_MARKER = '<!--c-marker:-->'

    @staticmethod
    def update(web_site: WebSite, contents_file_path: str):
        (version, lines) = ContentsPage._get_version(contents_file_path)
        if version is None:
            print('stopped; version not given')
            exit()
        ContentsPage._update_contents(version, lines, web_site, contents_file_path)
        logging.info('Updated ' + contents_file_path)
        return version

    @staticmethod
    def _update_contents(version, lines, web_site, contents_file_path):
        try:
            with open(contents_file_path, 'w') as f:
                for line in lines:
                    if ContentsPage.UPDATE_LINE_MARKER in line:
                        f.write(line)
                        ts = datetime.now().isoformat()
                        num = ts[2:10] + '/' + ts[11:13] + ts[14:16] + ts[17:19]
                        version_line = '\n<pre>Version: ' + num + '; ' + version + '\n'
                        f.write(version_line)
                        ContentsPage._append_content_links(web_site, f)
                        break
                    f.write(line + '\n')
                f.write('\n</body></html>')
        except Exception as ex:
            logging.exception(ex)
            print(traceback.format_exc())
            with open(contents_file_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
                f.close()
            raise ex

    @staticmethod
    def _append_content_links(web_site: WebSite, f):
        lines = ''
        path_max_len = -1
        topics = web_site.topic_names
        for topic_name in topics:
            web_pages = web_site.web_page_dict[topic_name]
            for page in web_pages:
                length = len(page.sub_dir + page.file_name)
                if length > path_max_len:
                    path_max_len = length
        topics.sort()
        for topic_name in topics:
            web_pages = web_site.web_page_dict[topic_name]
            lines += ContentsPage._get_file_links_list(web_pages, path_max_len)
        f.write(lines)
        f.write('\n all of above files: ')
        f.write("{:,.1f}".format(web_site.total_page_count))
        f.write(' PGS;  ')
        f.write("{:,.0f}".format(web_site.total_page_count)*60)
        f.write(' lines;  ')
        f.write("{:,.1f}".format(web_site.total_kb_size))
        f.write(' kB')

    @staticmethod
    def _get_version(contents_file_path):
        with open(contents_file_path) as f:
            lines = f.read().splitlines()

        version = 'UNK'
        for line in lines:
            if line.startswith('<pre>Version:'):
                version = line.split('; ')[1].strip()
                break
        root = tkinter.Tk()
        root.withdraw()
        version = simpledialog.askstring(title="Git check-in;  " + __file__,
                                         prompt=("\nUpdate 'Search contents' related files and check into git.   "
                                                 "\n\nVersion name:"), initialvalue=version)
        return version, lines

    @staticmethod
    def _get_file_links_list(web_pages: List[WebPage], path_max_len):
        web_pages.sort(key=lambda x: x.file_path, reverse=False)

        lines: str = ''
        prev_topic = ''
        prev_sub_dir = ''
        is_first_file = False
        is_odd = True
        for page in web_pages:
            topic = page.topic.title()
            sub_dir = page.sub_dir.title()
            pfx = ''
            if topic != prev_topic:
                pfx = '\n<b>' + topic.upper() + '</b>\n'
            lines += pfx

            pfx = '  '
            if sub_dir != prev_sub_dir and sub_dir != '':
                pfx = '  ' + sub_dir + ' '
            elif sub_dir != '':
                pfx = '  ' + ' ' * len(sub_dir) + ' '
            lines += pfx

            link = Util.add_mouse_listeners(page.link)
            lines += link
            if pfx == '  ':
                lines += ' '
            ch = '.' if is_odd else ' '
            lines += ch * (5 + path_max_len - len(page.sub_dir + page.file_name))
            date = page.date_range
            date += ch * (10 - len(date))
            pg_cnt = str(page.page_count)
            if pg_cnt[0:1] == '0':
               pg_cnt = ' ' + pg_cnt[1:]
            lines += date + '  ' + pg_cnt
            if not is_first_file:
                is_first_file = True
                lines += ' <u title="60 lines/page">PGS</u>'
            lines += '\n'
            prev_topic = topic
            prev_sub_dir = sub_dir
            is_odd = not is_odd
        return lines
