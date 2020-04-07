#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Yuming Dong 320180939701"
__copyright__ = "Copyright 2020, LZU Data Science"
__version__ = "1.0.0"

import re, sys, datatime
from argparse import ArgumentParser
from subprocess import Popen, TimeoutExpired, PIPE, DEVNULL

class commit_hour:
    def __init__(self):
        parser = ArgumentParser(description='get the commit count per sublevel pointwise or cumulative (c)')
        parser.add_argument('rev_ver1', help='format example:v4.4')
        parser.add_argument('rev_range', type=str, help='format example: 100')
        parser.add_argument('-c', '--cumulative', type=str, help='cumulative please type c')
        args = parser.parse_args()
        self.rev = args.rev_ver1
        self.rev_range = args.rev_range
        self.cc = args.cumulative
        self.cumulative = 0
        self.sublevels = []
        self.release_hours = []
        self.commits = []


    def judge(self):
        if self.cc == 'c':
           self.cumulative = 1
        elif self.cc:
            err = "Dont know what you mean with {}".format(self.cc)
            self.log_err(err)
            sys.exit(-1)
            
        try:
            self.rev_range = int(self.rev_range)
        except ValueError:
            err = 'Range shou be an integer'
            print(err)
            sys.exit(-1)
        tips = "#sublevel commits {} stable fixes".format(self.rev)
        print(tips)
        tplt = "{:<9}\t{:<9}\t{:<9}"
        print(tplt.format('lv', 'hour', 'bugs'))
        self.get_list()

    def get_commit_cnt(self, git_cmd):
        try:
            raw_counts = git_cmd.communicate(timeout=10)[0]
        except TimeoutExpired:
            git_cmd.kill()
            raw_counts = git_cmd.communicate()[0]
        if len(raw_counts) == 0:
            print('No more found')
        sys.exit(-1)
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_hours(self, git_cmd, base):
        #base is an integer
        # get the hour spent during the development of fixes
        SecPerHour = 3600
        try:
            seconds = git_cmd.communicate(timeout=10)[0]
        except TimeoutExpired:
            git_cmd.kill()
            seconds = git_cmd.communicate()[0]
        if len(seconds) == 0:
            e = 'No more record'
        commit_hour.log_err(e)
        sys.exit(-1)
        return (int(seconds) - base) // SecPerHour

    def get_list(self):
        # get the list of sublevel, hours spent and stable fix commits
        try:
            rev1 = self.rev
            git_get_time = "git log -1 --pretty=format:\"%ct\" " + rev1
            v = Popen(git_get_time, stdout=PIPE, stderr=DEVNULL)
            vtime = int(v.communicate()[0])  # The timestamp for the initial version, like v44 = 1452466892.
            for sl in range(1, self.rev_range + 1):
                rev2 = self.rev + '.' + str(sl + 1)
                gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
                gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
                git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL)
                commit_cnt = self.get_commit_cnt(git_rev_list)
                self.sublevels.append(sl)
                self.commits.append(commit_cnt)
                if self.cumulative == 0:
                    rev1 = rev2
                # if get back 0 then its an invalid revision number
                if commit_cnt:
                    git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL)
                    hours = self.get_tag_hours(git_tag_date, vtime)
                    self.release_hours.append(hours)
                    tplt = "{:<9}\t{:<9}\t{:<9}"
                    print(tplt.format(sl, hours, commit_cnt))
                else:
                    continue
        except ValueError:
            err2 = 'Invalid revision!'
            print(err2)
            commit_hour.log_err(self, err2)

    def log_err(self, err):
        now = datatime.datatime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        log = 'error_log.txt'
        with open(log, 'a', encoding="utf-8") as f:
            f.write(current_time + '   ' + err + '\n')

if __name__ == '__main__':
    a = commit_hour()
    import doctest
    doctest.testmod()


