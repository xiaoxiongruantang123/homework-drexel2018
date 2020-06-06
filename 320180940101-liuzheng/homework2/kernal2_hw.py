from subprocess import Popen, PIPE
import matplotlib.pyplot as plt



def git_timestamp(ver, repo):
    """
    use git command in python to get the timestamp of sublevels of each versions.
    :param ver: The version we want to get the timestamps of sublevels of. It must begin with v, like ver = "v4",
                    if you want to get the timestamps of v4.1, v4.2, etc.
    :param repo: The target directory for the git command. Like repo = "linux-stable",
                    if git command is working in directory "linux-stable".
    :return: ts_llist: the list of lists of timestamps.
             v_llist: the list of lists of versions.
    """
    sl_llist = []
    ts_llist = []
    v_llist = []
    for i in range(11):
        version = ver+'.{}'.format(str(i))
        sl_cmd = 'git tag | grep {} | sort -n -k3 -t"."'.format(version)
        p1 = Popen(sl_cmd, cwd=repo, stdout=PIPE, shell=True)
        sl_all, res = p1.communicate()

        ts_cmd = 'for V in $({}); ' \
                 'do git log -1 --pretty=format:"%ct" $V; echo ''; done'.format(sl_cmd)

        p2 = Popen(ts_cmd, cwd=repo, stdout=PIPE, shell=True)
        ts_all, res = p2.communicate()

        sl_list = []
        ts_list = []
        v_list = []
        for line in sl_all.decode("utf-8").split("\n"):
            if line != '':
                sl_list.append(line)
                v_list.append(version)
            else:
                continue

        sl_llist.append(sl_list)

        for line in ts_all.decode("utf-8").split("\n"):

            if line != '':
                ts_list.append(int(line))

            else:
                continue

        ts_llist.append(ts_list)
        v_llist.append(v_list)
    return ts_llist, v_llist


def picture_sl_ts(ts_llist, v_llist):
    """
    Obtain the picture with x-axis is time in some suitable unit and y-axis is release in order.
    :param ts_llist: list of lists of timestamps.
    :param v_llist: list of lists of versions. The order corresponds to ts_llist.
    """
    for i in range(len(ts_llist)):
        plt.scatter(ts_llist[int(i)], v_llist[int(i)], s=5)

    plt.xlabel('timestamps')
    plt.ylabel('order of versions')
    plt.savefig('result.png')



case = git_timestamp("v4", "linux-stable")
picture_sl_ts(case[0], case[1])

