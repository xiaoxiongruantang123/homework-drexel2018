"""
Personal information:
Name, ID, E-mail
Song Xiujie   320180940211  songxj2018@lzu.edu.cn
"""

"""
Take the brute-force shell-script snippets from kernel2 and
convert it into a python executable to deliver the
1 timestamps of all tags for all kernel versions
2 plot it with x-axis is time in some suitable unit and y-axis
is release in order. Sort the kernel release versions correctly as well.
3 Make sure that the labels on the x and y axis explain what the data is about and use a meaningful title.
"""

__copyright__ = 'T1,Lanzhou University,2020'
__license__ = 'GPLV2 or later'
__version__ = 0.1
__author__ = ['Xiujie Song']
__email__ = ['songxj@lzu.edu.cn']
__status__ = 'done'


from subprocess import Popen, PIPE
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import MultipleLocator
from random import choice


class Reproduce:
    def __init__(self,kVer):
        self.versions=[]
        self.dates=[]
        self.repo="f:/linux_stable/linux-stable"
        self.kVer=kVer

    def gitTagDate(self):
        """sorted version"""

        cmd = " ".join(["git", "tag", "|", "sort", "-n", "-k3", "-t '.'", "|", "grep", self.kVer])
        p = Popen(cmd, cwd=self.repo, stdout=PIPE, shell=True)
        data = p.communicate()[0]
        for i in data.decode('utf-8').split('\n'):
            self.versions.append(i)
        return self.versions

    def gitDate(self):
        """Iterating over the sorted tags, return timestamps"""
        # cmd_str = 'for V in $(git tag | grep v4.4 | sort -n -k3 -t"."); do git log -1 --pretty=format:"%cd" $V; echo ''; done'
        for V in self.versions:
            cmd_str='git log -1 --pretty=format:"%ct" {}'.format(V)
            p=Popen(cmd_str, cwd=self.repo, stdout=PIPE, shell=True)
            self.dates.append(int(p.communicate()[0].decode("utf-8")))
        # for line in p.communicate()[0].decode("utf-8").split("\n"):
        #     dates.append(line)
        # print(dates)
        return self.dates


def plot(version,number):
    # drawing plots
    shape=['o','x','v','1','D',',','2','d']
    color=['#ff1212', '#000000', '#006400', '#FF8C00', '#2F4F4F','#ADFF2F','#FF69B4','#FFE4E1','#9ACD32']
    plt.title('')

    plt.xlabel('seconds')
    plt.ylabel('patchlevel')

    plt.title(version.format('X')+' release time in second')

    for i in [version.format(x) for x in range(number)]:
        v = Reproduce(i)
        v.gitTagDate()
        v.gitDate()
        xValue = v.dates
        yValue = [i] * len(v.versions)
        plt.scatter(xValue, yValue, s=10, c=choice(color), marker=choice(shape))

    x_major_locator = MultipleLocator(10000000)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    ax.set_xticklabels(xValue,fontsize=6, rotation=15)

    plt.show()

if __name__ == '__main__':
    plot('v3.{}',19)
    plot('v4.{}',21)
    plot('v5.{}',7)