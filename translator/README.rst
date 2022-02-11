translator
==========
Project illustrates MVC in python.

It uses **googletranslate** and saves translated words into
a local json file.
User input and translation may be saved and viewed later.

.. contents:: Contents:


Get application
----------------
| Use git-bash to clone the repo:
|    ``git clone https://github.com/coaspo/rep``
|   To get a brach, for example ``br1``:
|    ``git pull origin br1``
| Or download zip file from github.

Run app
-------
|  Install python 3 and add it to path.
|  (Optional) Update pip:
|  ``python -m pip install --upgrade pip``
|
|  From project dir, run the commands:
|  ``pip install -r requirements.txt``
|  ``python cli.py``
|
|  May review info and error MSGs in:
|  ``logs\translator-YYYY-MM.log``

Run tests
---------
|  **In Pycharm:**
|   >File >Settings >Tools >Python-Integrated-Tools,
|   change >Default-test-runner to ``pytest``
|   select a test and > "run pytest"
|
|  **Outside pycharm:**
|   Double click ``c:\..\translator\run-tests.bat``

Notes
-----
|  **Best practice**, create virtual env:
|    ``pip install virtualenv``
|    ``virtualenv venv``
|
|    **Work in pycharm:**
|     >File >Settings >Project:translator
|     Should be able to select:
|     ``c:\..\translator\venv\Scripts\python.exe``
|
|    **Work outside pycharm:**
|     Activate venv (add bin to ``%PATH%``)
|       ``cd c:\..\translator``
|       ``.\venv\Scripts\activate.bat``
|       When done, deactivate Path. ``%PATH%``:
|       ``.\venv\Scripts\deactivate.bat``
|
|  **After using a new library**, update ``requirements.txt``:
|   ``pip install pipreqs``
|   ``pipreqs ltrans``


Problems/Solutions
------------------
| Cannot run pytest (rt click tests dir ..)
| **FIX:** >File >Settings >Tools >Python-Integrated-Tools,
| change >Default-test-runner to pytest
|
| ``E   ModuleNotFoundError: No module named 'googletrans'``
| **FIX:** Click on ``import googletrans`` and slect fix
| Cause(?): ``venv`` created before running:
|   ``pip install -r requirements.txt``
|  May need to install package: >File >Settings.... >project:translator >project-interpreter + ..
|
| on running pytest: ``found = cls._search_paths(context.pattern, context.path) AttributeError: 'str' object has no attribute 'pattern'``
| **FIX:** from project dir, run ``./venv/Scripts/activate.bat``
|