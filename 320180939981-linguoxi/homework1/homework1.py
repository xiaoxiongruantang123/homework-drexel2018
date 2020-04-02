#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
"""
This is a code about grab the git log and the day time about the linux_stable,from v4.1 to v4.4.
And there are three argument  eg. python homework.py -v=v4.4 -r=3 -c=True
-v The starting version you want to start counting
-r The revision number you want to query from the base version'
-c (bool)cumulative or not

and the result will be saved into test.csv as a dataframe

thanks to team 3 and my friends
"""
__author__ = "Guoxi Lin"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Guoxi Lin"]
__version__ = "3"
__maintainer__ = "Linux maintainer"
__email__ = "lingx18@lzu.edu.com"
__status__ = "Experimental"

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


import os, re, sys, subprocess
from datetime import datetime as dt
import numpy as np
import pandas as pd
import argparse

class ContentException(BaseException):
    collect = []
    def __str__(self):
        wron = 'Find nothing, please check your git and the address!'
        return wron

class Log_Collect:

    """
        python homework.py -v=v4.4 -r=3
        #sublevel commits v4.4 stable fixes
        lv hour bugs
        1 20 69
        2 37 120
        3 45 136
    """
    """get the argument"""
    def __init__(self):
        # get dates of all commits - unsorted
        self.collect = []# colect the result into list

        parser = argparse.ArgumentParser(description="parse")#argument defind
        parser.add_argument('-v', '--version', type=str,default='v4.4', help='The starting version you want to start counting')#argument defind
        parser.add_argument('-r', '--range', type=str,required=True, help='The revision number you want to query from the base version')#argument defind
        parser.add_argument('-c', '--cumulative', type=bool,default=False, help='cumulative or not')#argument defind
        args = parser.parse_args()

        self.rev = args.version
        cumulative = 0 # whether cumulative
        if (args.cumulative):
            cumulative = 1

        rev_range = int(args.range)
        self.get_base_time(self.rev)#instead of magic number v44
        self.main(cumulative, rev_range)
    """get the base time(the magic number)"""
    def get_base_time(self,v1):# instead of magic number v44
        gettime = "git log -1 --pretty=format:\"%ct\" " + v1
        get_time = subprocess.Popen(gettime, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.basetime = int(get_time.communicate()[0])

    """commit cnt here"""
    def get_commit_cnt(self, git_cmd):#change into date
        try:
           raw_counts = git_cmd.communicate()[0]
           if raw_counts == 0:
               raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(2)

           # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    """translate into date"""
    def get_tag_hour(self, git_cmd, base):#at last i choose the hour

       try:
           seconds = git_cmd.communicate()[0]
           SeePerDay = 3600
           if seconds == 0:
               raise ContentException
       except ContentException as err:
           print(err)
           sys.exit(2)

       return (int(seconds)-base)//SeePerDay# we need the day as normal

    """do what i can do"""
    def main(self, cumulative, rev_range):
        self.df = pd.DataFrame(columns=('lv','hour','bugs'))#create in dateframe
        # setup and fill in the table
        print("#sublevel commits {0} stable fixes".format(self.rev))
        #print("lv hour bugs")  # tag for R data.frame
        rev1 = self.rev
        # base time of v4.1 and v4.4 as ref base
        # fix this to extract the time of the base commit
        # from git !
        #
        # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
        # 1452466892
        # v44 = 1452466892
        for sl in range(1,rev_range+1):
            rev2 = self.rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)# grap it
            commit_cnt = self.get_commit_cnt(git_rev_list)# grap it
            if cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)# grap it
                days = self.get_tag_hour(git_tag_date, self.basetime) # grap it
                #print("{0} {1} {2}".format(sl,days,commit_cnt))
                #self.collect.append((sl,days,commit_cnt))# colect them into list
                self.df = self.df.append([{'lv': sl, 'hour': days, 'bugs': commit_cnt}],ignore_index=True)#save in dateframe

            else:
                break
        self.df = self.df.set_index('lv')

if __name__ == '__main__':
    """
        $python homework.py -v=v4.4 -r=3
        #sublevel commits v4.4 stable fixes
        lv hour bugs
        1 20 69
        2 37 120
        3 45 136
    """
    githistory = Log_Collect()
   # with open("savelog.txt", "w") as f:  # and save them into a text file
#    f.write("sl  days  commit_cnt\n")
#        for i in githistory.collect:
#            f.write(str(i))
#            f.write('\n')
    githistory.df.to_csv("Test.csv", encoding="utf-8-sig", mode="a", header=True, index=True)
    print(githistory.df)