#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Dongchunyao, Linruyu, Weidanni, Wangyixuan, Maziqiang"
__studentID__ = "320180939690，320180940000，320180940370, 320180940330 "
__email__ = "dongchy18@lzu.edu.cn, linry18@lzu.edu.cn, weidn18@lzu.edu.cn, wangyixuan2018@lzu.edu.cn，mazq18@lzu.edu.cn"
__version__ = "v1.0"

import subprocess, re
import matplotlib.pyplot as plt

class Get_Versions_Time():
    '''
    This class can get the plot of relation the versions and days.
    '''
    def __init__(self, address):
        '''
        address: the git address
        '''
        self.address = address
        self.versions = self.get_version()

    def get_version(self):
        '''
        get the versions. Because of too many small version in big version, in order to display
        better the data just use the big version.

        return the list of versions.
        '''
        gittag = subprocess.Popen("git tag", cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        gittag = re.findall('v[0-9].[0-9].[0-9]', str(gittag.communicate()[0]))
        gitversions = []
        for i in gittag:
            if i not in gitversions:
                gitversions.append(i)
        gitversions.pop(0) #my clone git cannot find the time of the first version 2.6 so i deleted it.
        gitversions.pop()
        return gitversions

    def get_time(self):
        '''
        get the modify time of each version.

        return the list of each time.
        '''
        seconds_times = []
        for i in range(0,len(self.versions)):
            gittag = "git log -1 --pretty=format:\"%ct\" " + self.versions[i]
            git_rev_list = subprocess.Popen(gittag, cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            tag_counts = git_rev_list.communicate()[0]
            if i == 0:
                seconds_times.append(int(tag_counts))
            else:
                seconds_times.append((int(tag_counts) - seconds_times[0])//24//3600)
        seconds_times[0] = 0
        print(len(seconds_times),len(self.versions))
        return seconds_times

    def draw_time_versions(self):
        '''
        draw the plot.
        '''
        plt.scatter(self.get_time(),self.versions)
        plt.title("Version modify days")
        plt.xlabel("days")
        plt.ylabel("version")
        plt.show()


if __name__ == "__main__":
    address = "/Users/apple/linux-stable"
    a = Get_Versions_Time(address)
    print(a.draw_time_versions())

