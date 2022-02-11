import logging
import os
import traceback
from tkinter import messagebox

import wpy.controller
from wpy.log import config_log


def update_search_and_index_files_of_w_project_and_check_in_branch_br1():
    try:
        log_file_name = os.path.basename(__file__) + '.log'
        config_log(log_file_name)
        wpy.controller.main('br1')
    except Exception as e:
        logging.error(traceback.format_exc())
        print(traceback.format_exc())
        messagebox.showerror('Exception ERR', os.path.basename(__file__) + ' FAILED; \n\n' + str(e))


if __name__ == '__main__':
    update_search_and_index_files_of_w_project_and_check_in_branch_br1()
