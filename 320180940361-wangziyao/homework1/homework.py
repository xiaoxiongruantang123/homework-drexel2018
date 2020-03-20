#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a program which can find all commits since the git revision.
The author is Professor Nicholas and I made some changes with ShenJiacheng.

author:Professor Nicholas
editor:WangZiyao
ID:320180940191
email:wangziyao2018@lzu.edu.cn
date:3/19/2020
"""

import re, argparse, os
import prettytable as pt
#I add this package in the program in order to get the more beautifual consequence.
from subprocess import Popen, PIPE, DEVNULL


class Revision:
    """
    Aggregate the functions of the previous program into one class
    """
    def __init__(self, revname, revrange):
        """
        Initialize the class and define two parameters:revision name and the range
        :param revname:
        :param revrange:
        """
        self.revname = revname
        self.revrange = revrange
        self.path = 'linux-stable'

    def getcommit(self, next_rev):
        """
        gain the length of commits log from base revision to the target revision
        :param next_rev:
        :return:
        """
        tagrange = self.revname + ".." + next_rev
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tagrange
        git_rev_list = Popen(gitcnt, cwd=self.path, stdout=PIPE, stderr=DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) == 0:
            raise TagNotExistError("No such revision range: {0}..{1}, please check tag again!"
                                   .format(self.revname, self.revname + str(self.revrange)))
        return len(cnt)

    def gettagdays(self, revname):
        """
        This function will return the days between the target revision to the base
        :param revname:
        :return:
        """
        SecPerHour = 3600
        HourPerDay = 24
        gittag = "git log -1 --pretty=format:\"%ct\" " + revname
        git_tag_date = Popen(gittag, cwd=self.path, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = int(git_tag_date.communicate()[0])
        day = seconds // (SecPerHour * HourPerDay)
        return day

    def get_log(self, rev2):
        """
        return the days and commit log, return False if no revision exist.
        :param rev2:
        :return:
        """
        commit_cnt = self.getcommit(rev2)
        if commit_cnt:
            current = self.gettagdays(rev2)
            base = self.gettagdays(self.revname)
            days = current - base
            return days, commit_cnt
        else:
            return False

    def log_print(self):
        """
        Using the prettytable to print out the result in a pretty way, and load it into a file.
        :return:
        """
        tb = pt.PrettyTable()
        tb.field_names = ["version", "days", "commits"]
        for sl in range(1, self.revrange+1):
            print(".")
            rev2 = self.revname + "." + str(sl)
            days, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                tb.add_row([rev2, days, commit_cnt])
            else:
                break
        with open('result', 'a') as f:
            f.write(str(tb))
        print(tb)


class TagError(Exception):
    def __init__(self, msg):
        self.msg = msg


class TagNotExistError(TagError):
    pass


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("revision", help="please enter the version tag you want to checking")
        parser.add_argument("range", type=int, help="please enter the range of revision you want to check")
        args = parser.parse_args()
        rev_in = args.revision
        range_in = args.range
        rev = Revision(rev_in, int(range_in))
        rev.log_print()
    except TypeError:
        print('argument type wrong: The first argument should be version number, and the second argument should be an int number.')


if __name__ == "__main__":
    main()
