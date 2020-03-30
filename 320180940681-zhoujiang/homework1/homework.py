#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Jiang Zhou, Lanzhou University, All Rights Reserved

__author__ = "Jiang Zhou"
__studentID__ = "320180940681"
__date__ = "3/27/2020"
__email__ = "zhoujiang18@lzu.edu.cn"

import os, re, sys, subprocess
os.system("pip install prettytable")
import prettytable as pt
from subprocess import Popen, PIPE, DEVNULL

class exception(BaseException):
    def __str__(self):
        err = 'Please check the right git!'
        return err

class time_result:

    def __init__(self, rev, revrange):

        self.rev = rev
        self.revrange = revrange
        self.repository = 'D:\git repositorysitory\linux-stable'


    def get_commit_cnt(self, next_rev):

        tag_range = self.rev + ".." + next_rev
        git_cnt = "git rev-list --pretty=format:\"%ai\" " + tag_range
        git_rev_list = Popen(git_cnt, cwd=self.repository, stdout=PIPE, stderr=DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, rev):

        sec_per_hour = 3600
        hour_per_day = 24
        git_tag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_tag_date = Popen(git_tag, cwd=self.repository, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = int(git_tag_date.communicate()[0])
        every_day = seconds // (sec_per_hour * hour_per_day)
        return every_day

    def get_log(self, rev2):

        commit_cnt = self.get_commit_cnt(rev2)
        if commit_cnt:
            current = self.get_tag_days(rev2)
            base = self.get_tag_days(self.rev)
            days = current - base
            return days, commit_cnt
        else:
            return False

    def log_result(self):

        tb = pt.PrettyTable()
        tb.field_names = ["version", "days", "commits"]
        for sl in range(1, self.revrange+1):
            rev2 = self.rev + "." + str(sl)
            days, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                tb.add_row([rev2, days, commit_cnt])
            else:
                break
        with open('result', 'a') as f:
            f.write(str(tb))

        print(tb)
        print('The result was written to the file')

if __name__ == "__main__":
    result = time_result(sys, subprocess)