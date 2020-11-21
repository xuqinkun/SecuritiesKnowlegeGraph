import tushare as ts

token = None
with open("../token") as f:
    token = f.readline()

print(token)
ts.set_token(token)
pro = ts.pro_api()

df = pro.daily(trade_date='20200325')
print(df.head())

df = pro.query('trade_cal', exchange='', start_date='20180901', end_date='20181001',
               fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
