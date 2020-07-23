import argparse
import numpy as np

def parseSec(name):
  """
  Results as in miliseconds
  """
  if name == "nsec":
    return 1e-6
  elif name == "msec":
    return 1
  elif name == "sec":
    return 1e3

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Read response times as 0 msec and compute total stats")
  parser.add_argument("f", type=str, help="File to read response times")
  parser.add_argument('-o', "--output_file", help="Optional name for output", default="TimeStats.log")
  args = parser.parse_args()

  tmp = []
  with open(args.f) as f:
    print("Reading...")
    for line in f:
      vals = line.strip().split(" ")
      if len(vals) != 2:
        continue
      tmp.append(float(vals[0])*parseSec(vals[1]))

  total = np.array(tmp, dtype=np.float32)

  with open(args.output_file, "w") as f:
    f.write("Median {:f} msec\n".format(np.median(total)))
    f.write("Average {:f} msec\n".format(np.mean(total)))
    f.write("Std {:f} msec\n".format(np.std(total)))
    f.write("Variance {:f} msec\n".format(np.var(total)))
  print("Done")