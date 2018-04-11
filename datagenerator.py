#!/usr/bin/env python3

"""
    This module tries to generate images.
    The generator is actually a python generator and is also used synonymously
    with batch generation (here)
"""


import glob
import os
import re

import numpy as np

class ImagePathGenerator:
    """
        This class is solely used for loading image paths (not actual images)
        Idea is:
            instead of loading all the images and then creating batches,
            we load only the paths and then create batches :P
    """
    def __init__(self, root='data/'):
        self.root = root
        self.pathmap = self.generate_pathmap(root)
        self.total_images = sum([len(paths) for label, paths in self.pathmap.items()])
        self.labels = sorted(self.pathmap.keys())

    def generate_pathmap(self, root):
        dirs = glob.glob(root + '*')
        pathmap = {}

        # loop labelled directory
        for dirname in dirs:
            label = dirname.split('/')[1]

            # use path info available from mit files
            mits = glob.glob(dirname + '/*.mit')
            image_paths = []
            num_images = 0
            for mit in mits:
                with open(mit, 'r') as f:
                    num_images += int(f.readline().strip())
                    for line in f.readlines():
                        image = line.split()[0]
                        # split to extract subdirectory name
                        splitted = image.split('_')
                        imgpath = '_'.join(splitted[:2])
                        imgpath = dirname + '/' + imgpath + '/' + image
                        image_paths.append(imgpath)
            pathmap[label] = image_paths
            print("Total images for label :: {} ==> {}".format(label, num_images))
        return pathmap

    def get_train_test(self, train=0.8, shuffle=False):
        """
            This splits the pathmap into training and test.
            It creates two dicts from existing pathmap
        """
        if train <= 0 or train >= 1:
            raise ValueError("Train size should be the range (0, 1)")
        test = 1 - train
        train_pathmap = {}
        test_pathmap = {}
        for label, paths in self.pathmap.items():
            if shuffle:
                np.random.shuffle(paths)
            num_images = len(paths)
            train_idx = int(num_images * train)
            test_idx =  num_images - train_idx
            train_pathmap[label] = paths[:train_idx]
            test_pathmap[label] = paths[train_idx : train_idx + test_idx]
        return train_pathmap, test_pathmap



def main():
    imgen = ImagePathGenerator(root='data/')
    print(imgen.total_images)
    print(imgen.labels)
    train_pathmap, test_pathmap = imgen.get_train_test(train=0.8, shuffle=True)


if __name__ == "__main__":
    main()

