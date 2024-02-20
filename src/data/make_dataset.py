import pathlib
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(path):
    df=pd.read_csv(path)
    return df

def split(df):
    train,test=train_test_split(df,test_size=0.2,random_state=23)
    return train,test

def save_data(train,test,path):
    train.to_csv(path+'/train.csv',index=False)
    test.to_csv(path+'/test.csv',index=False)

def main():
    curr_dir=pathlib.Path(__file__)
    parent=curr_dir.parent.parent.parent
    data_path=parent.as_posix()+'/data/raw/zomato.csv'
    df=load_data(data_path)
    paramfile=parent.as_posix()+'/params.yaml'
    train,test=split(df)
    save_path=parent.as_posix()+'/data/interim/'
    save_data(train,test,save_path)

if __name__=='__main__':
    main()
