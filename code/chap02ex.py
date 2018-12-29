"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function

import sys
#from operator import itemgetter

import first
import thinkstats2

import numpy as np


def Mode(hist):
    """Returns the value with the highest frequency.

    hist: Hist object

    returns: value from Hist
    """
    return AllModes(hist)[0][0]


def AllModes(hist):
    """Returns value-freq pairs in decreasing order of frequency.

    hist: Hist object

    returns: iterator of value-freq pairs
    """
    return sorted(hist.Items(),reverse=True,key=lambda x: x[1])


def CohenEffectSize(group1, group2):
    """Computes Cohen's effect size for two groups.

    group1: Series or DataFrame
    group2: Series or DataFrame

    returns: float if the arguments are Series;
             Series if the arguments are DataFrames
    """
    diff = group1.mean() - group2.mean()

    var1 = group1.var()
    var2 = group2.var()
    n1, n2 = len(group1), len(group2)

    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / np.sqrt(pooled_var)
    return d


def weight_diff(births, others=None):
    """

    :param births: All birth data, or first birth data if others is included
    :type births: DataFrame
    :param others: All other birth data; if missing this data is extracted from births
    :type others: DataFrame
    """
    if others is None:
        firsts = births[births.birthord == 1]
        others = births[births.birthord > 1]
    else:
        firsts = births

    firsts_mean = firsts.totalwgt_lb.mean()
    others_mean = others.totalwgt_lb.mean()

    print("Are first babies heavier? ", firsts_mean > others_mean)
    print("First babies, mean totalwgt_lb: ", firsts_mean)
    print("Other babies, mean totalwgt_lb: ", others_mean)
    print("Cohen d: ", CohenEffectSize(firsts.totalwgt_lb,others.totalwgt_lb))

    print("First baby pregnancy length mean: ", firsts.prglngth.mean())
    print("Other baby pregnancy length mean: ", others.prglngth.mean())
    print("Cohen d: ", CohenEffectSize(firsts.prglngth,others.prglngth))


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    live, firsts, others = first.MakeFrames()
    hist = thinkstats2.Hist(live.prglngth)

    # Compare data
    weight_diff(live)

    # test Mode    
    mode = Mode(hist)
    print('Mode of preg length', mode)
    assert mode == 39, mode

    # test AllModes
    modes = AllModes(hist)
    assert modes[0][1] == 4693, modes[0][1]

    for value, freq in modes[:5]:
        print(value, freq)

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
