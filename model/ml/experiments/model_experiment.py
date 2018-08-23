from ml.classes.active_learning_total_uncertainty_error_correlation_class import ActiveLearningErrorCorrelation


from ml.datasets.flights.FlightHoloClean import FlightHoloClean
from ml.datasets.blackOak.BlackOakDataSetUppercase import BlackOakDataSetUppercase
from ml.datasets.hospital.HospitalHoloClean import HospitalHoloClean
from ml.datasets.MoviesMohammad.Movies import Movies
from ml.datasets.RestaurantMohammad.Restaurant import Restaurant
from ml.datasets.BeersMohammad.Beers import Beers
from ml.datasets.Citations.Citation import Citation

from ml.active_learning.classifier.XGBoostClassifier import XGBoostClassifier
from ml.active_learning.classifier.LinearSVMClassifier import LinearSVMClassifier
from ml.active_learning.classifier.NaiveBayesClassifier import NaiveBayesClassifier
import numpy as np

from ml.configuration.Config import Config
import os
import time


path_folder = Config.get("logging.folder") + "/out/model"
if not os.path.exists(path_folder):
    os.makedirs(path_folder)


#data_list = [FlightHoloClean, BlackOakDataSetUppercase, HospitalHoloClean, Movies, Restaurant, Beers]
data_list = [FlightHoloClean]


classifiers = [XGBoostClassifier,LinearSVMClassifier, NaiveBayesClassifier]

parameters = []
parameters.append({}) #default




for dataset in data_list:

    '''
    dataSet,
				 classifier_model,
				 number_of_round_robin_rounds=2,
				 train_fraction=1.0,
				 ngrams=1,
				 runSVD=False,
				 is_word=False,
				 use_metadata = True,
				 use_metadata_only = False,
				 use_lstm=False,
				 user_error_probability=0.00,
				 step_size=10,
				 cross_validation_rounds=1,
				 checkN=10,
				 label_iterations=6,
				 run_round_robin=False,
				 correlationFeatures=True
    '''

    for classifier in classifiers:


        for param_i in range(len(parameters)):

            method = ActiveLearningErrorCorrelation()

            data = dataset()

            my_dict = parameters[param_i].copy()
            my_dict['dataSet'] = data
            my_dict['classifier_model'] = classifier
            my_dict['checkN'] = 10

            fscore_lists, label = method.run(**my_dict)

            f_matrix = np.matrix(fscore_lists)

            average = list(np.mean(f_matrix, axis=0).A1)

            latex = ""
            latex += "\\addplot+[mark=none] coordinates{"

            for c in range(len(average)):
                latex += "(" + str(label[c]) + "," + str(average[c]) + ")"
            latex += "};\n"


            ts = time.time()

            my_file = open( path_folder + '/labels_experiment_data_' + str(data.name) + "_" + classifier.name  + "_time_" + str(ts) + '.csv', 'w+')
            my_file.write(latex)

            my_file.write("\n\n")

            avg_prec = list(np.mean(np.matrix(method.all_precision), axis=0).A1)
            avg_rec = list(np.mean(np.matrix(method.all_recall), axis=0).A1)
            avg_f = list(np.mean(np.matrix(method.all_fscore), axis=0).A1)
            avg_time = list(np.mean(np.matrix(method.all_time), axis=0).A1)

            for i in range(len(label)):
                my_file.write(
                    str(label[i]) + "," + str(avg_time[i]) + "," + str(avg_prec[i]) + "," + str(avg_rec[i]) + "," + str(
                        avg_f[i]) + "\n")

            my_file.write("\n\n\nAVG Precision: " + str(avg_prec))
            my_file.write("\nAll Precision: " + str(method.all_precision))
            my_file.write("\n\nAVG Recall: " + str(avg_rec))
            my_file.write("\nAll Recall: " + str(method.all_recall))
            my_file.write("\n\nLabels: " + str(label))

            my_file.close()

