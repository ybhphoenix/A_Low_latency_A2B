from os import system, popen
import sys
PATH = "./test_res.txt"
open(PATH, 'w').close() # clear file
cur = ""
res = ""

VERBOSE_COMPILE = True
REDIRECT = ""
MAX_ORDER = 20
ITERATIONS = 100
rng=2




PARAM_MAKE = " RUNS="+str(ITERATIONS)+" "


if not VERBOSE_COMPILE:
	REDIRECT=">/dev/null"
with open(PATH,'a') as f:
  for width in range(8, 33, 8):
    for i in range(1, MAX_ORDER+1):
      print("Compiling for masking of order", i,"and rng", rng)
      system("make clean > /dev/null && make main ORDER="+str(i)+" WIDTH="+str(width)+PARAM_MAKE+REDIRECT)
      print("Running tests...", end ='')
      sys.stdout.flush()
      cur = popen("./main").read()
      print("Writing to "+PATH+" ...")
      f.write(cur)
      res += cur
      print(cur)
      print("Done.")
