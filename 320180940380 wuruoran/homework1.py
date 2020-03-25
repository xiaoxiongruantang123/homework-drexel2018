#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Bian Peijia, Cai Qiqi, Wu Ruoran, Jiang Yiyue All Rights Reserved

__author__ = "Bian Peijia, Cai Qiqi, Wu Ruoran, Jiang Yiyue"
__sid__ = "320180939520, 320180939530,320180940380,320180939820"
__date__ = "3/19/2020"
__email__ = "bianpj18@lzu.edu.cn, caiqq18@lzu.edu.cn, wurr18@lzu.edu.cn, jiangyy18@lzu.edu.cn"

import os, re, sys
from datetime import datetime as dt
from subprocess import Popen, PIPE, DEVNULL

class Get_commit_count:
    def __init__(self, gitcnt, gittag):
        self.gitcnt = gitcnt
        self.gittag = gittag
        
    
    def get_commit_cnt(self, git_cmd):
        cnt = 0
        raw_counts = git_cmd.communicate()[0]# if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, git_cmd, base):
        t = 3600
        seconds = git_cmd.communicate()[0]
        return ((int(seconds)-base))//t

    def get_unsorted_all_commits_dates(self):

        
        rev = sys.argv[1]
        cumulative = 0
        if len(sys.argv) == 4:
            if (sys.argv[3] == "c"):
                cumulative = 1
            else:
                print("Dont know what you mean with %s" % sys.argv[3])
                sys.exit(-1)
        rev_range = int(sys.argv[2])

        print("#sublevel commits %s stable fixes" % rev)
        print("lv hour bugs") #tag for R data.frame
        rev1 = rev

        v44 = 1452466892
        try:
            for sl in range(1,rev_range+1):
                rev2 = rev + "." + str(sl)
                gitcnt = self.gitcnt + rev1 + "..." + rev2
                gittag = self.gittag + rev2
                git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
                commit_cnt = self.get_commit_cnt(git_rev_list)
                if cumulative == 0:
                    rev1 = rev2
                # if get back 0 then its an invalid revision number
                if commit_cnt:
                    git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
                    days = self.get_tag_days(git_tag_date, v44)
                    print("%d %d %d" % (sl,days,commit_cnt))
                    
                else:
                    print('Its an invalid revision number')
                    break
        except:
            raise ValueError('something wrong.')
if __name__ == '__main__':
    gitcnt = "git rev-list --pretty=format:\"%ai\" " 
    gittag = "git log -1 --pretty=format:\"%ct\" " 
    get = Get_commit_count(gitcnt, gittag)
    get.get_unsorted_all_commits_dates()
