"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function

import numpy as np
import sys

import nsfg
import thinkstats2


def clean_fem_resp(df):
    """

    :type df: pd.DataFrame
    """
    verify_pregnum_check = [2610,   # 0
                            1267,   # 1 Pregnancy
                            1432,   # 2 Pregnancy
                            1110,   # 3 Pregnancy
                            611,    # 4 Pregnancy
                            305,    # 5 Pregnancy
                            150,    # 6 Pregnancy
                            158]    # 7 or more
    verify_pregnum=df.pregnum.value_counts().sort_index()
    # verify counts for 0 through 7
    for (index, value) in verify_pregnum[0:7].items():
        assert verify_pregnum_check[index]==value
    # verify the count for 7 or more by summing the value_count data
    assert verify_pregnum_check[7] == verify_pregnum[7:].sum()
    return df


def read_fem_resp(datfile='2002FemResp.dat.gz', dctfile='2002FemResp.dct'):
    """
    Reads the respondent file filename and returns the DataFrame  

    :type datfile: str
    :type dctfile: str
    :rtype: pd.DataFrame
    """
    dct = thinkstats2.ReadStataDct(dctfile)
    df = dct.ReadFixedWidth(datfile, compression='gzip')
    clean_fem_resp(df)
    return df


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    respdata=read_fem_resp()
    pregdata=nsfg.ReadFemPreg()
    preg_index_dict = nsfg.MakePregMap(pregdata)
    for (caseid, indexes) in preg_index_dict.items():
        assert len(indexes) == respdata.pregnum[respdata.caseid == caseid].values

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
