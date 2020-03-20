#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# get the commit count per sublevel pointwise or cumulative (c)
# arguments is the tag as displayed by git tag and the number
# of sublevels to be counted. If count is out of range for a
# specific sublevel it will terminate the loop

__author__ = "Kang Yunhao,id320180939851"
__copyright__ = "Copyright 2020, LZU DS"
__version__ = "1.1"
__license__ = "GPL"
__email__ = "kangyh18@lzu.edu.cn"

import os,re,sys
from subprocess import Popen,PIPE,DEVNULL
from datetime import datetime as dt

#transform it into a class
class counter():
    def __init__(self,git_cmd,base):
        self.git_cmd=git_cmd
        self.base=base

    def get_commit_cnt(self):
        cnt = 0
		#add some try..except
        try:
            raw_counts = self.git_cmd.communicate()[0]
            # if we request something that does not exist -> 0
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
            return len(cnt)
        except Exception:
            print('Error!Check your command and do it again.')

    def get_tag_days(self):
        try:
            seconds = self.git_cmd.communicate()[0]
            return ((int(seconds) - self.base)) // 3600
        except Exception:
            print('Error!Check your command and do it again.')

    # get dates of all commits - unsorted
    rev = sys.argv[1]
    cumulative = 0
    if len(sys.argv) == 4:
        if (sys.argv[3] == "c"):
            cumulative = 1
        else:
            print("Dont know what you mean with %s" % sys.argv[3])
            sys.exit(-1)
    rev_range = int(sys.argv[2])

    rev = sys.argv[1]

    # setup and fill in the table
    print("#sublevel commits %s stable fixes" % sys.argv[1])
    print("lv hour bugs") #tag for R data.frame
    rev1 = rev

    # base time of v4.1 and v4.4 as ref base
    # fix this to extract the time of the base commit
    # from git !
    # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
    # 1452466892

    v44 = 1452466892
    for sl in range(1, rev_range + 1):
        rev2 = rev + "." + str(sl)
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
        commit_cnt = get_commit_cnt(git_rev_list)
        if cumulative == 0:
            rev1 = rev2
        # if get back 0 then its an invalid revision number
        if commit_cnt:
            git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
            days = get_tag_days(git_tag_date, v44)
            print("%d %d %d" % (sl, days, commit_cnt))
        else:
            break

if __name__ == '__main__':
    c = counter()
    c.get_commit_cnt()
    c.get_tag_days()














