from ml.datasets.flights.FlightHoloClean import FlightHoloClean
from ml.datasets.blackOak.BlackOakDataSetUppercase import BlackOakDataSetUppercase
from ml.datasets.hospital.HospitalHoloClean import HospitalHoloClean
from ml.datasets.MoviesMohammad.Movies import Movies
from ml.datasets.RestaurantMohammad.Restaurant import Restaurant
from ml.datasets.BeersMohammad.Beers import Beers
from ml.datasets.salary_data.Salary import Salary
from ml.datasets.Citations.Citation import Citation

import time
import csv

from ml.configuration.Config import Config
import numpy as np
import os
from ml.tools.katara_new.Katara import Katara


path_folder = Config.get("logging.folder") + "/out/katara"

if not os.path.exists(path_folder):
    os.makedirs(path_folder)

#data_list = [FlightHoloClean, BlackOakDataSetUppercase, HospitalHoloClean, Movies, Restaurant, Beers]

#data_list = [Movies]

data_list = [HospitalHoloClean]


for dataset in data_list:

    data = dataset()

    #data.clean_pd.to_csv(Config.get('abstractionlayer.folder') + '/tools/KATARA/domainGroundtruth/groundtruth.rel.txt',
    #                     header=None, index=False, encoding='utf-8', sep='\t')


    ts = time.time()
    log_file = path_folder + "/" + str(data.name) + "_time_" + str(ts) + "_KATARA_"  + ".txt"

    dirty_dataset = '/tmp/dirty_dataset.csv'

    dirty_df = data.dirty_pd.copy()

    for column_i in range(dirty_df.shape[1]):
        dirty_df[dirty_df.columns[column_i]] = dirty_df[dirty_df.columns[column_i]].apply(lambda x: x.upper())

    dirty_df.to_csv(dirty_dataset, index=False, encoding='utf-8')

    start_time = time.time()

    command = "cd " + Config.get("abstractionlayer.folder") + "/\n" + "python2 cleaning_api.py"
    print command
    os.system(command)


    if os.stat('/tmp/katara_log_felix.txt').st_size == 0:
        print "KATARA did not work"
    else:
        tool = Katara('/tmp/katara_log_felix.txt', data)

        my_file = open(log_file, 'w+')
        my_file.write("Fscore: " + str(tool.calculate_total_fscore()) + "\n")
        my_file.write("Precision: " + str(tool.calculate_total_precision()) + "\n")
        my_file.write("Recall: " + str(tool.calculate_total_recall()) + "\n")
        my_file.write("Runtime: " + str(time.time() - start_time) + "\n")
        my_file.close()

        for c in range(data.shape[1]):
            print str(data.clean_pd.columns[c]) + ": " + str(tool.calculate_recall_by_column(c))
            print str(data.clean_pd.columns[c]) + ": " + str(tool.calculate_precision_by_column(c))