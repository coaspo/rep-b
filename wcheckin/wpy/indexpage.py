import logging
import traceback


class IndexPage:
    @staticmethod
    def update_links(website, file_path):
        with open(file_path) as f:
            lines = f.read().splitlines()
        line = 'NA'
        try:
            with open(file_path, 'w') as f:
                f.write(lines[0])
                j = 1
                while j < len(lines):
                    line = lines[j]
                    i_start = line.find('<!--*/')
                    if i_start > -1:
                        f.write('\n' + line)
                        i_end = line.index('-->')
                        topic = line[i_start+6:i_end]
                        print('IndexPage.update_links() topic=', topic)
                        webpages = website.web_page_dict[topic]
                        prev_sub_dir = ''
                        for page in webpages:
                            if '.jpg' in page.link:
                                continue
                            sub_dir = page.sub_dir
                            if len(sub_dir) > 0:
                                sub_dir += '<br>'
                            if sub_dir == '':
                                f.write('\n')
                            else:
                                if sub_dir != prev_sub_dir:
                                    dir_label = sub_dir.replace('_','').replace('-',' ')
                                    dir_label = '-'+dir_label.capitalize()
                                    f.write('\n' + dir_label)
                                else:
                                    f.write('\n')
                            if sub_dir != '':
                                f.write('&emsp;')  # 6-per-em space
                            prev_sub_dir = sub_dir
                            i = page.link.index('>') + 1
                            link = page.link[:i] + page.link[i:i+1].upper() + page.link[i+1:]
                            # if topic == 'apps':
                            #     f.write('<br>')
                            f.write(link)
                            f.write('<br>')
                        while line.find('<!--*/END-->') < 0:  # remove previous lines
                            j += 1
                            line = lines[j]
                        f.write('\n<!--*/END-->')
                    else:
                        f.write('\n' + line)
                    j += 1
        except Exception as e:
            logging.error(str(e))
            print('ERR line: ', line, '\n', traceback.format_exc())
            with open(file_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            raise e
        logging.info('Updated index.html')


if __name__ == '__main__':
    import doctest

    # This runs just a couple of tests;
    doctest.testmod()
