import sys
from Payment import Payment

def main(args):
    input_file = args[1]
    payments = process_input(file=input_file)



def process_input(file):
    try:
        f = open(file, 'rb')
    except IOError:
        print "Could not read file:", file
        sys.exit()
    with f:
        lines = f.readlines()
        print lines



if __name__ == "__main__":
     main(args=sys.argv)