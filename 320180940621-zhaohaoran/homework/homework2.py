#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

"""
Our group submit this individual assignment as group assignment

This is code about plotting the graph, using the output csv file of homework.py.
The input file is a csv file, containing a  dataframe with three columns: lv, hours, bugs
The output are four png files: hours_v4.4.png is the line chart of hours and bug commits,
sublevel_v4.4.png is the line chart of sublevels and bug commits. hours_v4.4_scatter.png
is the scatter chart of hours and bug commits. sublevels_v4.4_scatter.png is the scatter
chart of sublevels and bug commits.
"""

__author__ = "Group03"
__copyright__ = "Copyright 2019, OpenTech Research"
__credits__ = ["Group03"]
__version__ = "1"
__maintainer__ = "Linux maintainer"
__email__ = "lingx18@lzu.edu.com"
__status__ = "Experimental"


import matplotlib
# Ubuntu in windows is not installed with GUI, this make sure the code is running without exceptions
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
sublevels = []
release_hours = []
bug_commits = []


def plot_graph(file1):
    df = pd.read_table(file1, sep=',')  # read csv file with comma separator
    for i in range(df.index[-1]+1):  # for loop to put every value in dataframe into corresponded list
        sub_ele = df.loc[i, 'lv']
        hour_ele = df.loc[i, 'hour']
        bug_ele = df.loc[i, 'bugs']
        sublevels.append(sub_ele)
        release_hours.append(hour_ele)
        bug_commits.append(bug_ele)
    # plot the line chart to show the relation between hours and bug commits
    plt.plot(sublevels, bug_commits)
    plt.title("development of fixes over sublevel")
    plt.ylabel("kernel sublevel stable release")
    plt.xlabel("stable fix commits")
    plt.savefig("sublevels_v4.4.png")
    plt.clf()
    # plot the line chart to show the relation between sublevels and bug commits
    plt.plot(sublevels, bug_commits)
    plt.title("development of fixes over hours")
    plt.ylabel("kernel sublevel stable release")
    plt.xlabel("stable fix commits")
    plt.savefig("hours_v4.4.png")
    plt.clf()
    # plot the scatter chart to show the relation between hours and bug commits
    plt.scatter(release_days, bug_commits, c='b')
    plt.title("development of fixes over hours")
    plt.ylabel("kernel sublevel stable release")
    plt.xlabel("stable fix commits")
    plt.savefig("hours_v4.4_scatter.png")
    plt.clf()
    # plot the scatter chart to show the relation between sublevels and bug commits
    plt.scatter(sublevels, bug_commits, c='r')
    plt.title("development of fixes over sublevel")
    plt.ylabel("kernel sublevel stable release")
    plt.xlabel("stable fix commits")
    plt.savefig("sublevels_v4.4_scatter.png")
    plt.clf()


plot_graph('Test.csv')  # Test.csv is the output file of last homework.py
