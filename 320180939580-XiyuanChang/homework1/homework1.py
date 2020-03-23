'''
get the counts of sublevels, the release hours of per sublevel and commit count per sublevel pointwise or cumulative.
Data visulization to inspect data.
Passing the path storing linux kernel code as repo.
__author__  = "XiyuanChang 4320180939580"
__copyright__= "XiyuanChang, Lanzhou University"
__license__ = "GPL V2"
__version__ = "0.2"
__email__ = "xychang2018@lzu.edu.cn"
__status__ = "continous modification"
__maintainer__"XiyuanChang"

'''
import os, re, sys
from subprocess import Popen,PIPE,DEVNULL
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from prettytable import PrettyTable

#Custom exceptions to catch  the exception when Popen return no value
class NotexistException(Exception):
    def __str__(self):
        return("Don't request something that does not exist")
class RevnoException(Exception):# catch the invalid revision number when rev1 = rev2
    def __str__(self):
        return("Invalid revision number")

class sl_time_cnt(self,repo):
    def __init__(self,repo):
        self.repo = repo
        parser=argparse.ArgumentParser(description="to return git revision number and sublevel")
        parser.add_argument('revision_no', type = str, help="reversion=v4.4")
        parser.add_argument('rev_range', type=str, help='sublevel range,v4.4_sl_range=203')
        parser.add_argument('-c','--cumulative',type=str, help='argv[3]="c" rev_range cumulative')
        args = parser.parse_args()

        self.rev = args.revision_no
        self.cumulative = 0
        self.rev_range = int(args.rev_range)
        self.subl = []
        self.hour=[]
        self.cnt = []
        self.hour_cmd = ["git","log","-1", '--pretty=format:"%ct"',self.rev]
        self.basetime = Popen(cmd,cwd = repo, stdout=PIPE, stderr=DEVNULL, shell=True)#get ref base time(release hour of v4.4)
        self.bt = int(self.basetime)
        
        #test the input repo and check whether it is accessible or not
        try:
            assert type(repo) == str, 'Invalid repo input'
            f =open(repo)
            f.close()
        except IOError:
            print("File is not accessible.")
            sys.exit(-1)

        if args.cumulative == 'c':
            self.cumulative = 1
        else:
            excep = "Dont know what you mean with {}".format(args.cumulative)
            print(excep)
            sys.exit(-1)

    def git_commit_cnt(self, rev_2, repo):
         '''
        To gain commits of per sulevel
        >>> output.git_commit_cnt("v4.4-rc1","C:/Users/xycha/Desktop/linux kernel/linux")
        1856
        '''
        rev1=self.rev
        #rev2 = rev1+ "." + str(self.rev_range)
        try:
            cmd = ["git","rev-list",'--pretty=format:"%ai"',rev1+'...'+rev_2]
            git_rev_list = Popen(cmd,cwd=repo, stdout=PIPE,stderr=DEVNULL, shell=True)
            raw_counts = git_rev_list.communicate()[0]
            if len(raw_counts) == 0:
                raise NotexistException
            else:
                cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts.decode()))
                return(len(cnt))
        except NotexistException,err:
            print("catch the exception: ",err)
            sys.exit(-1)

            

    def get_tag_hour(self,rev_2,repo,base):
        '''
        get release hours of per sublevel
        >>> output.get_tag_hour("v4.4","C:/Users/xycha/Desktop/linux kernel/linux")
        403463
        '''
        hour_sec = 3600
        try:
            cmd = ["git","log","-1",'--pretty=format:"%ct"',rev_2]
            git_tag_hour = Popen(cmd,cwd = repo, stdout=PIPE, stderr=DEVNULL, shell=True)
            hour_sec = 3600
            seconds = git_cmd.communicate()[0]
            if len(seconds) == 0:
                raise NotexistException
            else:
                return((int(seconds)-base)//hour_sec)
        except NotexistException,err:
            print("catch the exception: ",err)
            sys.exit(-1)


    def get_data(self,repo):#get the list[sublevel,hours,commits]
        sublevel = self.subl
        hour = self.hour
        commits = self.cnt
        try:
            rev1 = self.rev
            for sl in range(1, self.rev_range+1):
                sublevel.append(sl)
                rev2 = self.rev + '.' + str(sl)
                commit_cnt = self.git_commit_cnt(rev2,repo)
                commits.append(commit_cnt)
                if self.cumulative == 0:
                    raise RevnoException
                else:
                    if commit_cnt:
                        hours = self.get_tag_hour(rev2,repo,self.bt)
                        hour.append(hours)
                        return(sublevel, hour, commits)
                    else:
                        break
        except RevnoException, err:
            print(err)


    def image(self):#data visulization
        plt.scatter(self.sublevels, self.commits)
        plt.title("scatter: development of fixes over sublevel")
        plt.ylabel("stable fix commits")
        plt.xlabel("kernel sublevel stable release")
        plt.savefig("scatter: sublevel_%s.png" % self.rev)
        plt.clf()

        plt.plot(self.sublevels, self.commits)
        plt.title("plot: development of fixes over sublevel")
        plt.ylabel("stable fix commits")
        plt.xlabel("kernel sublevel stable release")
        plt.savefig("plot: sublevel_%s.png" % self.rev)
        plt.clf()

        plt.scatter(self.hour, self.cnt)
        plt.title("scatter: development of fixes over days")
        plt.ylabel("stable fix commits")
        plt.xlabel("hours spent")
        plt.savefig("scatter: hours_%s.png" % self.rev)
        plt.clf()

        plt.plot(self.hour, self.cnt)
        plt.title("plot: development of fixes over days")
        plt.ylabel("stable fix commits")
        plt.xlabel("hours spent")
        plt.savefig("plot: hours_%s.png" % self.rev)
    


    def main(self, repo):
        '''to show the sublevel,hour,commits in a table and show images:sublevels vs commits; hours vs commits '''
        head = "sublevel commits {} stable fixes".format(self.rev)
        print(head)
        sl_hour_cnt = self.data(repo)
        sublevel = sl_hour_cnt[0]
        hour = sl_hour_cnt[1]
        commit = sl_hour_cnt[2]
        outtable = PrettyTable()#printout all data in a table and in this table, there are 3 columns
        outtable.add_column("sublevel",sublevel)
        outtable.add_column("hour",hour)
        outtable.add_column("commit",commit)
        print(outtable)

        #to show four images
        self.image()

if __name__ == '__main__':
    output = sl_time_cnt("C:/Users/xycha/Desktop/linux kernel/linux")
    import doctest
    doctest.testmod(verbose=True)
    output.main()
    

    
        
