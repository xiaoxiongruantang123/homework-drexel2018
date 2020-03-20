#! python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 LanZhou University All Rights Reserved
__author__ = "QiaoyuanYang and ShijieMa"
__studentID__ = "320180940450 and 320180940121"
__date__ = "3/21/2020"
"This is a program for finding all commits within the scope of the git version."
import os, re, sys, subprocess, argparse
import prettytable as pt


class Rev:
    def __init__(self, rev, rev_range):
        self.rev = rev
        self.rev_range = rev_range
        self.repo = 'http://commondatastorage.googleapis.com/git-repo-downloads/repo'

    def get_commit_cnt(self, rev):
        tag_range = self.rev + ".." + rev
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tag_range
        git_rev_list = subprocess.Popen(gitcnt, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                        shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) == 0:
            raise TagNotExistError("No such revision range in: {0}..{1}, please check tag again!"
                                   .format(self.rev, self.rev + str(self.revrange)))
        return len(cnt)

    def get_tag_days(self, rev):
        SecPerHour = 3600
        HourPerDay = 24
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_tag_date = subprocess.Popen(gittag, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                        shell=True)
        seconds = int(git_tag_date.communicate()[0])
        day = seconds // (SecPerHour * HourPerDay)
        return day

    def get_log(self, rev):
        commit_cnt = self.get_commit_cnt(rev)
        if commit_cnt:
            current = self.get_tag_days(rev)
            base = self.get_tag_days(self.rev)
            days = current - base
            return days, commit_cnt
        else:
            return False

    def log_print(self):
        tb = pt.PrettyTable()
        tb.field_names = ["version", "day", "commit"]
        for sl in range(1, self.revrange + 1):
            print(".")
            rev2 = self.rev + "." + str(sl)
            days, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                tb.add_row([rev2, days, commit_cnt])
            else:
                break
        with open('result', 'a') as file:
            file.write(str(tb))
        print(tb)
        print('The result has been written into the "result" file.')


try:
    rev = sys.argv[1]
    cumulative = 0
    if len(sys.argv) == 4:
        if sys.argv[3] == "c":
            cumulative = 1
        else:
            print("Don't know what you mean with %s" % sys.argv[3])
            sys.exit(-1)
    rev_range = int(sys.argv[2])
except IndexError:
    print("It's an argument type wrong: the first arg should be like'v4.1'', and the second should be an int.")

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
    print("It's an argument type wrong: the first arg should be like'v4.1'', and the second should be an int.")
