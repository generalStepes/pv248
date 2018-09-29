import scorelib
import sys

data = scorelib.load(sys.argv[1])
for item in data:
    print(item.format())
