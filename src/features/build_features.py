import pathlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(train_path):
    train=pd.read_csv(train_path)
    return train


def remove_columns(column,train):
    train=train.drop(columns=column)
    return train

def scaling(train):
    scaler=StandardScaler()
    train_scaled=scaler.fit_transform(train)
    return train_scaled

def splitting(train_scaled):
    df=pd.DataFrame(train_scaled)
    x_train=df.iloc[:,:-1]
    y_train=df.iloc[:,-1]
    return x_train,y_train

def save_data(x_train,y_train,path):
    x_train.to_csv(path+'/x_train.csv',index=False)
    y_train.to_csv(path+'/y_train.csv',index=False)

def main():
    curr_dir=pathlib.Path(__file__)
    parent=curr_dir.parent.parent.parent
    train_path=parent.as_posix()+'/data/interim/train.csv'
    train=load_data(train_path)
    column='Date'
    train=remove_columns(column,train)
    train_scaled=scaling(train)
    x_train,y_train=splitting(train_scaled)
    path=parent.as_posix()+'/data/processed/'
    save_data(x_train,y_train,path)

if __name__=='__main__':
    main()
