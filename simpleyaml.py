# This is the simplest way to read YAML but I'm not sure how to automatically turn Python
# dictionary keys into variable names to make the parsing automated
# There are python config parsers in YAML but I haven't found them to be super reliable

import yaml

stream = open("config.yaml", 'r')
dictionary = yaml.load(stream)
for key, value in dictionary.items():
    print(key + " : ", str(value))