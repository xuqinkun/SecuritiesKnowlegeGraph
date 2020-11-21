# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
import os.path as path
import random
import shutil

_1MB = 1024*1024


class SecuritiesPipeline(object):

    def process_item(self, item, spider):
        f = open('executive_prep.csv', 'a', encoding='utf8')
        write = csv.writer(f)
        write.writerow((item['name'], item['sex'], item['age'], item['code'], item['jobs']))
        return item


def init_dir(parent_dir, deep, sub_dir_num, dir_ret):
    if deep < 1:
        return
    dirs = os.listdir(parent_dir)
    n = len(dirs)
    for i in range(sub_dir_num):
        if n < sub_dir_num:
            sub_dir = str(random.randint(1000, 9999))
            os.chdir(parent_dir)
            create_dir(sub_dir)
            dir_ret.append(path.abspath(sub_dir))
            print("Create dir %s in deep=%s" % (path.abspath(sub_dir), deep))
            init_dir(path.abspath(sub_dir), deep - 1, sub_dir_num, dir_ret)
        elif deep > 1:
            init_dir(path.join(parent_dir, dirs[i]), deep - 1, sub_dir_num, dir_ret)
        elif deep == 1 and path.isdir(path.join(parent_dir, dirs[i])):
            dir_ret.append(path.join(parent_dir, dirs[i]))
        n += 1
    pass


class FilePipeline(object):

    def __init__(self):
        self.index = 0
        self.total_files = 10
        self.sub_dir_num = 2
        self.text_repo = path.abspath('txt_lib')
        self.books_repo = path.abspath("books")
        self.dirs = []
        self.files = []
        create_dir(self.text_repo)
        create_dir(self.books_repo)
        init_dir(path.abspath(self.text_repo), 3, self.sub_dir_num, self.dirs)
        stack = [self.text_repo]
        while len(stack) != 0:
            obj = stack.pop()
            if path.isdir(obj):
                for d in os.listdir(obj):
                    stack.append(path.join(obj, d))
            else:
                self.files.append(obj)
        pass

    def next_dir_file(self):
        self.index += 1
        return self.files[self.index - 1]

    def process_item(self, item, spider):
        title = str(item['title']).strip()
        author = str(item['author']).strip()
        content = str(item['content'])
        book_name = title + "_" + author + ".txt"
        file_name = str(self.next_dir_file())

        with open(file_name, "a") as f:
            print(file_name)
            while not path.exists(file_name) or path.getsize(file_name) < _1MB:
                f.write(content)
        pass


def create_dir(dir_name):
    if not path.exists(dir_name):
        # shutil.rmtree(dir_name)
        os.mkdir(dir_name)
