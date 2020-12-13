import collections
import enum
import functools
import io
import itertools
import operator
import re
import sys

def eea(r0, r1, s0 = 1, s1 = 0, t0 = 0, t1 = 1):
    if r0 < r1:
        d, t, s = eea(r1, r0)
        return d, s, t
    elif r1 == 0:
        return r0, s0, t0
    else:
        q1 = r0 // r1
        return eea(r1, r0 - q1 * r1, s1, s0 - q1 * s1, t1, t0 - q1 * t1)

def crt(a, n, a0 = 0, n0 = 1):
    if not a:
        return a0
    a1, *ar = a
    n1, *nr = n
    ni = n0 * n1
    _, m0, m1 = eea(n0, n1)
    ai = (a0 * m1 * n1 + a1 * m0 * n0) % ni
    return crt(ar, nr, ai, ni)

def first(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    arrival_time, *busses = map(lambda d: int(d), re.findall(r'\d+', indata))
    min_wait = arrival_time
    min_wait_bus = -1
    for bus in busses:
        if (bus_wait := bus - since_last if (since_last := arrival_time % bus) else 0) < min_wait:
            min_wait, min_wait_bus = bus_wait, bus
    print("First star: {}".format(min_wait * min_wait_bus))

def second(file_name):
    with io.open(file_name, mode = 'r') as infile:
        indata = infile.read()
    _, *busses = re.findall(r'\d+|x', indata)
    bus_diff_mods = list(zip(*[(bus := int(bus_id), -diff % bus) for bus_id, diff in zip(busses, itertools.count(0)) if bus_id != 'x']))
    print("Second star: {}".format(crt(bus_diff_mods[1], bus_diff_mods[0])))

if __name__ == "__main__":
    first(sys.argv[1])
    second(sys.argv[1])