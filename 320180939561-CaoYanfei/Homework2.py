# -*- coding: utf-8 -*-

__author__ = "Cao Yanfei"
__studentID__ = "320180939561"
__email__ = "caoyf18@lzu.edu.cn"
__version__ = "v1.0"

from subprocess import Popen, PIPE, DEVNULL
from matplotlib import pyplot as plt


class get_list:
    def __init__(self):
        self.data_get("D:\git_warehouse\linux-stable", "v4.5")

    def data_get(self, repo, ver):
        cmd_tag = 'git tag -l ' + '"' + ver + '.*"'
        v = Popen(cmd_tag, cwd=repo, stdout=PIPE)
        vtime, res = v.communicate()
        txt = vtime.decode('latin').encode('utf8').decode('utf8').split("\n")
        # print(txt)
        t_list = []
        for i in txt:
            cmd_get = 'git log -1 --pretty=format:\"%ct\" ' + str(i)
            t = Popen(cmd_get, cwd=repo, stdout=PIPE, stderr=DEVNULL)
            ttime, res1 = t.communicate()
            doc = ttime.decode('latin').encode('utf8').decode('utf8')
            t_list.append(doc)
        # print(t_list)
        self.draw(t_list, txt, ver)

    def draw(self, t_list, txt, ver):
        plt.scatter(t_list, txt)
        plt.title('release order with time')
        plt.xlabel('time')
        plt.ylabel('release order')
        plt.savefig('plot_{}.png'.format(ver))


a = get_list()
