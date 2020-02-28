# File generation

This script takes any text file and generates permutations based on the arguments passed in the command line.

Running `py input.py --var ZAA --var ZAB --range "100-200" --range "3-4" --var "ZAC"` would replace every occurence of `ZAA`, `ZAB` and `ZAC` in the template file.

The ranges should be specified in the same order as the variables are listed: in the example, the range `"100-200"` applies to `ZAA`, the range `"3-4"` applies to `ZAB` and any remaining variables (`ZAC`), as no more ranges were specified.

The number of steps can be specified with `--step`. The default is 2, meaning that for the range of `"100-200"`, a file is generated for `ZAC`=100, 150, 200.