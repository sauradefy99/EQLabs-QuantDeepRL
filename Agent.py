
# coding: utf-8

# In[1]:


import keras
from keras.models import Sequential
from keras.models import load_model, Model
from keras.layers import Dense, LSTM, Flatten, Input, concatenate
from keras.optimizers import Adam
import numpy as np
import random
import utilities


# In[2]:


from collections import deque


# In[3]:


class Agent:
    def __init__(self, time_steps, feature_count, is_eval=False, model_name=""):
        self.time_steps = time_steps 
        self.feature_count = feature_count
        self.action_size = 3  #
        self.memory = deque(maxlen=256)   
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval
        
        #HYPERPARAMS
        self.gamma = 0.80   #
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = load_model("models/" + model_name + ".h5") if is_eval else self._model()
        
    def _model(self):
        #ADD DROPOUT, TRY BATCHNORM AND EXPERIMENT DIFF SHAPES
        feature_input = Input(shape=(self.time_steps, self.feature_count), name="Market_inputs")
        lstm = LSTM(32, return_sequences=True, activation="relu")(feature_input)
        flattened_features = LSTM(16, return_sequences=False, activation="relu")(lstm)
        state_input = Input(shape=(utilities.PositionStateWidth,), name="Position_inputs")
        state = Dense(8, activation="relu")(state_input)
        merged = concatenate([flattened_features, state], axis=1) #SIMPLE, CAN CHANGE
        merged = Dense(units=16, activation="relu")(merged)
        preds = Dense(self.action_size, activation="softmax", name="Actions")(merged)
        model = Model(inputs=[feature_input, state_input], outputs=preds)
        model.compile(optimizer=Adam(lr=self.learning_rate), loss="mse")
        return model
    def act(self,state):
            if not self.is_eval and np.random.rand() <= self.epsilon:
                return random.randrange(self.action_size)
            options = self.model.predict(state)
            return np.argmax(options[0])
    def expRelay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size +1 , l):
            mini_batch.append(self.memory.popleft())
            
        states0,states1,targets=[],[],[]
        for state,action,reward,next_state, done in mini_batch:
            target = reward
            if not done:
                target = reward + self.gamma*np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            states0.append(state[0])   
            states1.append(state[1])  # added position_state as a list 
            targets.append(target_f)
        self.model.fit([np.vstack(states0), np.vstack(states1)], [np.vstack(targets)], epochs=1, verbose=0)
        if self.epsilon>self.epsilon_min:
            self.epsilon*=self.epsilon_decay

