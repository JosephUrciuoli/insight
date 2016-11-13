import filecmp


def verify_files():
    files = ["output1.txt","output2.txt","output3.txt","added_feature.txt"]
    for file in files:
        print "VERIFYING " + file
        comp = filecmp.cmp("tests/test-1-paymo-trans/paymo_output/" + file,
                           "tests/test-1-paymo-trans/verified_output/" + file)
        if comp:
            print file + " VERIFIED"
        else:
            print file + "NOT VERIFIED"


if __name__ == '__main__':
    verify_files()