#!/usr/bin/env python
# coding: utf-8

# In[26]:


import time
start_time = time.time()

# CIS*6020: Artificial Intelligence
# Assignment 2
# Student: Santosh Kumar Satapathy
# Under the guidance of Dr. Neil Bruce

# Nonogram.py

# The following functions would help us solve the nonograms provided in the examples, let's start solving!

# This function create_all_p, it takes a row/column of the nonogram as input and provides all the combinations as output that are VALID. Valid combinations are those that
# are not consecutive and blocks have white spaces between them. We feed all combinations into this function and it returns only VALID combinations
def create_all_p(p):
    p1 = []
    for i in p:
        mem = -5
        store = 1
        for j in i:
            if j-mem==1:
                store = 0
            mem = j

        if store == 1 :
            p1.append(i)
    return p1


# This functions solves the row/column by taking all the VALID combinations as input, the lengths of the blocks, the count of white spaces.
# What this function does, is it tries to fit all VALID combinations into the nonogram, it checks whether certains cells are already prefilled and then
# compares prefilled cells with our possible combinations and removes any combinations that creates conflicts with already filled nonogram.
# With the remaining combinations, it checks how many combinations are left and which cells we are certain about, whether they are black or white and then fills the cells we are certain about.

def create_final_p(p1,lengths,white,position=0,black=False,partial=-1):
    pf = [0]*(sum(lengths)+white)
    if partial != -1 :
        pf = nono[:,(a-split-1)]
    old_value = 0
    for k in range(len(p1[position])):
        if (black==True) & (p1[position][k-1] != p1[position][k]):
            pf[(p1[position][k-1]+old_value+1):(p1[position][k]+old_value)] = [-1]*((p1[position][k]+old_value)-(p1[position][k-1]+old_value+1))
        
        if partial == -1:            
            pf[(p1[position][k]+old_value):old_value+p1[position][k]+(int(lengths[k]))] = [1]*int(lengths[k])
        else:
            if p1[position][k] == partial:
                pf[(p1[position][k]+old_value):old_value+p1[position][k]+(int(lengths[k]))] = [1]*int(lengths[k])
            else:
                pf[(p1[position][k]+old_value):old_value+p1[position][k]+(int(lengths[k]))] = nono[:,(a-split-1)][(p1[position][k]+old_value):old_value+p1[position][k]+(int(lengths[k]))]
        old_value = old_value+int(lengths[k])-1
    
    if black==True:
        for i,j in enumerate(pf):
            if pf[i] == 0:
                pf[i] = -1
    return pf


# The following function is used only to calculate all the Columns of the nonogram by iterating over each column. We have an exactly similiar function for rows as well.

def calculate_c():
    # Iterate over each column
    for a in data_c.columns:
        
        # Length: Stores the length of all the Black Blocks
        lengths = [int(l) for l in data_c[a] if l != None]
        
        # Groups: Store the count of Black Blocks
        groups = len(lengths)
        
        # White: Stores the number of white cells we need to place in the column
        white = data_c_max-sum(lengths)
        
        # Opts: Create all possible combinations
        opts = combinations(range(groups+white), groups)
        p = list(opts)
        
        # Here we will call the function create_all_p to remove UNVALID combinations where Black Blocks are consecutive. 
        p1 = create_all_p(p)

        # First check, if there is only 1 combination possible, if Yes, place it in the nonogram using create_final_p function
        if len(p1) == 1:
            pf = create_final_p(p1,lengths, white, 0,True)
            nono[:,(a-split-1)] = pf

        # If there are more than 1 comibnations possible, we will try to fill only those cells that we are certain about
        else:
            
            # p1_test: Here we will store all possible combinations to compare them with already filled cells
            p1_test = []
            
            # rem: Here we will store INVALID combinations that clash with our prefilled nonogram
            rem = []
            for i in p1:
                
                # Create all possible combinations now
                pf = create_final_p([i],lengths, white, 0,True)

                # Compare these combinations with prefilled columns to check and remove clashes.
                if len([k for k in np.subtract(pf,nono[:,(a-split-1)]) if (k == -2) or (k == 2)]) > 0:
                    rem.append(i)

                if (len([k for k in np.subtract(pf,nono[:,(a-split-1)]) if k == 0]) > 0)&(i not in rem):
                    p1_test.append(i)
            
            # Store clashing combinations in rem and remove them.
            p1 = [i for i in p1 if i not in rem]

            # If there are no cells we are certain about, skip the column.
            if len(p1) == 0:
                continue;
            
            # If by performing previous step, we cannot find any valid comibination, we will try with ALL possible combinations.
            if len(p1_test) == 0:
                p1_test = p1.copy()
            
            # If only 1 VALID combination is left, fill it.
            if len(p1_test) == 1:
                pf = create_final_p(p1_test,lengths, white, 0,True)
                nono[:,(a-split-1)] = pf
                
            # If still multiple combinations can be placed without clashing with our prefilled nonogram, let's fetch cell-wise, which cells we are certain about and fill them.
            else:
                pf_temp = []
                for i in p1_test:
                    pf_temp.append(create_final_p([i],lengths, white, 0,True))

                extract = pd.DataFrame(pf_temp)
                for i in extract.columns:
                    if extract[i].nunique() != 1:
                        extract[i] = 0
                if extract.drop_duplicates().iloc[0].nunique() > 1:
                    for i in range(len(nono)):
                        if list(extract.drop_duplicates().iloc[0])[i] != 0:
                            nono[:,(a-split-1)][i] = list(extract.drop_duplicates().iloc[0])[i]
                    
                    
# Repeat the above process for all columns and all rows, as in the similiar row function below:                                  
                            
def calculate_r():

    for a in data_r.columns:

        lengths = [int(l) for l in data_r[a] if l != None]
        groups = len(lengths)
        white = data_r_max-sum(lengths)
        opts = combinations(range(groups+white), groups)
        p = list(opts)

        p1 = create_all_p(p)

        if len(p1) == 1:
            pf = create_final_p(p1,lengths,white, 0,True)
            nono[(a),:] = pf
        else:
            p1_test = []
            rem = []

            for i in p1:
                
                pf = create_final_p([i],lengths,white, 0,True)
#                 print(pf,nono[(a),:],lengths,white)
                if len([k for k in np.subtract(pf,nono[(a),:]) if (k == -2) or (k == 2)]) > 0:
                    rem.append(i)

                if (len([k for k in np.subtract(pf,nono[(a),:]) if k == 0]) > 0)&(i not in rem):
                    p1_test.append(i)

            p1 = [i for i in p1 if i not in rem]
            if len(p1) == 0:
                continue;
            if len(p1_test) == 0:
                p1_test = p1.copy()

            if len(p1_test) == 1:
                pf = create_final_p(p1_test,lengths,white, 0,True)
                nono[(a),:] = pf
                
            else:
                pf_temp = []
                for i in p1_test:
                    pf_temp.append(create_final_p([i],lengths,white, 0,True))

                extract = pd.DataFrame(pf_temp)
                for i in extract.columns:
                    if extract[i].nunique() != 1:
                        extract[i] = 0
                
                if extract.drop_duplicates().iloc[0].nunique() > 1:
                    for i in range(len(nono[0])):
#                         print("Extract")
#                         print(list(extract.drop_duplicates().iloc[0])[i])
#                         print(list(extract.drop_duplicates().iloc[0])[i] != 0)
                        if list(extract.drop_duplicates().iloc[0])[i] != 0:
                            nono[(a),:][i] = list(extract.drop_duplicates().iloc[0])[i]
            
            
# Now our functions are ready, let's import basic libraries.
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
import sys 
  
# Let's import combinations function from itertools library that will help us create all possible combinations.
from itertools import combinations

input_file = str(sys.argv[1])
# To open assignment's examples run below:
f = open(input_file, "r")
# f = open("/kaggle/input/examples/example4", "r")

data = pd.DataFrame(data=f)

# Read the input files and store them in a cleanformat in a dataframe
data[list(range(data[0].str.split('\n',expand=True).shape[1]))] = data[0].str.split('\n',expand=True)
data = data[[0]]
data[list(range(data[0].str.split(' ',expand=True).shape[1]))] = data[0].str.split(' ',expand=True)

data = data.transpose()

#Breaking point of file for rows and columns data
split = 0

for i in data.columns:
    if data[i][0]=='':
        break;
    split+=1
        
# Split into two dataframes for rows and columns
data_r = data.iloc[:,:split]
data_c = data.iloc[:,split+1:]

# Lengths of row and columns
data_r_max = len(data_c.columns)
data_c_max = len(data_r.columns)

# Create an empty nonogram
nono = np.zeros((data_c_max,data_r_max))


# Until the nonogram is fully filled, keep calling calculate_r and calculate_c that interates over each row and column to fill it.

while True if 0 in np.unique(nono) else False:
    nono_check = nono.copy()
    calculate_r()
    calculate_c()
    
    # See if after each iteration we have filled more cells, if not, we might be stuck in an infinite loop and not solving further.
    # In that case, break the loop and print partially solved nonogram.
    try:
        if np.unique(nono_check==nono)==True:
            break;
    except:
        pass
    
# Print the nonogram
plt.imshow(nono,cmap='gray', vmin=-1, vmax=1)

from PIL import Image  
img = Image.fromarray(np.uint8(nono), 'L')
img.save(input_file+'.png')
img.show()

print("--- " + input_file + " solved in: %s SECONDS ---" % ((time.time() - start_time)))


# In[ ]:





# In[ ]:





# In[ ]:




