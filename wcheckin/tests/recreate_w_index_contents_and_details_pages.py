import os
import traceback
import wpy.controller


def run_controller():
    if os.getcwd().endswith('/tests'):
        os.chdir('..')
    try:
        wpy.controller.update_index_and_contents_pages()
        print('index and contents pages updated')
    except Exception:
        print(traceback.format_exc())


if __name__ == '__main__':
    run_controller()
