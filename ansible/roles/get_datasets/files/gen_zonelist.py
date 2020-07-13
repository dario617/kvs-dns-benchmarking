import itertools
import random
import re
import sys

if len(sys.argv) != 2:
    print("{:s} <count>".format(sys.argv[0]))
    sys.exit(1)

count    = int(sys.argv[1])
suffix   = ('com', 'net', 'cz', 'co.uk', 'gov', 'edu', 'info')
wordlist = []
names    = []

# Prepare zone list
def permute_write(wordlist, n):
    for p in itertools.permutations(wordlist, n):
         names.append('%s.%s.' % (''.join(p), random.choice(suffix)))

for p in open('./wordlist', 'r'):
    wordlist.append(p.strip())

for n in range(1, 4):
    permute_write(wordlist, n)

random.shuffle(names)

# Prepare zone template
with open("./zone.tpl", 'r') as tpl_file:
    tpl=tpl_file.read()

# Create zonelist and stub.zone
zonelist = open("zonelist", "w")
#stubzone = open("./zones/stub.zone", "w")

for i in range(0, count):
    name = names[i]
    zonelist.write(name)
    zonelist.write("\n")
    zone=re.sub("@DOTZONE@", "." + name, tpl)
    zone=re.sub("@ZONE@", name, zone)
    stubzone.write(zone)
    with open("./zones/{}zone".format(name),"w") as f:
        f.write(zone)

#stubzone.close()
zonelist.close()
