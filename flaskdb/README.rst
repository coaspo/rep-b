w-todo
==========
A python "hello-world"-type web app.

[This is a code that comes along with great tutorial](https://medium.com/@bhavaniravi/build-your-1st-python-web-app-with-flask-b039d11f101c)

### To Run App in Docker

1. Checkout `Dockerfile`. It is created by [following this tutorial](https://runnable.com/docker/python/dockerize-your-flask-application).
2. I have changed it to accomodate latest version of ununtu and `python3`
3. To build docker image `docker build -t todo-flask:latest .`
4. To run the docker container `docker run -it -p 5000:8888 todo-flask `


Get application
----------------
| Use git-bash to clone the repo:
|    ``git clone https://github.com/bhavaniravi/flask-tutorial/``
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
