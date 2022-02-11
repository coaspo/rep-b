from subprocess import Popen, PIPE
from sys import exit


def run(*args: str):
    print('\nCMD:', args)
    p = Popen(args, shell=True, stdout=PIPE, stderr=PIPE)
    o, e = p.communicate()
    output = o.decode("utf-8").replace('\r', '')
    errs = e.decode("utf-8").replace('\r', '')
    print('output:', output)
    print('errs:', errs)


def run_all():
    print('Started', __file__)
    run(r'../venv/bin/activate')
    run('pytest',  '../tests')
    print('done')


if __name__ == '__main__':
    run_all()