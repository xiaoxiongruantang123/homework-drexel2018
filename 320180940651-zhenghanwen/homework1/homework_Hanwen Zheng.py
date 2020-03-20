#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The code is written by my professor Mr. Hofrat and improved by Hanwen Zheng on 3/19/2020.
# And it is written to record the log and its time.

import os,re,sys
from subprocess import Popen
from datetime import datetime as dt

class record():
    # Define the commit record

    def __init__(self, gittag, gitcnt, base_t):
        self.gittag = gittag
        self.gitcnt = gitcnt
        self.base_t = base_t

    # Key arguments: gittag - the git command log;
    # gitcnt - the git command rev_list; base_t - the base time of the version

    def get_tag_days(self, base_t, gittag):
        try:
            git_tag_date = subprocess.Popen(self.gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        except:
            print("There is something wrong: ")
        else:
            seconds = git_tag_date.communicate()[0]
            hour_s = 3600
            return ((int(seconds)-self.base_t))//hour_s

    def get_cnt(self, gitcnt):
        try:
            git_rev_list = subprocess.Popen(self.gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        except:
            print("There is something wrong: ")
        else:
            cnt = 0
            raw_counts = git_rev_list.communicate()[0]
            # if we request something that does not exist -> 0
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
            return len(cnt)


# get dates of all commits - unsorted 
rev = sys.argv[1]
cumulative = 0
if len(sys.argv) == 4:
    if (sys.argv[3] == "c"):
        cumulative = 1
if not cumulative == 1:
    print("There is something wrong with your input.")
    sys.exit(-1)
rev_range = int(sys.argv[2])

# setup and fill in the table
print("#sublevel commits %s stable fixes" % rev)
print("lv hour bugs") #tag for R data.frame
rev1 = rev
# base time of v4.1 and v4.4 as ref base
# fix this to extract the time of the base commit
# from git !
# 
# hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
# 1452466892

version = "v4.4"
git_com = "git log -1 --pretty=format:'{ver}'".format(ver='version')
base_time = int(os.Popen(git_com,"r").read())

for s1 in range(1,rev_range+1):
    rev2 = rev + "." + str(s1)
    gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
    gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
    commit_ct = record.get_cnt(gitcnt)
    if cumulative == 0:
        rev1 = rev2
    # if get back 0 then its an invalid revision number
    if commit_ct:
        days = record.get_tag_days(gittag, case_time)
        print("%d %d %d" % (s1, days, commit_ct))
    else:
        break
