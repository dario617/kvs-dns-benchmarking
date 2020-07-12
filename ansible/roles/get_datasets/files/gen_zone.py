#!/usr/bin/env python

import itertools
import random
import sys
import os

if len(sys.argv) != 3:
    print("{:s} <zonename> <rrcount>".format(sys.argv[0]))
    sys.exit(1)

suffix   = str(sys.argv[1])
rrcount  = int(sys.argv[2])
out_dir  = 'zones'
out_file = suffix + '.zone'
wordlist = []

# Generate random number
def rnd(a, b):
    return random.randint(a, b)

def rnd_hex(l):
    return '%x' % random.randrange(256**(l/2))

# Random IPv4
def rnd_ip4():
    return '%d.%d.%d.%d' % (rnd(0,255), rnd(0,255), rnd(0,255), rnd(0,255))

# Random IPv6
def rnd_ip6():
    addr = 'fd9c:20c0:91fc:cb36'
    for i in range(0,4):
        addr += ':' + rnd_hex(4)
    return addr

# Write out RR
def rr_write(dst, name, rrtype, val):
    return dst.write('%s 3600 %s %s\n' % (name, rrtype, val))

# Write out header
def header_write(dst):
    origin = suffix + '.'
    ns1 = 'ns1.' + origin
    ns2 = 'ns2.' + origin
    rr_write(dst, origin,    'SOA', 'a.outside. b.outside. 2013100800 1800 900 604800 86400')
    rr_write(dst, origin,    'NS',  ns1)
    rr_write(dst, origin,    'NS',  ns2)
    rr_write(dst, ns1, 'A',   rnd_ip4())
    rr_write(dst, ns2, 'AAAA',rnd_ip6())
    global count
    count += 5

# Write out permutations
def permute_write(dst, wordlist, n):
    global count
    for p in itertools.permutations(wordlist, n):
        if count > rrcount:
            return
        # Each unique name has two delegations and an A/AAAA
        name  = '%s.%s.' % (''.join(p), suffix)
        ns1 = 'ns1.' + name
        ns2 = 'ns2.' + name
        rr_write(dst, name, 'NS',   ns1)
        rr_write(dst, name, 'NS',   ns2)
        rr_write(dst, ns1,  'A',    rnd_ip4())
        rr_write(dst, ns2,  'AAAA', rnd_ip6())
        count += 4


# Prepare output directory
try:
    os.makedirs(out_dir)
except:
    pass

# Open output zone file
try:
    out_path = os.path.join(out_dir, out_file)
    out = open(out_path, "w")
except:
    print('Failed to create output file \'%s\'' % out_path)

# Load wordlist
for p in open('./wordlist', 'r'):
    wordlist.append(p.strip())

# Write out header
global count
count = 0
header_write(out)

# Permute words
for n in range(1, 4):
    permute_write(out, wordlist, n)
