import subprocess


def main():
    subprocess.run(['pyrcc5', './resource.qrc', '-o', './fluedit/resource_rc.py'], check=True)


if __name__ == '__main__':
    main()
