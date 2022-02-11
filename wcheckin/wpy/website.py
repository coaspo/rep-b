import logging
import os

from wpy.webpage import WebPage


class WebSite:
    def __init__(self, target_dirs):
        self.__file_path_structure = WebSite._get_search_file_path_structures(target_dirs)
        self.__topic_names, self.__pages_dict, self.__sub_dir_dict, self.__total_kb_size, \
            self.__total_page_count = WebSite._get_web_site_attrs(target_dirs)

    @staticmethod
    def _get_search_file_path_structures(target_dirs):
        file_path_structures = []
        for target_dir in target_dirs:
            for subdir, dirs, files in os.walk(target_dir):
                for file in files:
                    if file.endswith('.html') or file.endswith('.txt'):
                        p = subdir + '/' + file
                        file_path_structures.append([p, os.path.getmtime(p)])
        file_path_structures.sort(key=lambda x: x[0])
        # [print(x) for x in file_path_structures]total_page_count
        logging.info('WebSite; ' + str(len(file_path_structures)) + ' file paths; ' + str(target_dirs))
        return file_path_structures

    @staticmethod
    def _get_search_file_paths(target_dir):
        file_paths = []
        for subdir, dirs, files in os.walk(target_dir):
            for file in files:
                p = os.path.join(subdir, file)
                file_paths.append(p)
        file_paths.sort()
        logging.debug('WebSite; ' + str(len(file_paths)) + ' file paths')
        return file_paths

    @staticmethod
    def _get_web_site_attrs(target_dirs) -> (list, dict):
        web_page_dict = {}
        sub_dir_dict = {}
        topic_names = []
        total_kb_size = 0.
        total_page_count = 0
        for target_dir in target_dirs:
            i_start = target_dir.index('/w/') + 3
            topic_name = target_dir[i_start:]
            pages = []
            sub_dirs = []
            file_paths = WebSite._get_search_file_paths(target_dir)
            for file_path in file_paths:
                if not file_path.endswith('.js'):
                    # if file_path.endswith('.html') or file_path.endswith('.txt'):
                    page = WebPage(file_path)
                    total_kb_size += page.kb_size
                    total_page_count += page.page_count
                    pages.append(page)
                    if page.sub_dir not in sub_dirs:
                        sub_dirs.append(page.sub_dir)
            pages.sort(key=WebSite.sort_value, reverse=False)
            sub_dirs.sort(reverse=False)
            topic_names.append(topic_name)
            web_page_dict[topic_name] = pages
            sub_dir_dict[topic_name] = sub_dirs
        return topic_names, web_page_dict, sub_dir_dict, total_kb_size, total_page_count

    @staticmethod
    def sort_value(page: WebPage):
        if page.sub_dir == '':
            return 'a'*len(page.sub_dir) + page.file_path
        else:
            return page.sub_dir + page.file_path

    def save_search_file_paths(self, save_file):
        with open(save_file, 'w') as f:
            for p in self.file_path_structures:
                i_start = p[0].index('/w/') + 3
                f.write(p[0][i_start:])
                f.write('\n')

    @property
    def file_path_structures(self) -> list:
        return self.__file_path_structure

    @property
    def topic_names(self) -> list:
        return self.__topic_names

    @property
    def web_page_dict(self) -> dict:
        return self.__pages_dict

    @property
    def sub_dir_dict(self) -> dict:
        return self.__sub_dir_dict

    @property
    def total_kb_size(self) -> float:
        return self.__total_kb_size

    @property
    def total_page_count(self) -> float:
        return self.__total_page_count

    def save_search_labels(self, save_file):
        with open(save_file, 'w') as f:
            f.write('')
        is_first = True
        for i, x in enumerate(self.file_path_structures):
            if 'problem' in x[0]:
                continue
            web_page = WebPage(x[0])
            indexes = web_page.search_indexes
            if len(indexes) > 0:
                with open(save_file, 'a') as f:
                    for attrs in indexes:
                        if not is_first:
                            f.write('\n')
                        else:
                            is_first = False
                        f.write(attrs[0])  # anchor label or table header
                        f.write('$$')
                        f.write(str(i))  # file index number
                        if len(attrs) > 1:
                            f.write('$$')
                            f.write(attrs[1])  # url
        logging.info('Created ' + save_file)

    def __str__(self) -> str:
        return f'WebSite: file_paths = {self.file_path_structures} \n' + \
               f'         web_pages = {self.web_page_dict} '
