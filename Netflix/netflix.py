# !user/bin/python

# Author: Chun Zheng
# Assignment: Netflix program
# Lang: python 3.4
# Class: 4440 Artif Intell.
# ʕ•ᴥ•ʔ bear for encouragement

import json
import numpy as np

class Netflix(object):

    # load the npy file.

    def __init__(self):

        #npyfile = input("what file would you like to read?: ")
        train_file = "../train.npy"
        test_file = "../test.npy"
        valid_file = "../validation.npy"
        self.train_data = np.load(train_file)
        self.test_data = np.load(test_file)
        self.train_data = np.load(valid_file)

        print(self.train_data)
        print(self.test_file)

        # the first column is the user index
        #  2nd is the movie index
        #  and the third is the user rating.

    def store_results(self):

        with open('results.txt', 'w') as fp:
            lines = ['%f\n' % x for x in r_hat]
            fp.writelines(lines)

test = Netflix()
