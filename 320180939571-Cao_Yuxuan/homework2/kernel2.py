# -*- coding: utf-8 -*-


__license__ = "GPL V2"
__author__ = "Cao Yuxuan"
__version = '1.0'


import re
import pandas as pd
import time
from subprocess import Popen, PIPE, DEVNULL
import unicodedata
import matplotlib.pyplot as plt
import numpy as np



def get_list(kernels, repo):  #get the list of times in a kernel
    total_time_stamp_list = []

    for version in kernels:
        cmd = 'git tag | grep {} | sort -n -k3 -t"."'.format(version)
        p = Popen(cmd, cwd=repo, stdout=PIPE, shell=True)
        data, res = p.communicate()
        data = data.decode('latin').encode('utf8').decode('utf8').split("\n")
        time_stamp_list = []

        for v in data:
            cmd_1 = 'git log -1 --pretty=format:"%ct" {}'.format(v)
            p = Popen(cmd_1, cwd=repo, stdout=PIPE, shell=True)
            time_stamp, res = p.communicate()
            time_stamp = int(time_stamp.decode('latin').encode('utf8').decode('utf8'))
            # time_stamp=("%e" %int(time_stamp))
            # value=time.mktime(time.strptime(time_stamp,'%Y-%m-%d %H:%M:%S'))
            time_stamp_list.append(time_stamp)

        total_time_stamp_list.append(time_stamp_list)

    print(total_time_stamp_list)

    return (total_time_stamp_list)


def make_picture(all_time_stamp_list):  #make the picture and show it
    count_value = 0
    for i in all_time_stamp_list:
        j = []
        for a in range(len(i)):
            j.append(count_value)
        count_value = count_value + 1
        # plt.scatter(i,j)
        plt.xlim(1.42e+09, 1.49e+09)
        # plt.ylim(0,10)
        plt.xlabel('seconds')
        plt.ylabel('patchlevel')
        plt.scatter(i, j)
        plt.title ('timestamps')
    plt.show()


repo = '/Users/tsaoyuxuan/linux-stable'
versions = ['v4.1', 'v4.2', 'v4.3', 'v4.4', 'v4.5', 'v4.6', 'v4.7', 'v4.8', 'v4.9']
total_time_stamp_list = get_list(versions, repo)
make_picture(total_time_stamp_list)