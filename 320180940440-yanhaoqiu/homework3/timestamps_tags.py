#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Homework of kernel2:
plot a scatter of timestamps of all tags for all kernel versions"""

__license__ = "GPL V2"
__author__ = "Haoqiu Yan"

from subprocess import Popen, PIPE, DEVNULL
import matplotlib.pyplot as plt


def get_tags(repo):
    """Query 'git tag' in linux-stable, and get releases of [v2.6.1, v2.6.2...]"""
    cmd_tag = 'git tag'
    p = Popen(cmd_tag, stdout=PIPE, stderr=DEVNULL, shell=True, cwd=repo)
    data_releases, _ = p.communicate()
    releases = [release for release in data_releases.decode("utf-8").split("\n") if release]
    return releases


def tags_sort(releases):
    """Sort releases of [v2.6.1, v2.6.2...] ascending.
    For va.b.c:
    first: sort c
    second: sort b
    then: sort a"""
    def ckey_sort(tag):
        """To sort c"""
        try:
            return int(tag.split('.')[2].split('-')[0])
        except IndexError:
            # some tags do have only two terms: v3.1-rc1
            return 0

    releases_c = sorted(releases, key=lambda tag: ckey_sort(tag))
    releases_b = sorted(releases_c, key=lambda tag: int(tag.split('.')[1].split('-')[0]))
    releases_a = sorted(releases_b, key=lambda tag: int(tag.split('.')[0][1:]))
    return releases_a


def plot_scatter(x_times, sub_versions):
    """Plot a scatter, taking timestamps as x-axis, and patch level as y-axis.
    ---Paragrams---
    x_times: [[1119037709, 1113690036, 1114039461], [6666666, 77777777, 88888888], ...]
    sub_versions: [v2.6.1, v2.6.2, ...]"""
    j = 0
    for x_time in x_times:
        y_version = [sub_versions[j] for i in range(len(x_time))]
        plt.scatter(x_time, y_version)
        j += 1
    plt.xlabel("timestamps")
    plt.ylabel("patch level in linux-stable")
    plt.title("timestamps of all tags for all kernel versions")
    plt.show()


def get_times(repo):
    """Query 'git log' in linux-stable, and get timestamps of all kernel versions"""
    releases = get_tags(repo)
    releases_sorted = tags_sort(releases)
    i = 0
    patch_time = []  # store tags' times which are the same patch level
    patch_times = [] # store patch_times
    sub_versions = [] # store patch levels
    for version in releases_sorted:
        i += 1
        print("version: ", version)
        cmd_time = ['git', 'log', '-1', '--pretty=format:\"%ct\"', version]
        p = Popen(cmd_time, stdout=PIPE, stderr=DEVNULL, shell=True, cwd=repo)
        data_dates, _ = p.communicate()
        if len(version.split('.')) == 2:
            # filter the tags that are the same patch level
            sub_versions.append(version)
            patch_times.append(patch_time)  # save patch_time
            patch_time = []  # initialize patch_time
        else:
            try:
                time = int(data_dates.decode("utf-8").replace('\"', ''))
            except ValueError:
                print("data_dates.decode(\"utf-8\"): ", data_dates.decode("utf-8"))
                time = 0
            patch_time.append(time)  # add times which are the same patch level
        print("patch_time", patch_time)
        print("data_dates", data_dates)
        print("sub_versions", sub_versions)
    del (patch_times[0])  # delete the first null element
    return patch_times, sub_versions


def main(repo):
    """Main function, which plots a scatter of timestamps of all tags for all kernel versions"""
    patch_times, sub_versions = get_times(repo)  # get x_times and y_tags
    plot_scatter(patch_times, sub_versions)


if __name__ == '__main__':
    # set the linux-stable.git path
    repo = r'C:\Users\admin\Desktop\linux-stable'
    main(repo)
