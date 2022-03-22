import logging
import os.path
import re
from datetime import datetime
from wpy.util import Util


class WebPage:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__link = WebPage._create_link(file_path)
        self.__topic, self.__sub_dir, self.__file_name = WebPage._find_topic(file_path)
        update_ts = os.path.getmtime(file_path)

        self.__modification_date = str(datetime.utcfromtimestamp(update_ts))[:10]
        self.__search_indexes = []
        self.__date_range = ''
        self.__page_count = 0
        if file_path.endswith('.html') or file_path.endswith('.txt'):
            lines = WebPage._read_file(file_path)
            self.__page_count = WebPage._find_page_count(file_path, lines)
            if 'test_' not in file_path:
                self.__search_indexes = WebPage._find_indexes(lines)
                self.__date_range = WebPage._find_date_range(lines)
        self.__kb_size = round(os.path.getsize(file_path) / 1000, 1)
        logging.debug(file_path)

    @staticmethod
    def _read_file(file_path):
        try:
            with open(file_path, encoding="utf-8") as f:
                lines = f.readlines()
                return lines
        except Exception:
            print('IO ERR file_path=', file_path)
            raise

    @staticmethod
    def _create_link(file_path):
        i_start = file_path.rindex('/') + 1
        if file_path.endswith('.html'):
            i_end = file_path.rindex('.html')
        elif file_path.endswith('.txt'):
            i_end = file_path.rindex('.txt')
        else:
            i_end = len(file_path)
        file_name = file_path[i_start:i_end].replace('_', ' ')
        file_name = file_name[0].upper() + file_name[1:]
        if file_path.endswith('test.html') or 'test_' in file_path or 'tmp' in file_path:
            style = ' class="test" style="font-size:0px;"'
        else:
            style = ''
        link = '<a href=\'./' + file_path + '\'' + style + '>' + file_name + '</a>'
        return link

    @staticmethod
    def _extract_italicized_labels(line):
        """
        >>> WebPage._extract_italicized_labels('aa <i>AAA</i> bbb <i>BBB</i> xxx<i>222</i>yyy<i>333</i>zzz')
        'aaa bbb 222 333'
        """
        s = re.sub("^(.*?)<i>", "", line)
        s = re.sub("</i>.*?<i>", " ", s)
        s = re.sub("</i>.*", "", s).strip().lower()
        return s

    @staticmethod
    def _find_indexes(lines):
        indexes = []
        for line in lines:
            # search for anchors:
            i = line.find('<a ')
            if i > -1:
                if line.find('</a>', i) < 1:
                    raise Exception('ERR missing </a> in line:\n\t' + line)
                ii = line.index('</a>', i) + 4
                link = line[i:ii]
                if 'name=' not in link:
                    print('++++ line', line)
                    print('++++ line', link)
                    label_url = Util.extract_url_label(link)
                    indexes.append(label_url)
            # search for italic keywords:
            i = line.find('<i>')
            if i > -1:
                labels = WebPage._extract_italicized_labels(line)
                indexes.append((labels,))
        return indexes

    @staticmethod
    def _find_page_count(file_path, lines) -> float:
        lines_per_page: int = 60
        is_html = file_path.endswith('html')
        if is_html:
            html = ''.join(lines)
            if '<table' in html:
                page_count = round(html.count('<tr') / lines_per_page, 1)
                return page_count
        line_count = 0
        is_body = False
        for line in lines:
            if is_html:
                if not is_body:
                    is_body = '<body' in line.lower()
                else:
                    line_count += 1
            elif len(line) > 0:
                line_count += 1
        page_count = round(line_count / lines_per_page, 1)
        return page_count

    @staticmethod
    def _find_date_range(lines) -> str:
        dates = []
        for line in lines:
            i = line.find('🗓')
            if i > -1:
                i2 = line.find('©️')
                if i2 > -1:
                    line = line[:i2]
                date = line[i + 1:].split("<")
                date = date[0].strip()
                fields = date.split(" - ")
                fields = fields[0].split("-")
                print('date--', date, 'fields===', fields)
                fields = [int(x) for x in fields ]
                fields = [str(x) if x > 9 else '0' + str(x) for x in fields]
                date = '-'.join(fields)
                dates.append(date)
        if len(dates) == 0:
            date_range = ''
        elif len(dates) == 1:
            date_range = dates[0]
        else:
            date_range = min(dates)[:4] + '..' + max(dates)[:4]
        return date_range

    @staticmethod
    def _find_topic(file_path):
        """
        >>> WebPage._find_topic('/w/a/b/f.html')
        ('a', 'b', 'f')
        >>> WebPage._find_topic('/w/a/f.html')
        ('a', '', 'f')
        """
        i_start = file_path.index('/w/') + 3
        i_end = file_path.index('/', i_start)
        topic = file_path[i_start:i_end]

        sub_path = file_path[i_end + 1:]
        sub_dir = ''
        if sub_path.find("/") > 0:
            i_end = sub_path.index('/')
            sub_dir = sub_path[:i_end]
        i_start = file_path.rfind('/') + 1
        i_end = len(file_path) if file_path.endswith('.jpg') else file_path.rfind('.')
        file_name = file_path[i_start:i_end]
        return topic, sub_dir, file_name

    @property
    def file_path(self) -> str:
        return self.__file_path

    @property
    def is_text(self) -> bool:
        return self.__file_path.endswith('.txt') or self.__file_path.endswith('.html')

    @property
    def file_name(self) -> str:
        return self.__file_name

    @property
    def link(self) -> str:
        return self.__link

    @property
    def date_range(self) -> str:
        return self.__date_range

    @property
    def kb_size(self) -> float:
        return self.__kb_size

    @property
    def page_count(self) -> float:
        return self.__page_count

    @property
    def search_indexes(self) -> list:
        return self.__search_indexes

    @property
    def topic(self) -> str:
        return self.__topic

    @property
    def sub_dir(self) -> str:
        return self.__sub_dir

    def __str__(self) -> str:
        return f'WebPage: file_path = {self.file_path}, link = {self.link}, ' + \
               f' date_range = {self.date_range}, kb_size = {self.kb_size}, ' + \
               f' search_indexes = {self.search_indexes} topic = {self.topic} ' + \
               f' sub_dir = {self.sub_dir}'


if __name__ == '__main__':
    import doctest

    # This runs only a couple of tests;
    doctest.testmod()
