import argparse
import pandas as pd
from knowledge_graph import db
from knowledge_graph.models import Zip, Iri, Lrf

def add_iris_to_db(df):
    ''' Initially, the IRIs in the column headers are added to the database. This won't
        do anything if they are already present.
        
        Parameters
        ----------
        df - The CSV as a dataframe  
    '''
    for col in df.columns[1:]:
        exists = db.session.query(Iri).filter_by(iri=col).first()
        if not exists:
            i = Iri(iri=col)
            db.session.add(i)
            db.session.flush()
    db.session.commit()

def add_iris_to_zip(z, df, row):
    ''' Iris should be added to Zips only if they are relevant or if they are unknown,
        in which case it's assumed to affect the user.
        
        Parameters
        ----------
        z - A Zip Code Database Object
        df - The CSV as a dataframe
        row - The row from the dataframe
    '''
    print("adding zip: ", z)
    for col in df.columns[1:]:
        iri_affects = row[col]
        if iri_affects:
            i = db.session.query(Iri).filter_by(iri=col).first()
            print("Adding IRI to zip: ", i)
            z.iris.append(i)     

def main(args):
    path = args.Path
    df = pd.read_csv(path)
    df.fillna(True, inplace=True) # NaN are assumed to affect user
    print(df)
    
    add_iris_to_db(df)
    
    for index, row in df.iterrows():
        zip_code = row['zip_code']
        exists = db.session.query(Zip).filter_by(zip=zip_code).first()
        if exists:
            add_iris_to_zip(exists, df, row)
            
        if not exists:
            z = Zip(zip=zip_code)
            add_iris_to_zip(z, df, row)
            db.session.add(z)
        db.session.flush()
        
    db.session.commit()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Upload a CSV of LRF data to the database')
    parser.add_argument("-Path", type=str,
                        help='the path to the CSV file')
    args = parser.parse_args()
    main(args)