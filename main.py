import os
import sys
import shutil
from PIL import Image

rootdir = sys.argv[1]
max_mb = int(sys.argv[2])
# rootdir = 'C:\\Users\Shohoo\\Desktop\\chiny'
# max_mb = 2

class Resizator:
    def __init__(self, dir, max_mb):
        self.root_dir = os.path.abspath(dir)
        self.new_dir = self.root_dir + '-thumbnails'
        if os.path.exists(self.new_dir):
            shutil.rmtree(self.new_dir)
            while os.path.exists(self.new_dir):
                pass
        os.makedirs(self.new_dir)
        self.max_mb = max_mb
        self.execute()
        pass

    def execute(self):
        for root, sub, files in os.walk(self.root_dir):
            rel_root_path = os.path.relpath(root, self.root_dir)
            for folder in sub:
                rel_dir_path = os.path.join(rel_root_path, folder)
                dir_path = os.path.join(self.new_dir, rel_dir_path)
                self.do_dir(dir_path)

            for file in files:
                rel_file_path = os.path.join(rel_root_path, file)
                file_path = os.path.join(root, file)
                new_file_path = os.path.join(self.new_dir, rel_file_path)
                self.do_file(file_path, new_file_path)

    def do_dir(self, dir_path):
        print('Creating dir ' + dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def if_oversized(self, path):
        return (os.path.getsize(path) / 1024 / 1024) > self.max_mb

    def resize(self, im):
        width, height = im.size
        im.thumbnail((0.9 * width, 0.9 * height), Image.ANTIALIAS)

    def do_file(self, path, new_path):
        print('Copying file ' + path)
        try:
            im = Image.open(path)
        except IOError:
            print('Is not image file ' + path)
            return

        print('Saving to ' + new_path)
        if self.if_oversized(path):
            self.resize(im)
        im.save(new_path)
        while self.if_oversized(new_path):
            print('Resizing file ' + path)
            im = Image.open(new_path)
            self.resize(im)
            im.save(new_path)
        pass


r = Resizator(rootdir, max_mb)
print('end')
