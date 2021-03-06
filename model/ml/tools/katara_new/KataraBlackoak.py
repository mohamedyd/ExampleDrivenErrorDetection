from sets import Set

from ml.datasets.blackOak.BlackOakDataSetUppercase import BlackOakDataSetUppercase
from ml.tools.katara_new.Katara import Katara

data = BlackOakDataSetUppercase()

#data.dirty_pd.to_csv('/tmp/data.csv', index=False)

tool = Katara("/home/felix/ExampleDrivenErrorDetection/data/katara/address.txt", data)

print "Fscore: " + str(tool.calculate_total_fscore())
print "Precision: " + str(tool.calculate_total_precision())
print "Recall: " + str(tool.calculate_total_recall())

for c in range(data.shape[1]):
    print tool.calculate_fscore_by_column(c)

tool.write_detected_matrix()