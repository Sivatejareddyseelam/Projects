from scipy.io import arff
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from keras.models import Sequential
from keras.layers import Dense
content1="1year.arff"
content2="2year.arff"
content3="3year.arff"
content4="4year.arff"
content5="5year.arff"
content=[content1,content2,content3,content4,content5]
train_acc=[]
test_acc=[]
for i in content:
    data,meta=arff.loadarff(i)
    df=pd.DataFrame(data)

    a=df.loc[df.shape[0]-1,"class"]
    b=df.loc[0,"class"]
    c=0
    for i in range(df.shape[0]):
        if df.loc[i,"class"]==a:
            df.loc[i,"class"]=0
        if df.loc[i,"class"]==b:
            df.loc[i,"class"]=1

    df1=df.drop(columns=['Attr37','Attr21'])
    df1.fillna(0, inplace=True)
    x=df1.loc[:,df1.columns !="class"]
    y=df1.loc[:,df1.columns=="class"]

    s=SMOTE(random_state=0)
    df_train=df1.sample(frac=0.7,random_state=0)
    x_train= df_train.loc[:, df_train.columns != 'class']
    y_train= df_train.loc[:, df_train.columns == 'class']
    x_test=x.loc[~x.index.isin(x_train.index)]
    y_test=y.loc[~y.index.isin(y_train.index)]
    #over smapling and balanced the datasets.
    columns=x_train.columns
    s_data_x_tra,s_data_y_tra=s.fit_sample(x_train,y_train)
    s_data_x_train=pd.DataFrame(data=s_data_x_tra,columns=columns)
    s_data_y_train=pd.DataFrame(data=s_data_y_tra,columns=["class"])
    model=Sequential()
    model.add(Dense(s_data_x_train.shape[0],input_dim=s_data_x_train.shape[1],activation='relu'))
    model.add(Dense(2300,activation='relu'))
    model.add(Dense(500,activation='relu'))
    model.add(Dense(125,activation='relu'))
    model.add(Dense(31,activation='relu'))
    model.add(Dense(10,activation='relu'))
    model.add(Dense(1,activation='softmax'))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
    model.fit(s_data_x_train,s_data_y_train,epochs=5,batch_size=200,verbose=2)
    scores=model.evaluate(s_data_x_train,s_data_y_train)
    z_train=model.predict(s_data_x_train)

    c_train=0
    for i in range(z_train.shape[0]):
        if s_data_y_train[i]!=z_train[i]:
            c_train=c_train+1
    train_acc.append(100-(100*(c_train/z_train.shape[0])))
    z_test=model.predict(x_test)
    c_test=0
    for i in range(z_test.shape[0]):
        if y_test[i]!=z_test[i]:
            c_test=c_test+1
    test_acc.append(100-(100*(c_test/z_test.shape[0])))
print(train_acc)
print(test_acc)
