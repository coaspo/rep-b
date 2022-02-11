import recreate_w_index_contents_and_details_pages
import run_all_pytests


if __name__ == '__main__':
    print('--cli start')
    run_all_pytests.run_all()
    print('--run_all_pytests done')
    recreate_w_index_contents_and_details_pages.run_controller()
    print('--recreate_w_index_contents_and_details_pages done')
    print('--cli done')