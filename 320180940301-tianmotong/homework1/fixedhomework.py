#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 TianMotong, lzu All Rights Reserved
"""
Simple program to find all commits of a range starting at a git revision.

"""

__author__ = "TianMotong"
__address__ = 'Lanzhou University'
__studentID__ = "320180940301"
__date__ = "3/19/2020"
__email__ = "tianmt18@lzu.edu.cn"

import os, re, sys, subprocess
from datetime import datetime as dt

class TagError(Exception):
    def __init__(self, msg):
        self.msg = msg

class TagNotExist(TagError):
    pass

class Rev:
    def __init__(self,git_cmd,base,v):
        self.git_cmd = git_cmd
        self.base = base
        self.v = v


    def get_tag_days(self):
       seconds = self.git_cmd.communicate()[0]
       return ((int(seconds)-self.base))//3600

    def obtain_revrange(self):
        # get dates of all commits - unsorted
        rev = sys.argv[1]
        self.cumulative = 0
        if len(sys.argv) == 4:
            if (sys.argv[3] == "c"):
                self.cumulative = 1
            else:
                print("Dont know what you mean with %s" % sys.argv[3])
                sys.exit(-1)
        self.revrange = int(sys.argv[2])
        self.rev = rev

    def get_commit_cnt(self):
       cnt = 0
       raw_counts = self.git_cmd.communicate()[0]
       # if we request something that does not exist -> 0
       cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
       if len(cnt) == 0:
           raise TagNotExist("No such revision range: {0}...{1}, please check again!"
                                  .format(self.rev, self.rev + str(self.revrange)))
       return len(cnt)


    def fill_table(self):
        # setup and fill in the table
        print("#sublevel commits %s stable fixes" % self.rev)
        print("lv hour bugs") #tag for R data.frame
        self.rev1 = self.rev

    def final(self):
        for sl in range(1,self.revrange+1):
            self.rev2 = self.rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + self.rev1 + "..." + self.rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + self.rev2
            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            commit_cnt = get_commit_cnt(git_rev_list)
            if self.cumulative == 0:
                self.rev1 = self.rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                days = get_tag_days(git_tag_date, self.v)
                print("%d %d %d" % (sl,days,commit_cnt))
            else:
                break
