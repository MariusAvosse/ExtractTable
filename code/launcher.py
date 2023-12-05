import data2csv
import detectionTableau as dt
from PIL import Image
import argparse
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str, required=True,
	    help="path to input image")
    args = vars(ap.parse_args())
    traitement(args["image"]) 
    

def traitement(path):
    print(path)
    bounding=dt.table(path)
    im = Image.open(path)
    cords=dt.cleaning(bounding,im)
    nbcol=dt.col(cords) 
    nbline=dt.line(cords)
    tmp=data2csv.cords2data(cords,im)
    l=len(path)
    test=path[:l-3]
    test=test+'csv'
    data2csv.data2csv(test,tmp,nbcol,nbline)

if __name__ == '__main__':
    main()
