#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
__author__ = Yiqi Huang
__coptright__ = Copyright 2020, Yiqi Huang
__license__ = GPL
__version__ = 0.2
__maintainer__ = Yiqi Huang
__email__ = "huangyq2018@lzu.edu.cn"
__status__ = Done

"""

#Get the count of the commit in each sublevel by the tag
#The amount of tags means the number of patches
#We can count the number of patches to find how many issues were fixed
#When the count out of range, the loop will be terminated.
import os, re, sys, argparse, doctest
from subprocess import Popen,PIPE,DEVNULL

class Count_Commit:

    #We can use method get_argparse to control and 
    #limit the argument in the commandline. 
    #You can run the file in the terminal by 
    #"python3 homework.py -version v4.4 -rangenum 216"      
    def get_argparse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-version", required=True)
        parser.add_argument("-rangenum", required=True, type=int)
        parser.add_argument("-cumulative", default=0, type=bool,
           help="To calculate the sum of commit_cnt or  not, 0 would not calculate and others will calculate. The default value is 0.")
        return parser


    #The method get_git_cmd combines the git code with Popen 
    #and the command is used as the argument of other functions.
    def get_git_cmd(self,rev1,rev2):
        self.rev1 = rev1
        self.rev2 = rev2
        tag_range = rev1 + "..." + rev2
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tag_range
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
        git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
        return git_rev_list, git_tag_date


    #The method get_commit_cnt search the commit in the kernel
    #and return the length of all counts.
    def get_commit_cnt(self,git_cmd):
        self.git_cmd = git_cmd
        raw_counts = git_cmd.communicate()[0]
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)


    #The get_base method finds the latest commit time stamp.
    #using "git log -1 --pretty=format:%ct v4.4" 
    def get_base(self,rev):
        self.rev = rev
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_base_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
        base = git_base_date.communicate()[0]
        return base


    #Find the latest time of commit of different sublevels.
    #Convert the seconds into days.
    def get_tag_days(self, git_cmd, base):
        self.git_cmd = git_cmd
        self.base = base
        try:
            seconds = git_cmd.communicate()[0]
            SecPerDay = 3600*24
            return ((int(seconds)-base)//SecPerDay)
        except ValueError:
            print("The seconds cannot be converted into integer.")


    def main(self, rev, rev_range):
        self.rev = rev
        self.rev_range = rev_range
        rev1 = rev
        print("lv hour bugs") #tag for R data.frame
        try:
            for sl in range(1,rev_range+1):
                rev2 = rev + "." + str(sl)
                git_rev_list, git_tag_date = count.get_git_cmd(rev1,rev2)
                commit_cnt = count.get_commit_cnt(git_rev_list)
                if cumulative == 0:
                    rev1 = rev2
                # if get back 0 then its an invalid revision number
                if commit_cnt:
                    base = int(count.get_base(rev))
                    try:
                        stamp_days = count.get_tag_days(git_tag_date, base)
                    except TypeError:
                        print("The return value of git_tag_days is None.")
                        break
                    print("%d %d %d" % (sl,stamp_days,commit_cnt))
                else:
                    break
        except IndexError:
            print("Invalid rev_range")
            sys.exit(-1)


if __name__ == "__main__":
    count = Count_Commit()
    parser = count.get_argparse()
    args = parser.parse_args()
    rev = args.version
    rev_range = args.rangenum
    cumulative = args.cumulative
    count.main(rev,rev_range)
    print("#sublevel commits %s stable fixes" % rev)
