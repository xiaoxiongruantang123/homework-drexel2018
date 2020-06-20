#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Run the git command automatically.
__author__ = " Zhai Zhaoyuan, ID:320180939661 "
__copyright__ = "Zhai Zhaoyuan, Group 03, Lanzhou University, 2020"
__license__ = "GPL V2 or later"
__version__ = "0.1"
__maintainer__ = "Zhai Zhaoyuan"
__email__ = "zhaizhy18@lzu.edu.cn"
'''

import os, re, sys, time, argparse
from subprocess import Popen, PIPE, DEVNULL, TimeoutExpired

class Get_Commit():
    def __init__(self):
        parser = argparse.ArgumentParser(description="Manage integers and strings")
        parser.add_argument('rev', help='the beginning version,for example v4.4')
        parser.add_argument('rev_range', help='the ending number of sublevel version,for example v4.4.x，x = rev_range',type=int)
        parser.add_argument('cumu', help='switch for whether running git command cumulatively',type=str,default = 'c')
        args = parser.parse_args()
        self.rev = args.rev
        rev_range = int(args.rev_range)
        self.cumu = args.cumu
        
        cumulative = 0
        try:
            len(sys.argv) == 4
        except ValueError:
            print('Please input the correct number of parameters')
        if (self.cumu == "c"):
            cumulative = 1
        else:
            print("Dont know what you mean with %s" % self.cumu)
            sys.exit(-1)
        print("#sublevel commits %s stable fixes" % self.rev)
        print("lv hour bugs")
        self.count_commit_date(cumulative,rev_range) 
    def get_commit_cnt(self,git_cmd):
        '''Find the length of output,produced by git command, which fits the requirement of regular expression
        
        This function is called by the funtion of count_commmit. The argument is about
        git command that inputted.
        '''
        try:
            time_begin = time.time()
            raw_counts = git_cmd.communicate()[0]
            # if we request something that does not exist -> 0
            time_end = time.time()
            time_end-time_begin > 20
        except:
            git_cmd.kill()
            raise TimeoutExpired
        cnt = 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)
    
    def get_tag_days(self,git_cmd, base):
        '''Create a pipe for subflow and get date of commits.
        
        This function is called by the funtion of count_commmit. Two arguments are 
        about git command and base time of certain commit.
        '''
        try:
            time_begin = time.time()
            seconds = git_cmd.communicate()[0]
            time_end = time.time()
            time_end-time_begin > 20
        except:
            git_cmd.kill()
            raise TimeoutExpired
        SecPerHour = 3600
        return (int(seconds)-base)//SecPerHour
          
    def count_commit_date(self,cumulative,rev_range):
        '''Run git command automatically.
        
        The args.cumu refer to a statement for whether running git command cumulatively 
        or running without any output.If running git command cumulatively,the output is 
        about author date and committer date for a certain range of version.
        '''
        rev1 = self.rev
        v44 = 1452466892
        for sl in range(1,rev_range+1):
            rev2 = self.rev + "." + str(sl)
            tag_range = rev1 + "..." + rev2
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + tag_range
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if cumulative == 0:
                rev1 = rev2
            if commit_cnt:
                git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
                days = self.get_tag_days(git_tag_date, v44)
                result = "%d %d %d" % (sl,days,commit_cnt)
                print(result)
            else:
                break
            
            
if __name__ == '__main__':
    a = Get_Commit()
