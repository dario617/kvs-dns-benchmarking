import argparse
from os import listdir

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Read zone file names and append them to configuration file using the server's format")
  parser.add_argument("directory", type=str, help="Directory containing the zone files")
  parser.add_argument("server", type=str, help="Server type: bind, nsd, knot, pdns")
  parser.add_argument("fileConf", type=str, help="Output file to append zones")
  parser.add_argument("zonelist", type=str, help="Available zone list", default="zonelist")
  args = parser.parse_args()

  zonelist = open(args.zonelist)
  zones = zonelist.readlines()

  with open(args.fileConf, "a") as conf:
    template = ""
    if args.server == "bind":
      template = "zone \"{0}\" {{ file \"{1}\"; type master; }};\n"
    elif args.server == "knot":
      template = "  - domain: \"{0}\"\n    file: \"{1}\"\n"
    elif args.server == "nsd":
      template = "zone:\n  name: \"{0}\"\n  zonefile: \"{1}\"\n" 
    elif args.server == "pdns":
      print("Not yet implemented.")
      exit(0)
    else:
      print("Not a valid server. Options are bind, knot, nsd")
      exit(1)
    
    for z in zones:
      conf.write(template.format(z, args.directory+"/"+z+".zone"))