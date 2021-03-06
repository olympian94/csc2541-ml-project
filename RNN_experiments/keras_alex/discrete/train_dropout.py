import errno
import os
from itertools import product
import numpy as np
from utils.data import *
from utils.dropout import train_models_differences
import numpy as np
import tensorflow as tf
np.random.seed(100)
tf.set_random_seed(100)

def dataset_looper(args):
    datasets = [["co2", load_co2]]
    seq_lens = [1, 5, 10, 20]
    train_percents = [0.8]

    state = "stateless"
    stationarity = "difference"
    dataset_looper_helper(args, datasets, seq_lens, train_percents, state, stationarity)

    # state = "stateful"
    # stationarity = "difference"
    # dataset_looper_helper(args, datasets, seq_lens, train_percents, state, stationarity)

def dataset_looper_helper(args, datasets, seq_lens, train_percents, state, stationarity):
    for dataset, seq_len, train_percent in product(datasets, seq_lens, train_percents):
        data = get_data(args[dataset[0]], dataset[1])
        args["seq_len"] = seq_len
        args["window_length"] = seq_len
        args["train_percent"] = train_percent
        args["data_name"] = dataset[0]
        args["state"] = state
        args["stationarity"] = stationarity

        train_models_differences(data, args)


def main(args):
    if not os.path.exists(os.path.dirname(args["direct"])):
        try:
            os.makedirs(os.path.dirname(args["direct"]))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    if not os.path.exists(os.path.dirname(args["difference"])):
        try:
            os.makedirs(os.path.dirname(args["difference"]))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    dataset_looper(args)


if __name__ == "__main__":
    args = {"seq_len": 40, "seq_dim": 1, "train_percent": 0.7, "co2": "data/mauna-loa-atmospheric-co2.csv",
            "erie": "data/monthly-lake-erie-levels-1921-19.csv", "solar": "data/solar_irradiance.csv",
            "window_length": 40, "difference": "results/dropout/differences/",
            "direct": "results/dropout/direct/",
            "diff_interval": 1, "model_type": "stateless", "stationarity": "difference", "state": "stateless",
            "starts": "single"}

    main(args)