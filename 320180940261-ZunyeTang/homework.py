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

"""
This file is mainly for get the differences between certain revision and newest one of linux kernel.
First argument is revision of the linux kernel.
Second argument sets amount of the differences as you want.
Third argument (boolean cumulative), if it is c, third return,bugs, will accumulate result.
Results is lv,hour, bugs.

Requirement:
1. fix these bugs in the function, and some illogical syntax
2  package argparse is a better method in receiving the parameters.
3. Wrap up other code and make it more structured.
4. No error handing
5. add the header and copyright information.

"""
__author__ = "Zunye Tang,Wenyao Chen, Data Scicence, LZU University "
__copyright__ = "Copyright © 2020, Group 14, Zunye Tang"
__version__ = 0.1

import os, re, sys, subprocess
import argparse


def get_para():
    parse = argparse.ArgumentParser(description="Output the log between V and v4.4")
    parse.add_argument("-c","--cumulative",help="accumulate bugs",action="count")
    parse.add_argument("version",help="return log from given version to v4.4")
    parse.add_argument("number",type=int,help="log number")
    args, other =parse.parse_known_args()
    return args


class Output:
    def __init__(self,args):
        self.version = args.version
        self.number = args.number
        self.cumulative = args.cumulative
        self.v44 = 1452466892
        self.repo = "C:\\Users\\17301\\Desktop\\linux-stable\\"

    def get_commit_cnt(self,git_cmd):
        raw_counts = git_cmd.communicate()[0]
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self,git_cmd, base):
        seconds = git_cmd.communicate()[0]
        return (int(seconds)-base)//3600

    def cumulative_change(self):
        if self.cumulative == 1:
            self.cumulative = 1
        elif self.cumulative == None:
            self.cumulative = 0
        else:
            print("Don't know what you mean with %s" % self.cumulative)
            raise SyntaxError

    def run(self):
        rev1 = self.version
        self.cumulative_change()
        for sl in range(1, self.number + 1):
            rev2 = self.version + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                            shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if self.cumulative == 0:
                rev1 = rev2
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                                shell=True)
                days = self.get_tag_days(git_tag_date, self.v44)
                print("%d %d %d" % (sl, days, commit_cnt))
            else:
                break


if __name__ == "__main__":
    args = get_para()
    print("#sublevel commits %s stable fixes" % args.version)
    print("lv hour bugs")
    Output(args).run()
