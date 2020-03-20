#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# get the commit count per sublevel pointwise or cumulative (c)
# arguments is the tag as displayed by git tag and the number
# of sublevels to be counted. If count is out of range for a 
# specific sublevel it will terminate the loop
#
# no proper header in this file 
# no legal/copyright ...OMG !
# 
# things to cleanup:
# restructure the code - use of functions 
# error handling ...where is the try..except ?
# argument handling: you can do better right ?
# documentation: once you understand it - fix the docs !
# transform it into a class rather than just functions !

# setup and fill in the table
# base time of v4.1 and v4.4 as ref base
# fix this to extract the time of the base commit
# from git !
#
# hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
# 1452466892
__copyright__ = "Jiyang Xin "

import os, re, sys
from subprocess import Popen, PIPE, DEVNULL
    
class GitLearn():

    def __init__(self,git_cmd,rev,get_commit_cnt,get_tag_days):
        self.__git_cmd=git_cmd
        self.__rev=rev
        self.__get_commit_cnt=get_commit_cnt
        self.__get_tag_days=get_tag_days

    def get_commit_cnt(git_cmd):
        cnt = 0
        try:
            raw_counts = git_cmd.communicate()[0]
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        except TypeError as cnt:
            print("TypeError")
        finally:
            return len(cnt)

    def get_tag_days(git_cmd, base):
        SecPerHour = 3600
        try:
            seconds = git_cmd.communicate()[0]
        except TypeError as seconds:
            print("TypeError")
        finally:
            return ((int(seconds)-base))//SecPerHour

    def get_all_commit(rev):
        try:
            rev = sys.argv[1]
            rev.cumulative = 0
            if len(sys.argv) == 4:
                if (sys.argv[3] == "c"):
                    rev.cumulative = 1
                else:
                    print("Dont know what you mean with %s" % sys.argv[3])
                    sys.exit(-1)
            rev.range = int(sys.argv[2])
            rev.one = rev
        except TypeError as rev:
            print("TypeError")
        finally:
            print("#sublevel commits %s stable fixes" % rev)
            print("lv hour bugs")


    def get_cumulate(rev,get_commit_cnt,get_tag_days):
        v44 = 1452466892
        try:
            for sl in range(1,rev.range+1):
                rev2 = rev + "." + str(sl)
                gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
                gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
                git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
                commit_cnt = get_commit_cnt(git_rev_list)
                if rev.cumulative == 0:
                    rev1 = rev2
                if commit_cnt:
                    git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
                    days = get_tag_days(git_tag_date, v44)
                else:
                    break
        except TypeError as sl:
                print("TypeError")
        except TypeError as days:
                print("TypeError")
        except TypeError as commit_cnt:
                print("TypeError")
        finally:
                print("%d %d %d" % (sl,days,commit_cnt))

