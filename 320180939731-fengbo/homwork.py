#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Cao Jialun All Rights Reserved
# Record all the commits starting at a git revision

__author__ = "Cao Jialun", "Feng Bo"
__sid__ = "320180939541", "320180939731"
__date__ = "3/19/2020"
__email__ = "caojl2018@lzu.edu.cn", "bfeng18@lzu.edu.cn"

import os, re, sys
from datetime import datetime as dt
from subprocess import Popen, PIPE, DEVNULL

class get_dates_commit():
    def __init__(self,rev,rev1):
        self.rev = rev
        self.rev1 = rev1
        self.repository = 'D:\git repository\linux-stable'

    def get_commit_cnt(self):
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + self.rev +".."+self.rev1
        git_rev_list = Popen(['ubuntu',gitcnt],cwd=self.repository,stdout=PIPE,stderr=DEVNULL,shell=True)
        raw_counts = git_cmd.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self):
        gittag = "git log -1 --pretty=format:\"%ct\" " + self.rev
        git_tag_date = Popen(['ubuntu',gittag],cwd=self.repository,stdout=PIPE,stderr=DEVNULL,shell=True)
        seconds = git_tag_date.communicate()[0]
        gittag1 = "git log -1 --pretty=format:\"%ct\" " + self.rev1
        git_tag_date1 = Popen(['ubuntu',gittag],cwd=self.repository,stdout=PIPE,stderr=DEVNULL,shell=True)
        seconds1 = int(git_tag_date1.communicate()[0])
        secperhour = 3600
        return (seconds1-seconds)//secperhour
    
def main():
    rev = sys.argv[1]
    rev_range = int(sys.argv[2])
    if not sys.argv[3] == "c":
        raise ValueError("The 3rd param should be 'c'.")

    for sl in range(1,rev_range+1):
        try:
            print("commits: {0}, ".format(get_dates_commit(rev,rev+"."+str(sl)).get_commit_cnt()))
        except TypeError:
            print("You have an invalid input on the 1st param")
        try:
            print("time: {0}, ".format(get_dates_commit(rev,rev+"."+str(sl)).get_tag_days()))
        except TypeError:
            print("You have an invalid input on the 2nd param")

if __name__ == "__main__":
    main()

