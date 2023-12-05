import launcher
import argparse
from os import walk
import filecmp
import platform


def cmp(new,attendus):
    b=filecmp.cmp(new,attendus,False)
    return b
            
def main():
    print(platform.system())
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--directory", type=str, required=True,
	    help="path to input image")
    ap.add_argument("-a", "--attendus", type=str, required=True)
    args = vars(ap.parse_args())
    listeFichiers = []
    for (repertoire, sousRepertoires, fichiers) in walk(args["directory"]):
        listeFichiers.extend(fichiers)
    n=0
    r=0
    if(platform.system()!="Windows"):
        slash="/"
    else:
        slash="\\"
    for f in fichiers:
        l=len(f)
        if(f[l-4:]!=".csv"):
            n+=1
            launcher.traitement(args["directory"]+slash+f)
            f=f[:l-3]
            f=f+"csv"

            if cmp(args["directory"]+slash+f,args["attendus"]+slash+f):
                r+=1
                print(f)
    print(r)
    print("/")
    print(n)
    



    

if __name__ == '__main__':
    main()