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
#
__Copyright__ = "Copyright Jiachuan_He 2020"
__Created_on__ = "2020-3-19"
__Author__ = "Jiachuan_He 320180939771"
__Version__ = "1.0.0"
__Title__ = "homework1"

import re
import sys
from subprocess import Popen, PIPE, DEVNULL


class Data:
    def __init__(self, git_cmd):
        self.git_cmd = git_cmd

    def get_commit_cnt(self):
        try:
            raw_counts = self.git_cmd.communicate()[0]
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
            return len(cnt)
        except Exception:
            print('Please check your git command!')

    def get_tag_days(self, base):
        try:
            self.base = base
            SecPerHour = 3600
            seconds = self.git_cmd.communicate()[0]
            return (int(seconds)-self.base)//SecPerHour
        except Exception:
            print('Please check your git command!')


def get_rev():
    rev = sys.argv[1]
    try:
        rev
    except IndexError:
        print("The list is out of range!")
    else:
        return rev


def get_cumulative():
    cumulative = 0
    try:
        if len(sys.argv) == 4:
            if sys.argv[3] == "c":
                cumulative = 1
            else:
                print("Dont know what you mean with %s" % sys.argv[3])
                sys.exit(-1)
    except Exception:
        print("Something wrong with sys.argv!")
    return cumulative


def base_time(base_version):
    gettime = "git log -1 --pretty=format:\"%ct\" " + base_version
    get_time = Popen(gettime, stdout=PIPE, stderr=DEVNULL, shell=True)
    return int(get_time.communicate()[0])


if __name__ == "__main__":
    print("#sublevel commits %s stable fixes" % get_rev())
    print("lv hour bugs")
    rev_range = int(sys.argv[2])
    for sl in range(1, rev_range+1):
        v44 = 1452466892
        rev1 = get_rev()
        rev2 = get_rev() + "." + str(sl)
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
        commit_cnt = Data(git_rev_list).get_commit_cnt()
        if get_cumulative() == 0:
            rev1 = rev2
        if commit_cnt:
            git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
            days = Data(git_tag_date).get_tag_days(v44)
            print("Reversion number: %d, days: %d, committed times: %d" % (sl, days, commit_cnt))
        else:
            break
