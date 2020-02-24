
# coding: utf-8

# In[1]:


# This file has some common constant variables which are used repeatedly
#
#
#model params
PositionStateWidth = 3 #3 positions buy hold and sell
MAXCONTRACTS = 200
ACTIONZERO = 1 # WILL SEE IF THIS IS NEEDED LATER - basically says Position = 0 means exit current position, instead of keep current position and do nothing
IGNORE_EOD_ACTIVATION = True #no new position at open of next day


COMMISSION = 0.2

POINTVALUE = -1000.0

Debug=True


# In[2]:


#################################################################


# In[3]:


#We also define common functions that we will be using again

import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler  # save this scaler to model directory
from sklearn.externals import joblib


# In[4]:


scaler = MinMaxScaler(feature_range=(0.1,1))


# In[5]:


def make_timesteps(inArr, L=2):
    if L==1:
        return inArr.reshape(inArr.shape[0],1,inArr.shape[1])
    
    a = np.vstack((inArr[-L+1:],inArr))
    m,n = a.shape
    s0,s1 = a.strides
    nd0 = m - L + 1 #Length of 3D array along its axis = 0
    strided = np.lib.stride_tricks.as_strided
    return strided(a[L-1:],shape=(nd0,L,n),strides=(s0,-s0,s1))[L-1:]
    


# In[6]:


import time, datetime


# In[7]:


class Timer(object):
    def __init__(self,total):
        self.start = datetime.datetime.now()
        self.total = total
        
    def remains(self,done):
        now = datetime.datetime.now()
        left = (self.total - done)*(now-self.start)/max(done,1)
        secs = int(left.total_seconds())
        if secs>3600:
            return "{0:.2f} hours ".format(secs/360)
        else:
            return "{0:.2f} minutes ".format(secs/60)
        
    


# In[8]:


def formatPrice(n):
    return ("-$" if n<0 else "$")+"{0:.2f}".format(abs(n))


# In[9]:


def getStockDataVec(key, timesteps, model_name="", dayTrading=False):

    data = np.genfromtxt("data/"+ key + ".csv",delimiter=';',skip_header=1,  dtype="float_")[:,1:]  
    if Debug:
        print("func Datashape: ", data.shape)
    prices = data[:,0]   # column 0 after date 
    
    
    startFeatures = 1  # normal mode
    if dayTrading:
        eod = data[:,1] # column 1 after price (or some not used feature if not )
        startFeatures = 2
    else:
        eod = np.zeros(len(data), dtype=int)
    eod[len(data)-1] = 1  
    
    features = data[:,startFeatures:] # price removed, column 1 or 2 based to dayTrading
    
    scaler = MinMaxScaler(feature_range=(0.1, 1)) 
    if model_name=="":  # expect training
        scaler.fit(features)   
        # save scaler for later usage, if out of sample set read together with model .h5
        joblib.dump(scaler, "models/"  +key+ "_skaler.sav")
    else: # use existing scaler 
        scaler = joblib.load("models/"  +model_name.split("_")[0]+ "_skaler.sav") # split to cut number of epochs away 

        
    scaledFeatures = scaler.transform(features)
    
    features3D = make_timesteps(scaledFeatures, timesteps) # non full feature sets removed 
    prices = prices[timesteps-1:]  # cut as well
    eod = eod[timesteps-1:] ## 
    
    assert features3D.shape[0] != prices.shape, "Shape error"
    
    if Debug:
        print("func Features shape: ",features3D.shape, prices.shape)
    
    return prices, features3D, eod


# In[10]:


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# In[11]:


def getState(data, t):
    return data[t].reshape(1, data[t].shape[0], data[t].shape[1]) 


# In[12]:


def getNextPositionState(action, position_state, prev_price, price, eod, prev_eod):  # or think it like current  price and  next_price  !!!!!!!!!!!!!!!!!!!!!!
# position state [Long,Short, Pnl]   # Flat position incorporated if long and short are both 0
# by defining the position state this way, we are integrating the quantity bought 
# instead of just buying the same constant quantity, we are buying number of contracts present in position_state[0]
    
    price_diff = price - prev_price
    immediate_reward = 0.0
    full_pnl = 0.0
    comission_count = 0
    
    if IGNORE_EOD_ACTIVATION and prev_eod == 1:  # no new state (should be okay after last bars flat set, BUT set anyway here again
        #print ("prev eod, should be 0", position_state[2])
        position_state[0] = 0
        position_state[1] = 0
        position_state[2] = 0
        #position_state[3] = 0.0
        return position_state, 0.0, 0.0
    
    if action == 0: 
        full_pnl = position_state[2] - position_state[0]*COMMISSION - position_state[1]*COMMISSION  # either one [1],[2] or both are zero 
        # immediate_reward = 0.0
        position_state[0] = 0
        position_state[1] = 0
        position_state[2] = 0
        #position_state[3] = 0.0
        return  position_state, immediate_reward, full_pnl   # 
        
        

    LC = int(position_state[0])  # Long, how many contracts, stock_count or ..
    SC = int(position_state[1])  # Short, how many ..
    F = (LC == 0 and SC == 0) # to simple boolean
    
    
    #prev_state = position_state[1] 
    
    if action == 1:  # buy
        if SC > 0:
            full_pnl = position_state[2] - SC*COMMISSION 
            position_state[2] = price_diff - COMMISSION # one buy
        if LC < MAXCONTRACTS:  
            immediate_reward = price_diff - COMMISSION #one more buy
            position_state[0] += 1 
            if LC > 0: 
                position_state[2] += (LC+1)*price_diff
                
        if LC ==MAXCONTRACTS:
            position_state[2] += LC*price_diff   # and no immediate reward any more 
        if F : 
            position_state[0] = 1
            # position_state[2] == 0 
            position_state[2] = price_diff - COMMISSION
            
        #position_state[0] = 0
        position_state[1] = 0
        # position_state[3]  # should be calculated above to all possibilities
        
    if action == 2:  # sell
        if LC > 0:
            full_pnl = position_state[2] - LC*COMMISSION 
            position_state[2] = -1.0*price_diff - COMMISSION # one buy
        if SC < MAXCONTRACTS:  
            immediate_reward = -1.0*price_diff - COMMISSION # one buy, more 
            position_state[1] += 1 
            if SC > 0: # SC can't be positive then, no need to worry next at that point ,, CHECK LC == 0 and 
                position_state[2] += (LC+1)*-1*price_diff
        if SC == MAXCONTRACTS:
            position_state[2] += -1.0*SC*price_diff   # and no immediate reward any more 
        if F: 
            # immediate_reward = price_diff 
            position_state[1] = 1
            # position_state[2] = 0 
            position_state[2] = -1.0*price_diff - COMMISSION
            
        #position_state[0] = 0
        position_state[0] = 0
        # position_state[3] 
   
    
    if eod == 1:    
        full_pnl = full_pnl - position_state[0]*COMMISSION - position_state[1]*COMMISSION + immediate_reward # either one [1],[2] or both are zero 
        
        position_state[0] = 0
        position_state[1] = 0
        position_state[2] = 0.0
        return  position_state, immediate_reward, full_pnl    
    
    return  position_state, immediate_reward, full_pnl   



##############################

