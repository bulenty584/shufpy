import argparse
from argparse import ArgumentParser
import random
import sys
import string

class Shuf:
    def __init__(self, lines, repeat, count):
        random.shuffle(lines)
        self.lines = lines
        self.repeat = repeat
        self.count = count
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == 0 or self.index == len(self.lines):
            raise StopIteration
        if self.repeat:
            result = random.choice(self.lines)
        else:
            result = self.lines[self.index]
            self.index += 1
        if self.count > 0:
            self.count -= 1
        return result
    
def outputLines(args, notKnown):
    if args.echo != None:
        if (args.input_range != None):
            sys.stdout.write("shuf.py: cannot combine -e and -i options\nTry 'shuf.py --help' for more information.\n")
            exit(1)
        if (args.input_file != None):
            args.echo.append(args.input_file)
            args.input_file = None
            while (len(notKnown) != 0):
                args.echo.append(str(notKnown[0]))
                notKnown.pop(0)     
        
        lines = [i for i in args.echo]
        return lines
    
    if (len(notKnown) > 0 and notKnown[0] != "-"):
            if (notKnown[0][0] == "-" and notKnown[0][1] == "-"):
                sys.stderr.write("""shuf.py: unrecognized option """ + str(notKnown[0]) + """\nTry 'shuf --help' for more information.\n""")
                exit(1) 
            else:
                sys.stderr.write("shuf: invalid option -- '%s'\nTry 'shuf --help' for more information.\n" % notKnown[0][1])
                exit(1)
    
    if (args.input_range != None):
        range_ = args.input_range[0].split("-")
        if (args.input_file != None):
            sys.stdout.write("""shuf.py: extra operand '%s'\nTry 'shuf.py --help' for more information.\n""" %args.input_file)
            exit(1)  
        elif (len(args.input_range) > 1):
            sys.stdout.write("shuf.py: multiple -i options specified\n")
            exit(1)
            
        elif (len(args.input_range[0].split("-")) == 1):
            sys.stdout.write("""shuf.py: invalid input range: '%s' \n""" % args.input_range[0])
            exit(1)
        elif int(args.input_range[0].split("-")[1]) + 1 < int((args.input_range[0].split("-")[0])):
            sys.stdout.write("""shuf.py: invalid input range: '%s' \n """ % args.input_range[0])
            exit(1)
        min = int(range_[0])
        max = int(range_[1])
        
        lines = []
        
        for i in range (min, max + 1):
            lines.append(str(i))
        return lines
       
    if (args.input_file == "-" or args.input_file == None):
        if (len(notKnown) == 1 and "-" in notKnown):
            sys.stderr.write("shuf.py: extra operand '-'\nTry 'shuf.py --help' for more information.\n")
            exit(1)
        elif(len(notKnown) > 0):
            return None   
        lines = [line.strip() for line in sys.stdin]
        return lines
    
    elif (args.input_file != None and args.input_file != "-"):
        try:
            with open(args.input_file, 'r') as f:
                lines = [line.strip('\n') for line in f.readlines()]
        except:
            sys.stderr.write("""shuf.py: %s: No such file or directory\n""" % args.input_file)
            exit(1)
        return lines
    
    else:
        lines = []
    
    return lines
        

def main():
    usage_msg = """Usage: shuf [OPTION]... [FILE]\n or:  shuf -e [OPTION]... [ARG]...\n or:  shuf -i LO-HI [OPTION]...\nWrite a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.

Mandatory arguments to long options are mandatory for short options too.
  -e, --echo                treat each ARG as an input line
  -i, --input-range=LO-HI   treat each number LO through HI as an input line
  -n, --head-count=COUNT    output at most COUNT lines
  -r, --repeat              output lines can be repeated
      --help     display this help and exit
"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-e", "--echo", action = "store", nargs = '*', help="Treat each command-line operand as an input line")
    parser.add_argument("-i", "--input-range", action = "append", help = "Treat each number N as an input line by reading from a file")
    parser.add_argument("-n", "--head-count", type=int, action="store", default = 0, dest = "head_count", help="Output at most COUNT lines")
    parser.add_argument("-r", "--repeat", action="store_true", dest = "repeat", help="Repeat output values by selecting with replacement")
    parser.add_argument("--help", action = "store_true", dest = "help", help = "help page")
    parser.add_argument("input_file", nargs="?", help="optional input file")
    args, notKnown = parser.parse_known_args()
        
    head_count = args.head_count     
    
    if (args.help):
        sys.stdout.write(usage_msg)
        return
    
    lines = None
    
    if (args.repeat == False):
        lines = outputLines(args, notKnown)
        
    if (args.repeat):
        lines = outputLines(args, notKnown)
            
        if (len(lines) == 0):
            sys.stderr.write("shuf.py: no lines to repeat\n")
            exit(1)
            
        if (args.head_count == 0):
            head_count = -1
        
        while(True):
            line = random.choice(lines)
            sys.stdout.write(line + '\n')
            head_count -=1
            if (head_count == 0):
                break
        return
                
                
    else:
        shuf = Shuf(lines, args.repeat, args.head_count)
        if (head_count == 0 or head_count > len(shuf.lines)):
            head_count = len(shuf.lines)
        for i in range(head_count):
            line = shuf.lines[i]
            sys.stdout.write(line + '\n')
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
            exit(2)