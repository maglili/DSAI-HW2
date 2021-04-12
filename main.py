from tools import * 


def main(train, test):

    t, test = load_data(train, test)
    model = train_model(t, test)

    x_name = ['open', 'high', 'low', 'close']
    train_last = t[-1:]
    last = train_last[x_name].values
    train_40 = t['open'][-40:].tolist()

    output = list()
    for i in range(len(test)-1):
        
        #regression 產生預測明天的y
        open_last = float(model.predict(last).ravel()[0])
        
        #送入draw_MA的dataset
        train_40.append(open_last) 
        
        #產生MA
        draw_MA = pd.DataFrame()
        draw_MA['Open'] = train_40
        draw_MA['EMA_DayByDay_1'] = np.NaN
        draw_MA['EMA_DayByDay_2'] = np.NaN
        
        
        ##
        window_size = 2
        multiplier = 2 / (window_size + 1)
        window = make_window(window_size, 0)
        EMA_anterior = draw_MA['Open'].iloc[window].mean(axis=0)
        draw_MA.iat[window_size, draw_MA.columns.get_loc('EMA_DayByDay_1')] = EMA_anterior
        for index in range(window_size+1, len(draw_MA)):
            window = make_window(window_size, index-window_size)
            EMA = (draw_MA['Open'].iloc[index-1] - EMA_anterior) * multiplier + EMA_anterior
            draw_MA.iat[index, draw_MA.columns.get_loc('EMA_DayByDay_1')] = EMA
            EMA_anterior = EMA
        #---------------
        window_size = 1
        multiplier = 2 / (window_size + 1)
        window = make_window(window_size, 0)
        EMA_anterior = draw_MA['Open'].iloc[window].mean(axis=0)
        draw_MA.iat[window_size, draw_MA.columns.get_loc('EMA_DayByDay_2')] = EMA_anterior
        for index in range(window_size+1, len(draw_MA)):
            window = make_window(window_size, index-window_size)
            EMA = (draw_MA['Open'].iloc[index-1] - EMA_anterior) * multiplier + EMA_anterior
            draw_MA.iat[index, draw_MA.columns.get_loc('EMA_DayByDay_2')] = EMA
            EMA_anterior = EMA
        
        
        #產生決策→1,0,1
        # 初始決策

        fast = draw_MA['EMA_DayByDay_1'].values[-2]
        slow = draw_MA['EMA_DayByDay_2'].values[-2]        
        
        check_past = fast-slow 

        fast = draw_MA['EMA_DayByDay_1'].values[-1]
        slow = draw_MA['EMA_DayByDay_2'].values[-1]

        check_last = fast-slow 
        
        if i == 0:
            
            if check_last >= 0 :
                output.append(1)
            elif check_last < 0 :  
                output.append(-1)
        else:
            if check_past > 0:
                if check_last < 0:
                    output.append(-1)
                else:
                    output.append(0)
            elif check_past < 0:
                if check_last > 0:
                    output.append(1)
                else:
                    output.append(0)            
        
        #獲得 明天的真實的y
        last = test.iloc[[i]][x_name].values


    return output




