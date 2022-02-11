import os
import shutil
import ntpath
import logging
root = logging.getLogger()
root.setLevel(os.environ.get("LOG_LEVEL","INFO"))


def recreate_tmp_dir(filepath):
    tmp_dir = os.path.dirname(filepath) + '/tmp'
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    mod_name = ntpath.basename(filepath)
    tmp_dir = tmp_dir + '/' + mod_name[: len(mod_name)-3]
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    path = str(os.path.abspath(tmp_dir))
    return path
