import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import cv2
import argparse
import time

parser = argparse.ArgumentParser(description= 'Generate images from .ms files')
parser.add_argument('-pref', type=str, help= '.ms file prefix', required=True)
parser.add_argument('-nHap', type=int, help= 'Number of haplotypes', required=True)
parser.add_argument('-subFolder', type=str, help= 'Name of the subfolder', required=True)
parser.add_argument('-n', type=int, help= 'Number of .ms files of the chosen class', required=True)
parser.add_argument('-start', type=int, help= 'Start number of .ms files', required=True)
parser.add_argument('-out', type=str, help= 'Output filename', required=True)

args = parser.parse_args()


# In[40]:


val = args.pref
nS = args.nHap
num_ = args.n
subf = args.subFolder
strt = args.start




# In[33]:

path1 = "./Datasets"


######


def image_gen(num_text_file, num_strands, window_length, num_stride):
    
        
    path = path1 + "/"
    path+= subf + "/" + val + "_"
    path+= str(num_text_file)+".ms"
    
    with open(path, 'r') as file:
        text = file.readlines()
    if len(text) == 0:
        return []
    elif text[2][:20] == 'trajectory too bigly':
        return []
    segsites = text[5][11:-2]

    strands = num_strands
    stride = num_stride

    Sites = [float(segsites[x*9 : x*9+8])for x in range((len(segsites)+1)//9)]
    data = np.zeros((strands, len(Sites)))
    for a in range(strands):
        binary = text[a+6][:-2]
        for b in range(len(binary)):
            data[a][b]= int(binary[b])
    Dataset = pd.DataFrame(data)


    Dataset.columns = Sites
    
    dataset = []
    sites = []
    
    for col_ in range(Dataset.shape[1]):
        col1 = list(Dataset.iloc[:, col_])
        
        if sum(col1) >2 and sum(col1) <= nS-2:
            dataset.append(col1)
            sites.append(Sites[col_])
            
    dataset = pd.DataFrame(dataset)
    dataset = dataset.T
    
    dataset.columns = sites
    
    #print(len(sites))

    
    
    err = float('inf')
    idx= None
    for pos in sites:
        error = abs(pos-0.5)
        if error<err:
            err = error
            idx = sites.index(pos)

    if idx<250 or len(sites) -idx < 250:
        return []


    window = window_length
    data_range = 500
    #print(data_range)
    
    
    DF = dataset.iloc[:, idx-data_range//2:idx+data_range//2]
    
    all_cols = []

    all_mids = []

    d = 0
    
    while 1:

        if d*stride+ window >= data_range:
            break
    
    
        df = DF.iloc[:, d*stride: d*stride+ window ]
        
        #print(df.shape)
        
        reref = []
        
        for col in range(df.shape[1]):
            lst = np.array(df.iloc[:, col])
            sum_ = np.sum(lst)
            if sum_ > int(df.shape[0]/2):
                lst[lst == 1] =2
                lst[lst == 0] =1
                lst[lst == 2] =0
                
                reref.append(list(lst))
            else:
                reref.append(list(lst))
                
        
        reref_df = pd.DataFrame(reref).T
        
        #print(reref_df.shape)
        
        reref_aligned = [list(reref_df.iloc[row, :]) for row in range(reref_df.shape[0])]
            
        column = list(np.linalg.norm(reref_aligned,axis=1, ord=1))
        
        column.sort()
        
        all_cols.append(column)

        d+=1
    
    cols_DF = pd.DataFrame(all_cols).T
    
    img =np.asmatrix(cols_DF)
    
    return img


images = []

counter = strt
element_counter = 0

while counter < strt+num_:
    
    image = image_gen(num_text_file = counter ,num_strands= nS, window_length=25, num_stride=2)
    
    counter+=1

    if len(image)==0:
        print('fail')
    
    elif len(image) != 0:
        
        images.append(image)
        element_counter+=1
        print(element_counter, counter-1)     
    else:
        print('fail')






np.save('./Image_datasets/' + args.out + '.npy', np.array(images))
print(f'Number of images: {np.array(images).shape[0]}')
