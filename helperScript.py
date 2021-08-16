import pandas as pd
import json

def jsonify_it(filename):
    kl = pd.read_csv(filename).to_json(orient="records")
    with open("quotes.json", "w") as outfile:
        outfile.write(kl)

def disintegrate(chunksize=100000,filename=""):
    for i,chunk in enumerate(pd.read_csv(filename, chunksize=chunksize)):
        chunk.to_csv('quotes/quotes_{}.csv'.format(i), index=False)

if __name__ == "__main__":
    jsonify_it("quotes.csv")
    disintegrate(chunksize=10000,filename="quotes.csv")
