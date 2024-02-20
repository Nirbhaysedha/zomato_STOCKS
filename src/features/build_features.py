import pathlib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(train_path):
    train=pd.read_csv(train_path)
    return train


def remove_columns(train):
    train=train.drop(columns='Date')
    return train

def rename_f(df):
    df.rename(columns={'Adj Close': 'Adj_Close'},inplace=True)
    return df

def splitting(train_scaled):
    df=pd.DataFrame(train_scaled)
    x_train=df.iloc[:,:-1]
    y_train=df.iloc[:,-1]
    return x_train,y_train

def save_data(x_train,y_train,path):
    x_train.to_csv(path+'/x_train.csv',index=False)
    y_train.to_csv(path+'/y_train.csv',index=False)

def infrence_feature(df):
    data=load_data(df)
    return data

def test_feature(test_path,save_path):
    df=load_data(test_path)
    data=remove_columns(df)
    x_test,y_test=splitting(data)
    x_test.to_csv(save_path+'/x_test.csv',index=False)
    y_test.to_csv(save_path+'/y_test.csv',index=False)

def main():
    curr_dir=pathlib.Path(__file__)
    parent=curr_dir.parent.parent.parent
    train_path=parent.as_posix()+'/data/interim/train.csv'
    train=load_data(train_path)
    trainr=remove_columns(train)
    df=rename_f(trainr)
    x_train,y_train=splitting(df)
    path=parent.as_posix()+'/data/processed/'
    save_data(x_train,y_train,path)

    test_path=parent.as_posix()+'/data/interim/test.csv'
    test_feature(test_path,path)



if __name__=='__main__':
    main()
