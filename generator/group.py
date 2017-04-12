import jsonpickle
import os
import random
import string
from model.group import Group
import getopt
import sys


# Edit Configurations > Script parameters > -n 10 -f data/test.json  # to generate 10 data_sets in new test file
# https://docs.python.org/2/library/getopt.html
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f", ["number of groups", "file"])
except getopt.GetoptError as err:
    print str(err)  # will print something like "option -a not recognized"
    getopt.usage()
    sys.exit(2)

n = 5
file_path = "data/groups.json"

for o, a in opts:
    if o == '-n':
        n = int(a)
    elif o == '-f':
        file_path = a


# generator of random strings, maxlen var for passing to function max string len
def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + ' ' * 10  # + 10 spaces
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])


# one group with empty strings and 5 random test_data strings
testdata = [Group(name='', header='', footer='')] + [
    Group(name=random_string('name', 10), header=random_string('header', 20), footer=random_string('footer', 20))
    for i in range(5)
]


# path to file
file1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", file_path)

# file groups.json creation with testdata in it
with open(file1, 'w') as f:
    jsonpickle.set_encoder_options('json', indent=2)
    f.write(jsonpickle.encode(testdata))


    # # this block to work with simple json
    # f.write(json.dumps(testdata, default=lambda x: x.__dict__, indent=2))
    # # json.dumps Serialize ``obj`` to a JSON formatted ``str``
    # # x.__dict__ transform to dictionary
    # # indent=2 json file formating


# testdata = [
#     Group(name=random_string('name', 10), header=random_string('header', 20), footer=random_string('footer', 20)),
#     Group(name='', header='', footer='')
# ]


# 8 groups as a result, for every parameter in Group we loop through empty or random value
# '','',''
# '','',footer
# '',header,''
# '',header,footer
# name,'',''
# name,'',footer
# name,header,''
# name,header,footer

# testdata = [
#     Group(name=name, header=header, footer=footer)
#     for name in ['', random_string('name', 10)]
#     for header in ['', random_string('header', 10)]
#     for footer in ['', random_string('footer', 10)]
# ]