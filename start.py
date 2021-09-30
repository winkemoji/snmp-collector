import subprocess
import traceback

def start():
    res = subprocess.run(['python', 'superserver.py'])
    if res.returncode!=0:
        raise Exception


def main():
    try:
        start()
    except BaseException as e:
        traceback.print_exc()

if __name__ == '__main__':
    main()
