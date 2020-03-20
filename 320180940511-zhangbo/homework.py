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


import os,sys, subprocess 
from datetime import datetime as dt
from re import findall as findall 
    

class git_collect:
    
    def __init__(self, argv=[]):
        try:
            if argv[4]:
                pass
        except IndexError:
            print(' at least 4 arguments')
            sys.exit(1)

        self.rev = argv[1]
        cumulative = 0
        if len(argv) == 4:
            if (argv[3] == "c"):
                cumulative = 1
            else:
                print("Do not know the mean with %s" % argv[3])
                sys.exit(-1)
        rev_range = int(argv[2])
        self.git(cumulative, rev_range)
        
    def get_commit_cnt(git_cmd):
       cnt = 0
       raw_counts = git_cmd.communicate()[0]
       # if we request something that does not exist -> 0
       cnt = findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
       return len(cnt)
    
    def get_tag_days(git_cmd, base):
       seconds = git_cmd.communicate()[0]
       return ((int(seconds)-base))//3600
    
    def git(self, cumulative, rev_range):
        v44 = 1452466892

        for sl in range(1,rev_range+1):
            rev2 = rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            commit_cnt = get_commit_cnt(git_rev_list)
        if cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                days = get_tag_days(git_tag_date, v44)
                print("%d %d %d" % (sl,days,commit_cnt))
            else:
                break
    
    

if __name__ == '__main__':
    collecter = git_collect(sys.argv)   
