#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""homework1.py: Count the number of uploads of each sub-level in
a project and the time they were uploaded. Submissions represents the
number of times, and time represents time.."""

__author__      = "Xiangwen Qiao，Wenyao Chen, class4, Data science, Lanzhou university"
__copyright__   = "Copyright 2020, Project of Data science in python"
__version__ = "0.1"

import os, re, sys, subprocess,argparse


parser = argparse.ArgumentParser(description='Output the log of linux-stable')
parser.add_argument('-n','--cumulative',help='accumulate bugs',action='count')
parser.add_argument('version',help="return log of version4.4")
parser.add_argument('number',type=int,help='log number')
args = parser.parse_args()


class Count:
    version = args.version
    number = args.number
    cumulative = args.cumulative
    v44 = 1452466892
    repo = "C:\\Users\\乔向文\\AppData\\Local\\Packages\\CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc\\LocalState"

    def get_commit_cnt(self,git_cmd):
       cnt = 0
       raw_counts = self.git_cmd.communicate()[0]
       cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
       return len(cnt)

    def get_tag_days(self,git_cmd, base):
       seconds = self.git_cmd.communicate()[0]
       return ((int(seconds)-base))//3600


    def Cumulative_statistics(self):
        if self.accum == 1:
           self.accum == 1
        elif self.accum == None:
            self.accum == 0
        else:
            print("Don't know what you mean with %s" % self.cumulative)
            raise SyntaxError

    def start(self,git_cmd):
        rev1 = version
        self.Cumulative_statistics()
        for sl in range(1,number+1):
            rev2 = self.version + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if self.accum == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                days = get_tag_days(git_tag_date, self.v44)
                print("%d %d %d" % (sl,days,commit_cnt))
            else:
                break

if __name__ == "__main__":
    print("#sublevel commits %s stable fixes" % args.version)
    print("level time Submissions")
    Count()