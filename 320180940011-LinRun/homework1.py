#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Group04"
__copyright__ = "Copyright 2020, Lanzhou University"
__credits__ = ["Group04"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "LinRun"
__email__ = "linr18@lzu.edu.cn"
__status__ = "Production"

import os, sys, re
import argparse
from subprocess import Popen, PIPE, DEVNULL


class ContentException(BaseException):
    def __str__(self):
        exp_info = "Find nothing, please check your git and the address!"
        return exp_info


def get_parser():
    parser = argparse.ArgumentParser(
        description="get the commit count per sublevel pointwise or cumulative")
    parser.add_argument("-bv", "--baseversion", type=str, default="v4.4")
    parser.add_argument("-rn", "--revisionnumber", type=str, required="Ture",
                        help="The version number you want to query from the base version")
    parser.add_argument("-c", "--cumulative", type=bool, default="Fause",
                        help="cumulative or not")
    return parser


class CommitCount:
    def __init__(self, revision, baseversion="v4.4", cumulative=False):
        self.baseversion = baseversion
        self.revision = revision
        self.cumulative = cumulative
        self.get_base_time()

    @staticmethod
    def get_commit_cnt(git_cmd):
        try:
            raw_cnt = git_cmd.communicate()[0]
            if len(raw_cnt) == 0:
                raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(1)
        cnt = re.findall("[0-9]*-[0-9]*-[0-9]*", str(raw_cnt))
        return len(cnt)

    def get_base_time(self):
        print(self.baseversion)
        git_time = "git log -1 --pretty=format:\"%ct\" " + self.baseversion
        get_time = Popen(git_time, stdout=PIPE, stderr=DEVNULL, shell=True)
        try:
            basetime = get_time.communicate()[0].decode("utf-8").replace("'", "")
            if len(basetime) == 0:
                raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(1)
        self.basetime = int(basetime)
        print(self.basetime)

    @staticmethod
    def get_tag_days(rev, base):
        s_per_h = 3600
        h_per_day = 24
        git_tag = "git log -1 --pretty=format:\'%ct\' " + rev
        get_tag_date = Popen(git_tag, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = get_tag_date.communicate()[0].decode("utf-8").replace("'", "")
        return (int(seconds) - base) // (s_per_h * h_per_day)

    def main(self):
        rev_range = int(self.revision)
        basetime = self.basetime
        rev = self.baseversion
        rev1 = rev
        print("#sublevel commits %s stable fixes" % rev)
        cumulative = int(self.cumulative)

        for sl in range(1, rev_range + 1):
            rev2 = rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\'%ai\' " + rev1 + "..." + rev2
            git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if cumulative == 0:
                rev1 = rev2
            if commit_cnt:
                days = self.get_tag_days(rev2, basetime)
                print("reversion number is %d ,It's been %d days since version %s ,commit %d times!" % (
                sl, days, baseversion, commit_cnt))
            else:
                break


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    baseversion = args.baseversion
    revisionnumber = args.revisionnumber
    cumulative = args.cumulative
    CommitCount(revisionnumber, baseversion, cumulative).main()