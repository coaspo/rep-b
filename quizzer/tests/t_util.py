import ntpath
import os
import shutil


def recreate_tmp_dir(file_path):
    tmp_dir = os.path.dirname(file_path) + '/tmp'
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    mod_name = ntpath.basename(file_path)
    tmp_dir = tmp_dir + '/' + mod_name[: len(mod_name)-3]
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    path = str(os.path.abspath(tmp_dir))
    return path
