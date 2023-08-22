from NHBC_12x16_1000x1000 import half_data_1k_12x16
data_1k_12x16 = {"5000": {"PD": {"max": 0.01653102, "min": 0.01618694}, "CC": {"max": 0.09982920000000002, "min": 0.097842}}, "10000": {"PD": {"max": 0.01652343, "min": 0.01624513}, "CC": {"max": 0.099774, "min": 0.0984768}}}
for key in list(data_1k_12x16.keys()):
    half_data_1k_12x16[key] = data_1k_12x16[key]
data_1k_12x16 = half_data_1k_12x16