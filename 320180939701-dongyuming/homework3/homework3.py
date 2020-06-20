# -*- coding: utf-8 -*-

__author__ = "Yuming Dong 320180939701"
__copyright__ = "Copyright 2020, LZU Data Science"
__version__ = "1.0.0"

from subprocess import Popen, PIPE, DEVNULL
from matplotlib import pyplot as plt

def get_list(repo,ver):
    cmd_tag = 'git tag -l ' + '"'+ ver + '.*"'
    v = Popen(cmd_tag, cwd = repo, stdout=PIPE)
    vtime, res = v.communicate()
    txt = vtime.decode('latin').encode('utf8').decode('utf8').split("\n")
    #csv_file = open('test.csv', 'w', newline='', encoding='utf8')
    #writer = csv.writer(csv_file)
    print(txt)
    t_list = []
    for i in txt:
        data_get = 'git log -1 --pretty=format:\"%ct\" ' + str(i)
        t = Popen(data_get, cwd = repo, stdout=PIPE, stderr=DEVNULL)
        ttime, res1 = t.communicate()
        doc = ttime.decode('latin').encode('utf8').decode('utf8')
        t_list.append(doc)
    print(t_list)
    plt.scatter(t_list, txt)
    plt.title('release order with time')
    plt.xlabel('time')
    plt.ylabel('release order')
    plt.savefig('plot%s.png' % ver)

get_list("E:\SourceTreeClone\linux-stable\linux-stable", "v4.5")