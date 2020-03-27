#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 ShenJiacheng, lzu All Rights Reserved
"""
Simple program on finding all commits of a range starting at a git revision.
Educational purpose only, do not use for other purpose please!
"""

__author__ = "ShenJiacheng"
__address__ = 'Lanzhou University'
__studentID__ = "320180940191"
__date__ = "3/18/2020"
__email__ = "shenjch18@lzu.edu.cn"

import re, argparse, os
os.system("pip install prettytable")  # in case you don't have prettytable module which is a perfect module for
# formatted output
import prettytable as pt
from subprocess import Popen, PIPE, DEVNULL


class Rev:
    """
    One revision as an instance
    """
    def __init__(self, rev, revrange):
        """
        revision name and the range should be provided of an instance
        :param rev:
        :param revrange:
        """
        self.rev = rev
        self.revrange = revrange
        self.repo = 'D:\git repository\linux-stable'

    def get_commit_cnt(self, next_rev):
        """
        return the length of commits log from base revision to the target revision
        :param next_rev:
        :return:
        """
        tagrange = self.rev + ".." + next_rev
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tagrange
        git_rev_list = Popen(gitcnt, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) == 0:
            raise TagNotExistError("No such revision range: {0}..{1}, please check tag again!"
                                   .format(self.rev, self.rev + str(self.revrange)))
        return len(cnt)

    def get_tag_days(self, rev):
        """
        return the days between the target revision to the base
        :param rev:
        :return:
        """
        SecPerHour = 3600
        HourPerDay = 24
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_tag_date = Popen(gittag, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = int(git_tag_date.communicate()[0])
        day = seconds // (SecPerHour * HourPerDay)
        return day

    def get_log(self, rev2):
        """
        return the days and commit log, return False if no revision exist.
        :param rev2:
        :return:
        """
        commit_cnt = self.get_commit_cnt(rev2)
        if commit_cnt:
            current = self.get_tag_days(rev2)
            base = self.get_tag_days(self.rev)
            days = current - base
            return days, commit_cnt
        else:
            return False

    def log_print(self):
        """
        print out the result in a pretty way, and load it into a file.
        :return:
        """
        print("it takes time, please wait")
        tb = pt.PrettyTable()
        tb.field_names = ["version", "days", "commits"]
        for sl in range(1, self.revrange+1):
            print(".")
            rev2 = self.rev + "." + str(sl)
            days, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                tb.add_row([rev2, days, commit_cnt])
            else:
                break
        with open('result', 'a') as f:
            f.write(str(tb))
        print(tb)
        print('The result has been written into "result" file')


class TagError(Exception):
    def __init__(self, msg):
        self.msg = msg


class TagNotExistError(TagError):
    pass


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("revision", help="the version tag you want to start checking, example: v4.1")
        parser.add_argument("range", type=int, help="the range of revision you want to check")
        args = parser.parse_args()
        rev_in = args.revision
        range_in = args.range
        rev = Rev(rev_in, int(range_in))
        rev.log_print()
    except TypeError:
        print('argument type wrong: the first arg should be like"v4.1", and the second should be an int.')


if __name__ == "__main__":
    main()
