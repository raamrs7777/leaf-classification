import os
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
from skimage import io

import data_helpers

base_path = os.path.dirname(os.getcwd())


class GameState:
    def __init__(self):
        self.score = self.loopIter = 0
        self.frames, self.labels, self.ids = load_data()

    def reset(self):
        self.score = self.loopIter = 0
        self.frames, self.labels, self.ids = load_data()
        ind_label = np.where(self.ids == int(self.frames[self.loopIter]))
        return load_image(self.frames[self.loopIter]), self.labels[ind_label[0]]

    def frame_step(self, input_action):
        ind_label = np.where(self.ids == int(self.frames[self.loopIter]))
        if self.labels[ind_label[0]] == input_action:
            self.score += 1
            reward = 1
        else:
            self.score -= 1
            reward = -1

        self.loopIter += 1
        image_data = load_image(self.frames[self.loopIter])
        ind_label = np.where(self.ids == int(self.frames[self.loopIter]))
        return image_data, reward, False, self.labels[ind_label[0]]


class TestState:
    def __init__(self):
        self.loopIter = 0
        self.frames = load_test_data()

    def reset(self):
        self.loopIter = 0
        self.frames = load_test_data()
        image_id = int(self.frames[self.loopIter])
        return load_image(self.frames[self.loopIter]), self.frames.shape[0], image_id, load_species_list()

    def frame_step(self, input_action):
        self.loopIter += 1
        image_data = load_image(self.frames[self.loopIter])
        image_id = int(self.frames[self.loopIter])
        return image_data, image_id


def load_test_data():
    df = pd.read_csv('{}/test.csv'.format(base_path))
    image_id = df[['id']].values
    shuffle = data_helpers.shuffle_test_data(image_id)
    return shuffle


def load_species_list():
    df = pd.read_csv('{}/train.csv'.format(base_path))
    return data_helpers.convert_labels_to_species(df.species)


def load_data():
    df = pd.read_csv('{}/train.csv'.format(base_path))
    image_id = df[['id']].values
    species = df.species
    species = species.values.reshape((species.shape[0], 1))
    stacked = np.concatenate((image_id, species), axis=1)
    ids, labels = data_helpers.convert_species_to_labels(stacked)
    shuffle_id, shuffle_labels = data_helpers.shuffle_data(ids, labels)
    return shuffle_id, shuffle_labels, image_id


def load_image(image_id):
    return io.imread('{0}/processed/{1}.jpg'.format(base_path, str(int(image_id))))
