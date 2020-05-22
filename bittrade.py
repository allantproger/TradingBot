#!/usr/bin/env python
# coding: utf-8

# In[13]:


import websocket,json
import dateutil.parser


# In[19]:


minutes_proc = {}
minute_candlesticks = []
current_tick = None 
previous_tick = None 
in_position = False


# In[15]:


def on_open(ws):
    print("Opened")
    
    subscribe_message = {
        "type" : "subscribe",
        "channels" : [
            {
                "name" : "ticker",
                "product_ids": [
                    "BTS-USD "      
                ]
            }
        ]
    }
        
    ws.send(json.dumps(subscribe_message))


# In[23]:


def on_message(ws, message):
    global current_tick, previous_tick
    
    previous_tick = current_tick 
    current_tick = json.loads(message)
    
    print("==== Recieved Tick ====")
    print("{} @ {}".format(current_tick['time'], current_tick['price']))
    
    tick_datetime_object = dateutil.parser.parse(current_tick['time'])
    tick_dt = tick_datetime_object.strftime("%m/%d/%Y %H:%M")
    
    if not tick_dt in minutes_proc:
        print("Starting new Candle stick")
        minutes_proc[tick_dt] =  True
        print("min_proc")
        
        if len(minute_candlesticks > 0):
            minute_candlesticks[-1]['close'] = previous_tick['price']
        
        minute_candlesticks.append({
            "minute": tick_dt,
            "open": current_tick['price'],
            "high": current_tick['price'],
            "low":  current_tick['price'],
        })
        
    if len(minute_candlesticks) > 0:
        current_candlestick = minute_candlesticks[-1]
        if current_tick['price'] > current_candlestick['high']:
            current_candlestick['high'] = current_tick['price']
        if current_tick['price'] < current_candlestick['low']:
            current_candlestick['low'] = current_tick['price']
        print("=== Candlesticks ===")
        for candlestick in minute_candlesticks:
            print(candlestick)
    #print(json.loads(messsage)) json.loads converts mes to a python dict
    
    if(len(minute_candlesticks) > 3 ):
        print(" Now Soldiers pattern can be checked")
        last_candle = minute_candlesticks[-2]
        previous_candle = minute_candlesticks[-3]
        first_candle = minute_candlesticks[-4]
        
        if (last_candle["close"] > previous_candle["close"] and previous_candle["close"] > first_candle["close"]):
            print("=== TRADE ===")
            distance = last_candle["close"] - first_candle["open"]
            profit_price = last_candle["close"] + (distance * 2)
            print("I will take profit at {}".format(profit_price))
            loss_price = first_candle("open")
            print("sell for a loss at {}".format(loss_price))
    
            if   in_position == False :
                print("== Placing order and setting in position to true ==")
                in_position = True 


# In[24]:


socket = "wss://ws-feed.pro.coinbase.com"


# In[ ]:


ws = websocket.WebSocketApp(socket, on_open = on_open, on_message = on_message)
ws.run_forever()


# In[ ]:





# In[ ]:




