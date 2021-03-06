import numpy as np

from ml.datasets.blackOak import BlackOakDataSet


class TamrOnBlackOak(Tool):
    def __init__(self, blackOakDataSet=BlackOakDataSet()):
        path_to_tool_detected = "/home/felix/BlackOak/List_A/ToolOutputDetectedCells/tamr.csv"
        path_to_tool_correct_detected = "/home/felix/BlackOak/List_A/ToolOutputCorrectCells/tamr_CorrectCells.csv"
        super(TamrOnBlackOak, self).__init__("Tamr", blackOakDataSet, path_to_tool_detected, path_to_tool_correct_detected)
        #self.validate()

    # validate by the results obtained from the paper "Detecting Data Errors: Where are we and what needs to be done?"
    def validate(self):
        np.testing.assert_almost_equal(0.50, self.calculate_total_fscore(), decimal=2, err_msg='', verbose=True)
        np.testing.assert_almost_equal(0.41, self.calculate_total_precision(), decimal=2, err_msg='', verbose=True)
        np.testing.assert_almost_equal(0.63, self.calculate_total_recall(), decimal=1, err_msg='', verbose=True)
