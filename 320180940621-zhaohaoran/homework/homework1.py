#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
"""
This is a tool to grab the git log information.
You can use this tool by calling it in command line with three parameters, e.g. $python homework.py -v=4.4 -r=3 -c=c
These three parameters
-v / --version : Which version of git do we need
-r / --range : The range of revision
-c / --cumulative : Whether we need cumulative one.
"""

__author__ = "Nicholas Mc Guire, Haoran Zhao"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Haoran Zhao"]
__version__ = "3"
__maintainer__ = "Linux maintainer"
__email__ = "zhaohr18@lzu.edu.com"
__status__ = "Experimental"

import os
import re
import sys
import argparse
from datetime import datetime as dt
from subprocess import Popen, PIPE, DEVNULL
import pandas as pd

class GitException(BaseException):
    def __str__(self):
        err = 'Find nothing, please check if you are in the right git'
        return err


class Git_Log:
    def __init__(self):
        '''
        Using argparse to get the information of which version of git do we need, how many sublevels
        we need, and whether we need a cumulative one?
        Also get the information like basetime.
        '''
        self.collect = []
        
        parser = argparse.ArgumentParser(description="parse")
        parser.add_argument('-v', '--version', default='V4.4', required=True, help='The starting version')
        parser.add_argument('-r', '--range', default=2, required=True, help='The revision number')
        parser.add_argument('-c', '--cumulative', default="c", help='Cumulative or not')
        args = parser.parse_args()

        self.rev = args.version
        if args.cumulative == "c":
            cumulative = 1
        else:
            print("Dont know what you mean with {0}".format(args.cumulative))
            cumulative = 0
            sys.exit(1)
        rev_range = int(args.range)
        self.get_base_time(self.rev)
        self.git(cumulative, rev_range)
        
    def get_base_time(self,v1):
        """
        This is a function used to get the basetime.
        """
        gettime = "git log -1 --pretty=format:\"%ct\" " + v1
        get_time = Popen(gettime, stdout=PIPE, stderr=DEVNULL, shell=True)
        self.basetime = int(get_time.communicate()[0])

    def get_commit_cnt(self, git_cmd):
        """
        This is a function used to count how many commits are here.
        """
        try:
            raw_counts = git_cmd.communicate()[0]
            if raw_counts == 0:
                raise GitException
        except GitException as err:
            print(err)
            sys.exit(2)

        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_hours(self, git_cmd, base):
        """
        This is a function used to git the hours from the commit.
        """
        try:
            seconds = git_cmd.communicate()[0]
            if seconds == 0:
                raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(2)
        return (int(seconds) - base) // (3600 )  # we need the day as normal

    def git(self, cumulative, rev_range):
        """
        This is the main function to grab the git log and find out what we need.
        """
        self.df = pd.DataFrame(columns=('lv','hour','bugs'))
        print("#sublevel commits {0} stable fixes".format(self.rev))
        rev1 = self.rev

        for sl in range(1, rev_range + 1):
            rev2 = self.rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
                days = self.get_tag_hours(git_tag_date, self.basetime)
                self.df = self.df.append([{'lv': sl, 'hour': days, 'bugs': commit_cnt}],ignore_index=True)            
            else:
                break
        self.df = self.df.set_index('lv')
        self.df.to_csv("Test.csv", encoding="utf-8-sig", mode="a", header=True, index=True)


if __name__ == '__main__':
    collect = Git_Log()