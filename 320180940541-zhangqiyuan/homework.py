
#__author__ = "Qiyuan Zhang"
import os, re, sys
from datetime import datetime as dt
from subprocess import Popen, PIPE, DEVNULL

class git_commit:
    '''
    ask command line and count by using git
    >>> gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
    >>> commit_cnt = git_commit(gitcnt)
    >>> print(commit_cnt.get_commit_cnt())
    85
    >>> get_time = "git log -1 --pretty = format:\"%ct\" v4.41"
    >>> gettime = get_commit_cnt(get_time)
    >>> time = gettime.get_time()
    >>> print(time)
    3284782
    >>> gettag = "git log -1 --pretty = format:\"%ct\" v4.4"
    >>> get_tag = git_commit(gettag)
    >>> print(get_tag.get_tag_days(time))
    -26427 
    '''
    def __init__(self,command):
        self.git_cmd = Popen(command,stdout=PIPE,stderr=DEVNULL,shell=True)
        
		    
    def get_commit_cnt(self):
       try:
           raw_counts = self.git_cmd.communicate()[0]
       except IndexError:
	       raise IndexError("wrong commit")
	   
   # if we request something that does not exist -> 0
       cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
       return len(cnt)

    def get_tag_days(self,base):
        runhour=3600
        try:
            seconds = self.git_cmd.communicate()[0]
        except IndexError:
            raise IndexError("wrong commit")
        return ((int(seconds)-base))//runhour
    def get_time(self):
        get_time = self.git_cmd.communicate()[0]
        times = str(git_time.decode("UTF-8")).split("v")[0]
        return int(times)

# get dates of all commits - unsorted
def main():
    rev = sys.argv[1]
    cumulative = 0
    if len(sys.argv) == 4:
        if (sys.argv[3] == "c"):
            cumulative = 1
        else:
            print("Dont know what you mean with %s" % sys.argv[3])
            sys.exit(-1)
    rev_range = int(sys.argv[2])

    print("#sublevel commits %s stable fixes" % rev)
    print("lv hour bugs") 
    rev1 = rev
    v44 = 1452466892

    for sl in range(1,rev_range+1):
        rev2 = rev + "." + str(sl)
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        git_rev_list=git_commit(gitcnt)
        commit_cnt = git_rev_list.get_commit_cnt()
        if cumulative == 0:
            rev1 = rev2
        if commit_cnt:
            git_tag_date = git_commit(gittag)
            days = git_tag_date.get_tag_days(v44)
            print("%d %d %d" % (sl,days,commit_cnt))
        else:
            break

if __name__== '__main__':
    main()
