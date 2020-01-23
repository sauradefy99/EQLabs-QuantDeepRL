
# coding: utf-8

# In[1]:


from utilities import *
from Agent import *
import matplotlib.pyplot as plt


# In[2]:


import matplotlib.pyplot as plt


# In[3]:


import Agent
def main(stock_name,episode_count=1000,timesteps=4):
    dayTrading=False
    if stock_name[-1:] == 'D': #If datafile ends with D then daytrading
        dayTrading = True
    
    batch_size = 32 #also check memory length of agent replay memory
    prices,market_data,eod = getStockDataVec(stock_name, timesteps, dayTrading=dayTrading)
    agent = Agent.Agent(timesteps,market_data.shape[2])
    l = len(prices) - 1
    
    timer = Timer(episode_count)
    if Debug:
        print("DataLength: ", l)
        print("Features: ", market_data.shape[2])
        print("Timesteps to use: ", market_data.shape[1])
        
    pnl_track = []
    
    position_state = np.zeros(utilities.PositionStateWidth).reshape(1,utilities.PositionStateWidth) 
    best_profit = 0.0
    
    for e in range(episode_count + 1):
        if (Debug):
            print("Episode " + str(e) + "/" + str(episode_count))
            
        market_state = getState(market_data, 0)
        position_state = np.zeros(utilities.PositionStateWidth).reshape(1,utilities.PositionStateWidth)
        total_profit = 0
        agent.inventory= []
        state = [market_state, position_state]
        
        for t in range(l):
            action = agent.act(state)
            
            next_market_state = getState(market_data, t + 1)
            reward = 0
            next_position_state, immediate_reward, PnL = getNextPositionState(action, state[1][0], prices[t], prices[t+1], eod[t+1], eod[t] ) 
            
            #NOVEL APPROACH - REWARD HAS AUGMENTED REWARD(IMMEDIATE) AS WELL AS LONG TERM REWARD (PNL)
            reward = immediate_reward + PnL
            
            #TRY WITH 
            #reward = max(reward,0)
            total_profit+=PnL
            
            done = True if t==l-1 else False
            next_state = [next_market_state, next_position_state.reshape(1,utilities.PositionStateWidth)]
            agent.memory.append((state, action, reward, next_state, done))
            state = next_state
            
            if done:
                #print("--------------------------------")
                print("Total Profit (Points) : {0:.4f}".format(total_profit))
                print ("Training left: ", timer.remains(e+1))
                print("--------------------------------")
                pnl_track.append(total_profit) 
            
            if len(agent.memory) > batch_size:
                agent.expRelay(batch_size)
                
        if e % 100 == 0 or total_profit > best_profit:
            agent.model.save("models/" + stock_name + "_" + str(e) + ".h5")
            best_profit = total_profit
            
    agent.model.save("models/" + stock_name + "_" + str(e) + ".h5") 
    plt.plot(pnl_track)
    plt.xlabel('Episode')
    plt.ylabel('Profit')
    plt.show()
    


# In[8]:


### Terminal/Command Line call
if __name__ == '__main__':
    import sys
    import Agent
    import utilities
    import matplotlib.pyplot as plt
    
    if len(sys.argv) <= 2:
        print("Usage: python train.py [stockfile] [episodes] [timesteps] ")
        exit(1)
    stock_name = sys.argv[1]
       
    episode_count = 1000
    timesteps = 4

    if len(sys.argv) >= 3:
        episode_count = int(sys.argv[2])
        
    if len(sys.argv) >= 4:
        timesteps = max(int(sys.argv[3]), 1)
    
    main(stock_name, episode_count, timesteps)

