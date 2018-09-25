from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from sklearn.model_selection import cross_val_score
import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing as mp

from xgboost import plot_tree


def convert(data):
    return xgb.DMatrix(data, nthread=-1)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, l.shape[0], n):
        yield l[i:i + n]

def convert_in_parallel(data, jobs, model):
    data_chunks = chunks(data, jobs)

    pool = mp.Pool(processes=jobs)
    results = pool.map(convert, data_chunks)

    probability_predictions = []
    for r in results:
        probability_predictions.append(model.predict(r))
    print(probability_predictions)





class XGBoostClassifier(object):
    name = 'XGBoost'
    def __init__(self, X_train, X_test, balance=False):
        self.params = {}
        self.model = {}

        self.name = XGBoostClassifier.name

        self.X_train = xgb.DMatrix(X_train)
        self.X_test = xgb.DMatrix(X_test)

        self.balance = balance

        self.all_data = None



    def run_cross_validation(self, train, train_target, folds, column_id):
        cv_params = {'min_child_weight': [1, 3, 5],
                     'subsample': [0.7, 0.8, 0.9],
                     'max_depth': [3, 5, 7]}

        ind_params = {  # 'min_child_weight': 1, # we could optimize this: 'min_child_weight': [1, 3, 5]
            'learning_rate': 0.1,  # we could optimize this: 'learning_rate': [0.1, 0.01]
            'colsample_bytree': 0.8,
            'silent': 1,
            'seed': 0,
            'objective': 'binary:logistic',
            'n_jobs': 4
        }

        if self.balance:
            ratio = float(np.sum(train_target == False)) / np.sum(train_target == True)
            print("weight ratio: " + str(ratio))
            ind_params['scale_pos_weight'] = ratio

        optimized_GBM = GridSearchCV(xgb.XGBClassifier(**ind_params),
                                     cv_params,
                                     scoring='f1', cv=folds, n_jobs=1, verbose=0)

        print(train.shape)

        optimized_GBM.fit(train, train_target)

        # print "best scores: " + str(optimized_GBM.grid_scores_)

        our_params = ind_params.copy()
        our_params.update(optimized_GBM.best_params_)

        self.params[column_id] = our_params

    def train_predict_all(self, x, y, column_id, x_all, feature_names=None, column_names=None):
        if self.balance:
            ratio = float(np.sum(y == False)) / np.sum(y == True)
            print("weight ratio: " + str(ratio))
            self.params[column_id]['scale_pos_weight'] = ratio

        xgdmat = xgb.DMatrix(x, y, feature_names=feature_names)
        self.model[column_id] = xgb.train(self.params[column_id], xgdmat, num_boost_round=3000, verbose_eval=False)


        if feature_names != None:
            all_trees = self.model[column_id].get_dump()
            print("number trees:" + str(len(all_trees)))

            plot_tree(self.model[column_id])

            fig = plt.gcf()
            fig.set_size_inches(150, 100)
            plt.savefig('out/' + str(column_id) + "_" + column_names[column_id] + '.pdf')


        # predict
        all_records = xgb.DMatrix(x_all, feature_names=feature_names)
        probability_prediction = self.model[column_id].predict(all_records)
        class_prediction = (probability_prediction > 0.5)

        return probability_prediction, class_prediction

    def train_predict_all(self, x, y, column_id, x_all):
        if self.balance:
            ratio = float(np.sum(y == False)) / np.sum(y == True)
            print("weight ratio: " + str(ratio))
            self.params[column_id]['scale_pos_weight'] = ratio


        print("type: " + str(type(x_all)))

        #if self.all_data == None:
        #    self.all_data = xgb.DMatrix(x_all, nthread=-1)


        s1= time.time()

        xgdmat = xgb.DMatrix(x, y, nthread=-1)


        s2=time.time()
        self.model[column_id] = xgb.train(self.params[column_id], xgdmat, num_boost_round=3000, verbose_eval=False)
        s3 = time.time()

        # predict

        s4 = time.time()
        #all_data_real =xgb.DMatrix(x_all, nthread=-1)
        #probability_prediction = self.model[column_id].predict(all_data_real)

        probability_prediction =convert_in_parallel(x_all, 4, self.model[column_id])

        class_prediction = (probability_prediction > 0.5)
        s5 = time.time()

        print("load1: "+ str(s2 - s1))
        print("train: " + str(s3 - s2))
        print("load2: " + str(s4 - s3))
        print("predict: " + str(s5 - s4))

        return probability_prediction, class_prediction

    def explain_prediction(self, x, column_id, feature_names):
        from eli5.explain import explain_prediction
        params = {}
        params['feature_names'] = feature_names
        params['top'] = 5
        expl = explain_prediction(self.model[column_id], x, **params)
        from eli5.formatters import format_as_text
        params_text = {}
        params_text['show_feature_values'] = True
        return format_as_text(expl, **params_text)

    def train_predict(self, x, y, column_id):
        if self.balance:
            ratio = float(np.sum(y == False)) / np.sum(y == True)
            print("weight ratio: " + str(ratio))
            self.params[column_id]['scale_pos_weight'] = ratio
        xgdmat = xgb.DMatrix(x, y)
        self.model[column_id] = xgb.train(self.params[column_id], xgdmat, num_boost_round=3000, verbose_eval=False)
        # predict
        probability_prediction = self.model[column_id].predict(self.X_train)
        class_prediction = (probability_prediction > 0.5)

        return probability_prediction, class_prediction

    def predict(self, column_id):
        probability_prediction = self.model[column_id].predict(self.X_test)
        class_prediction = (probability_prediction > 0.5)

        return probability_prediction, class_prediction

    def run_cross_validation_eval(self, train, train_target, folds, column_id):
        scores = cross_val_score(xgb.XGBClassifier(**self.params[column_id]), train, train_target, cv=folds, scoring='f1')
        return scores