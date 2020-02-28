import os
import re
import argparse
import math
from collections import defaultdict
import itertools
from pprint import pprint

parser = argparse.ArgumentParser(
    description="Generate a range of numbers for each variable."
)
parser.add_argument("--var", action="append", nargs="+")
parser.add_argument("--range", action="append", nargs="+")
parser.add_argument("--steps", action="append", nargs="+")
args = parser.parse_args()


def invalidStr(x, format):
    return "{} is not valid. Must be in the format {}".format(x, format)


def validate():
    def validRange(r):
        mid = r.find("-")
        n1 = int(r[:mid])
        n2 = int(r[mid + 1 :])
        return mid >= 0 and n1 < n2

    formats = {"var": "ZXX", "range": "min-max", "steps": "[integer]"}
    varLength = len(formats["var"])

    checks = {
        "var": lambda v: v[0] == "Z" and len(v) == varLength,
        "steps": lambda s: abs(int(s)) > 0,
        "range": lambda r: validRange(r),
    }

    for key in vars(args):
        try:
            for arg in vars(args)[key]:
                valid = checks[key](arg[0])
                if not valid:
                    print("\n\nInvalid argument, {}: {}\n\n".format(key, arg[0]))
                    raise ValueError(invalidStr(arg, formats[key]))
        except TypeError:
            pass


validate()


def getRanges():
    ranges = [r[0] for r in vars(args)["range"]]
    variables = [v for v in vars(args)["var"]]

    steps = [2]
    if not vars(args)["steps"] is None:
        steps = [int(s) for s in vars(args)["steps"]]

    matched = []
    for i, v in enumerate(variables):
        currentRange = ranges[min(i, len(ranges) - 1)]
        currentStep = steps[min(i, len(steps) - 1)]
        r = [int(n) for n in currentRange.split("-")]
        matched.append((v, r, currentStep))

    d = defaultdict(list)

    for var in matched:
        varName = var[0][0]
        stepSize = math.ceil((var[1][1] - var[1][0]) / var[2])
        r = list(range(var[1][0], var[1][1] + 1, stepSize))
        d[varName] = r

    return dict(d)


ranges = getRanges()
variables = list(ranges.keys())
combinations = list(itertools.product(*ranges.values()))


print("\n\nParametric input file generation\n")
here = os.getcwd()

with open("template.txt", "r") as template:
    templateText = template.read()
    print(templateText)
    for comb in combinations:
        print("\n\n", comb)
        modified = templateText
        for i, v in enumerate(variables):
            modified = modified.replace(v, str(comb[i]))
        print(modified)
        outFileName = "-".join([str(c) for c in comb])
        with open("{}.txt".format(outFileName), "w") as out:
            out.write(modified)

