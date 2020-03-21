#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Desciription: 
    Get the commit count per sublevel pointwise or cumulative.
Fixed list:
    1.Use argparse to handle arguments.
    2.Add error handling.
    3.Transform it to a class.
    4.Add HEADER.
    5.Restructure the code, and modify the use of functions.
"""

__author__ = "Yixuan Wang, Chunyao Dong, Danni Wei, Ruyu Lin, Ziqiang Ma"
__copyright__ = "Copyright 2020, CS212, Lanzhou University"
__license__ = "GPL V2"
__version__ = "0.1"
__maintainer__ = "Yixuan Wang, Chunyao Dong, Danni Wei, Ruyu Lin, Ziqiang Ma"
__status__ = "Experimental"

import os, re, sys
from subprocess import Popen, PIPE, check_output
from datetime import datetime as dt
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='get the commit count per sublevel pointwise or cumulative')
    parser.add_argument('-bv','--baseversion', type=str, default='v4.4',
                        help='Get the initial version you want to count')
    parser.add_argument('-rn','--revisionnumber', type=str, required=True,
                        help='Get the version nuber you want to query from the initial version')
    parser.add_argument('-c','--cumulative', type=bool, default=False,
                        help='Get the answer to cumulative or not')


class GetCommitCount():
    def __init__(self, revision, baseversion='v4.4', cumulative=False):
        self.revision = revision
        self.baseversion = baseversion
        self.cumulative = cumulative
    
    def get_commit_cnt(git_cmd):
        """
        Get the counts of commit.
        """
        try:
            raw_counts,errs = git_cmd.communicate()
        except TimeoutExpired:
            git_cmd.kill()
            raw_counts, errs = git_cmd.communicate()
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)
    
    def get_base_time(self):
        """
        Get the time of each commit.
        """
        print(self.baseversion)
        time = "git log -1 --pretty=format:\"%ct\" " + self.baseversion
        get_time = Popen(time, stdout=PIPE, stderr=DEVNULL, shell=True)
        try:
            basetime, errs = get_time.communicate(timeout=15)
        except TimeoutExpired:
            get_time.kill()
            basetime, errs = get_time.communicate()
        basetime = int(basetime)
        return basetime
    
    def get_tag_days(rev, base):
        """
        Get the day of commit.
        """
        git_tag = "git log -1 --pretty=format:\"%ct\" " + rev
        get_date = Popen(git_tag, stdout=PIPE, stderr=DEVNULL, shell=True)
        try:
            seconds, errors = get_date.communicate(timeout=15)
        except TimeoutExpired:
            get_date.kill()
            seconds, errors = get_date.communicate()
        SecPerHour = 3600
        HourPerDay = 24
        return ((int(seconds)-base))// (SecPerHour * HourPerDay)
    
    def run(self):
        """
        Run the functions
        """
        rev_range = int(self.revision)
        basetime = get_base_time()
        rev = self.baseversion
        rev1 = rev
        print("#sublevel commits %s stable fixes" % rev)
        cumulative = int(self.cumulative)
        print('1')

        for sl in range(1, rev_range + 1):
            print('2')
            rev2 = rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\'%ai\' " + rev1 + "..." + rev2
            git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            commit_cnt = get_commit_cnt(git_rev_list)
            print('3')
            if cumulative == 0:
                rev1 = rev2
            if commit_cnt:
                print('4')
                days = get_tag_days(rev2, basetime)
                print("reversion number is %d ,It's been %d days since version %s ,commit %d times!" % (
                    sl, days, baseversion, commit_cnt))
            else:
                break
        print("5")

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    baseversion = args.baseversion
    revisionnumber = args.revisionnumber
    cumulative = args.cumulative
    GetCommitCount(revisionnumber,baseversion,cumulative).run()

