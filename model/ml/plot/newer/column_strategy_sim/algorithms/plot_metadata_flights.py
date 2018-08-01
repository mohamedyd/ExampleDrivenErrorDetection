import numpy as np
from ml.plot.newer.column_strategy_sim.plotlatex_lib import plot_list_latex
from ml.plot.newer.column_strategy_sim.plotlatex_lib import plot_list
from ml.plot.newer.column_strategy_sim.plotlatex_lib import plot_integral
from ml.plot.newer.column_strategy_sim.plotlatex_lib import plot_integral_latex
from ml.plot.newer.column_strategy_sim.plotlatex_lib import plot_outperform
from ml.plot.newer.column_strategy_sim.plotlatex_lib import plot_outperform_latex


labels_all = [4, 8, 12, 16, 26, 36, 46, 56, 66, 76, 86, 96, 106, 116, 126, 136, 146, 156, 166, 176, 186, 196, 206, 216, 226, 236, 246, 256]
svm_sim = []
svm_sim.append([0.18300027163911786, 0.33795603321040096, 0.4065445993483966, 0.4892115141590079, 0.5235250434490144, 0.5419937606553868, 0.6070632057480602, 0.6515631984431995, 0.6590174335187429, 0.6912383340115053, 0.726833760561514, 0.7314499662359514, 0.7543707072810066, 0.7595867281568224, 0.7606555126357, 0.7667167969407223, 0.7847451189717184, 0.7886883675710321, 0.7923830968934222, 0.7952402591229665, 0.7978023365343859, 0.7999886508199492, 0.8020705741062801, 0.8044999325935367, 0.8086983290784566, 0.8109951565279993, 0.8137892376985324, 0.8199269678815341])
average_svm_sim = list(np.mean(np.matrix(svm_sim), axis=0).A1)

bayes_sim = []
bayes_sim.append([0.19904680323047869, 0.3628568888443452, 0.4719428969872901, 0.5749586963306612, 0.551472832595876, 0.5901062044199085, 0.5783209328781219, 0.5895522369560968, 0.5943478527455168, 0.5988997812820969, 0.5984526234034171, 0.6035747792371485, 0.6050902372384163, 0.6076457412031451, 0.6093043317480673, 0.6119034538378124, 0.6145604935292313, 0.6167406482973374, 0.6189630253880698, 0.6194189201726682, 0.6214150185364039, 0.6229091714798158, 0.6231329039819846, 0.6242909552685815, 0.6253755193528068, 0.6258379327997148, 0.6260768478977178, 0.6281222100533495])
average_bayes_sim = list(np.mean(np.matrix(bayes_sim), axis=0).A1)

trees_sim = []
trees_sim.append([0.0, 0.0, 0.0, 0.0, 0.3009828033510852, 0.5261875013216127, 0.6574735566846837, 0.7838476062023378, 0.7889281216279175, 0.7966459938487097, 0.8155764784363694, 0.8340225045292667, 0.8467671035322368, 0.861908390684745, 0.87429555337602, 0.8814245695785825, 0.8880835123925991, 0.8926581255143615, 0.8976074732499342, 0.9024917129518293, 0.9081079570444335, 0.9118599009653838, 0.9173633562596045, 0.9202480039563478, 0.9232285636775994, 0.9243026199361546, 0.9281721415287523, 0.9329826853990767])
average_trees_sim = list(np.mean(np.matrix(trees_sim), axis=0).A1)



ranges = [#labels_all,
		  labels_all,
          labels_all
		  ]
list = [#average_trees_sim,
		average_svm_sim,
		average_bayes_sim

		]
names = [
		 #"Gradient Tree Boosting",
		 "Linear SVM",
		 "Multinomial Naive Bayes"
		 ]


plot_list(ranges, list, names, "Flights", x_max=200, end_of_round=56)
plot_list_latex(ranges, list, names, "Flights", x_max=200)
#plot_integral(ranges, list, names, "Flights", x_max=200,x_min=56, sorted=True)
#plot_end(ranges, list, names, "Flights", x_max=200,x_min=56, sorted=True)
#plot_outperform(ranges, list, names, "Flights", 0.7366, x_max=200)

#plot_outperform(ranges, list, names, "Flights", 0.9, x_max=200)