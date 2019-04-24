import os
import sys
import time
import subprocess


class Builder:
    def __init__(self, source):
        self.files = {}
        if source[-1] not in ['\\', '/']:
            source += '/'
        self.source = source
        self.output = './fluedit/ui'

    def build(self):
        self._tick(True)

    def _tick(self, build_all):
        ls = {}
        for dirpath, _, filenames in os.walk(self.source):
            for file in filenames:
                if file.endswith('.ui'):
                    file = os.path.join(dirpath, file)
                    ls[file] = os.stat(file)
        if build_all:
            for file in ls:
                self._pyuic5(file, self.output)
        else:
            diff = dict()
            for k, v in ls.items():
                cur = self.files.get(k)
                if not cur:
                    diff[k] = v
                else:
                    if cur.st_mtime != v.st_mtime:
                        diff[k] = v

            for file in diff:
                print(file)
                self._pyuic5(file, self.output)

            self.files.update(diff)

    def _pyuic5(self, source, dest):
        path = os.path.commonprefix([source, self.source])
        path = os.path.split(source[len(path):])
        out_dir = os.path.join(self.output, *path[:-1])

        try:
            os.makedirs(out_dir)
        except FileExistsError:
            pass

        out = os.path.join(out_dir, path[-1].rsplit('.ui', 1)[0] + '.py')
        subprocess.run(['pyuic5', source, '-o', out], check=True)

    def watch(self):
        while True:
            self._tick(False)
            time.sleep(2)


def main():
    builder = Builder('./ui')
    if len(sys.argv) > 1 and sys.argv[1] == '-w':
        builder.watch()
    else:
        builder.build()


if __name__ == '__main__':
    main()
