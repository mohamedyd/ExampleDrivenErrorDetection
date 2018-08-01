from sets import Set

from ml.datasets.HospitalDomainError.HospitalDomainError import HospitalDomainError
from ml.tools.nadeef_detect.FD import FD
from ml.tools.nadeef_detect.NadeefDetect import NadeefDetect

data = HospitalDomainError()

rules = []
rules.append(FD(Set(["phone_number"]), "zip_code"))
rules.append(FD(Set(["phone_number"]), "city"))
rules.append(FD(Set(["phone_number"]), "state"))

rules.append(FD(Set(["zip_code"]), "city"))
rules.append(FD(Set(["zip_code"]), "state"))

rules.append(FD(Set(["measure_code"]), "measure_name"))
rules.append(FD(Set(["measure_code"]), "condition"))

rules.append(FD(Set(["measure_code", "provider_number"]), "stateavg"))
rules.append(FD(Set(["measure_code", "state"]), "stateavg"))

nadeef = NadeefDetect(data, rules, log_file="/home/felix/ExampleDrivenErrorDetection/log/NADEEF/hospital_detect.txt")