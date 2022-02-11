w (web site)
============
The 'w' is a static web site project.
It is like a dynamic searchable book.

See `<./contents.html>`__ for more details

.. contents:: Contents:


View web site from github
-------------------------
|To view ``br1/main`` branches in browser click:
| <https://htmlpreview.github.io/?https://github.com/coaspo/rep/blob/br1/w/index.html>
| <https://htmlpreview.github.io/?https://github.com/coaspo/rep/blob/master/w/index.html>
|respectfully.


Run python (deploymnet-related) tests
-------------------------------------
|  From project dir, install pytest:
|    ``pip install -r requirements.txt``
|  May need to activate venv (see 'Notes'below) before doing this.
|
|  **In Pycharm:**
|   >File >Settings >Tools >Python-Integrated-Tools,
|   change >Default-test-runner to ``pytest``
|   select a test and > "run pytest"
|
|  **Outside pycharm:**
|   In command window, and in project dir, type:
|     ``python tests/run_all_pytests.py``
|   May run individual doc (limited) tests, for example:
|     ``python pi/webpage.py``


Run javascript tests
--------------------
| 1. Local tests
|   Run <./tests/start_local_server__open__test_search.html.py>.
|
|   The script stops/runs local server using:
|     ``fuser -k 8080/tcp``
|     ``python3 -m http.server 8080``
|   And displays
|     <http://localhost:8080/w/tests/test_search.html>
|
| 2. Remote tests
| Open <https://li.netlify.app/w/tests/test_search.html>.
|

Run python tests and check into github
--------------------------------------
|   In command window type:
|   ``python check_in.py``

Notes
-----
|**Best practice**
|  **Setup virtual env**:
|    ``pip3 install virtualenv``
|  Create env, from the project directory run:
|    ``virtualenv venv``
|
|  Activate virtual env
|    **In pycharm:**
|     >File >Settings >Project:w
|     Create ``venv`` in project folder and select project interpreter:
|     ``c:\..\w\venv\Scripts\python.exe``
|
|    **Outside pycharm:**
|       . venv/bin/activate
|
|  **After using a new library**, update ``requirements.txt``:
|   ``pip install pipreqs``
|   ``pipreqs pi``
|
|Updater requirments:
| ``pip freeze > requirements.txt``
|
Problems/Solutions
------------------
| Cannot run pytest (rt click tests dir ..)
| **FIX:** >File >Settings >Tools >Python-Integrated-Tools,
| change >Default-test-runner to pytest
|
| E   ModuleNotFoundError: No module named 'mock'
| **FIX:** In Terminal tab enter:
| ``pip install mock``