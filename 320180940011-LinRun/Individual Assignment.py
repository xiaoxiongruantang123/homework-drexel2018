#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Group04"
__copyright__ = "Copyright 2020, Lanzhou University"
__credits__ = ["Group04"]
__license__ = "GPL V3"
__version__ = "1.0"
__maintainer__ = "LinRun"
__email__ = "linr18@lzu.edu.cn"
__status__ = "Production"


import subprocess, re
import matplotlib.pyplot as plt


class GetVersionTime():
    """
    Get the plot of versions and the relative days.
    """
    def __init__(self, address):
        self.address = address
        self.versions = self.get_version()

    def get_version(self):
        """
        Returns the list of versions.
        """
        git_tag = subprocess.Popen("git tag", cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        git_tag = re.findall('v[0-9].[0-9]', str(git_tag.communicate()[0]))
        versions = []
        for i in git_tag:
            if i not in versions:
                versions.append(i)
        versions.pop(0)
        versions.pop()

        return versions

    def get_time(self):
        """
        Returns the list of the time of each versions.
        """
        seconds_times = []
        sec_per_day = 24 * 3600

        for i in range(0,len(self.versions)):
            gittag = "git log -1 --pretty=format:\"%ct\" " + self.versions[i]
            git_rev_list = subprocess.Popen(gittag, cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            tag_counts = git_rev_list.communicate()[0]
            if i == 0:
                seconds_times.append(int(tag_counts))
            else:
                seconds_times.append((int(tag_counts) - seconds_times[0]) // sec_per_day)

        seconds_times[0] = 0
        return seconds_times

    def draw_time_versions(self):
        plt.scatter(self.get_time(),self.versions)
        plt.title("Version modify days")
        plt.xlabel("days")
        plt.ylabel("version")
        plt.show()


if __name__ == "__main__":
    address = "/home/ytliu/linux-next/fs/afs/"
    extracor = GetVersionTime(address)
    extracor.draw_time_versions()
