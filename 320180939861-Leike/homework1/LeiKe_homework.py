#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#copyright(c) 2020 LeiKe, lzu ALL Rights Reserved
"""
Simple program on counting git commits in a specific git revision. 
Educational purpose only, do not use for other purpose please!
"""

"""work with ShenJiachen, ID:320180940191"""
__author__ = "LeiKe"
__address__ = 'Lanzhou University
__studnetID__ = "320180939861"
__date__ = "3/20/2020"
__email__ = "leik18@lzu.edu.cn"



import os, re, sys
from subprocess import Popen
from datetime import datetime as dt


class get_git_commit(): 
    def __init__(self, rev, revrange):
        self.rev = rev
        self.revrange = revrange
        self.repo = 'root/linux_kernel/linux_stable'
        
        
    def get_commit_cnt(self, git_cmd):
    '''this function is used to get commit communication's raw counts.'''
       cnt = 0
       raw_counts = git_cmd.communicate()[0]
       # if we request something that does not exist -> 0
       cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
       return len(cnt)

    
    def get_tag_days(self, git_cmd, base):
    '''This function is used to get seconds of getting a tag per hour.'''
       seconds = git_cmd.communicate()[0]
       return ((int(seconds)-base))//SecondPerHour


    def get_log(self, rev2):
        """
        return the days and commit log, return False if no revision exist.
        :param rev2:
        :return:
        """
        commit_cnt = self.get_commit_cnt(rev2)
        if commit_cnt:
            current = self.get_tag_days(rev2)
            base = self.get_tag_days(self.rev)
            days = current - base
            return days, commit_cnt
        else:
            return False

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("revision", help="the version tag you want to start checking, example: v4.1")
        parser.add_argument("range", type=int, help="the range of revision you want to check")
        args = parser.parse_args()
        rev_in = args.revision
        range_in = args.range
        rev = Rev(rev_in, int(range_in))
        rev.log_print()
    except TypeError:
        print('argument type wrong: the first arg should be like"v4.1", and the second should be an int.')


if __name__ == "__main__":
    main()
