def parse_boolean(val, true_values=('1', 'yes', 'y', 'true', 't')):
    return val.lower() in true_values