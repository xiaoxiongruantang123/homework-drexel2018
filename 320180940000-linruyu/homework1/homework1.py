#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This py can find the commits and days of which version of a git.
The arguments must be the version like 'v4.1', and the versions number must be an int.
The address is the git address in the computer.
'''

__author__ = "Dongchunyao, Linruyu, Weidanni, Wangyixuan, Maziqiang"
__studentID__ = "320180939690，320180940000，320180940370, 320180940330 "
__email__ = "dongchy18@lzu.edu.cn, linry18@lzu.edu.cn, weidn18@lzu.edu.cn, wangyixuan2018@lzu.edu.cn，mazq18@lzu.edu.cn"
__version__ = "v1.1.2"

import re, subprocess


class Get_Commits_Days():
    '''
    This is a class with the objects' version infomation and the address of the git should be provided.
    '''
    def __init__(self,momversion,versions,address):
        '''
        The attributes of object.

        momversion:the initial version.
        versions:the number of the version information want to know.
        address:the git address.
        '''
        self.momversion = momversion
        self.versions = versions
        self.address = address

    def get_commits_num(self):
        '''
        Get the commits number of each version.

        return the list of commits number of each version.
        '''
        commits = []
        for i in range(1,self.versions+1):
            rev1 = self.momversion    #initial version
            rev2 = self.momversion + "." + str(i)     #the version which should be counted
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            git_rev_list = subprocess.Popen(gitcnt, cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            #run a subprocess to find the modify dairy and return a tuple with (stdoutdata , stderrdata)
            raw_counts = git_rev_list.communicate()[0]
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))    #find the modify date

            if len(cnt) == 0:
                raise ValueError
            else:
                commits.append(len(cnt))
        return commits

    def get_newversion_day(self):
        '''
        Get the distance days of each version to the first.

        return the list of distance days of each version.
        '''
        days = []
        for i in range(0, self.versions+1):
            if i == 0:
                rev = self.momversion
            else:
                rev = self.momversion + "." + str(i)
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev
            git_rev_list = subprocess.Popen(gittag, cwd=self.address, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,shell=True)
            secounds_counts = git_rev_list.communicate()[0]
            if i == 0:
                base = int(secounds_counts)
            else:
                days.append((int(secounds_counts)-base)//24//3600)
        return days

    def make_DaysAndCommits(self):
        '''
        Test the error and return the both commits and days.

        return a list of some lists including the version, commites number and distance days.
        '''
        try:
            DatesCommits = []
            commits = self.get_commits_num()
            days = self.get_newversion_day()
            for i in range(1,self.versions+1):
                DatesCommits.append([self.momversion + "." + str(i), commits[i-1], days[i-1]])
            return DatesCommits
        except ValueError:
            print("The initial version should be like 'v4.1', the versions number should be an int.")
        except FileNotFoundError:
            print("The git address is not correct.")


def doctest():
    '''
    >>> address = "/Users/apple/linux-stable"
    >>> a = Get_Commits_Days("v4.1",5,address)
    >>> print(a.make_DaysAndCommits())
    [['v4.1.1', 12, 7], ['v4.1.2', 72, 18], ['v4.1.3', 138, 29], ['v4.1.4', 408, 42], ['v4.1.5', 532, 49]]
    '''

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)




