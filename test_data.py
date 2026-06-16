import pandas as pd
import random
from datetime import datetime, timedelta

def generate_test_data():
    random.seed(42)
    
    dates = []
    types = []
    opponents = []
    goods = []
    amounts = []
    payment_methods = []
    
    categories = ['餐饮美食', '交通出行', '购物消费', '娱乐休闲', '生活服务', '医疗健康']
    merchants = ['美团外卖', '滴滴出行', '淘宝', '微信支付-腾讯视频', '水电费', '药店', '超市', '餐厅', '便利店']
    
    start_date = datetime(2024, 1, 1)
    for i in range(500):
        date = start_date + timedelta(days=random.randint(0, 364))
        dates.append(date)
        
        if random.random() > 0.1:
            types.append(random.choice(categories))
            amounts.append(-random.uniform(10, 500))
        else:
            types.append('转账')
            amounts.append(random.uniform(100, 5000))
        
        opponents.append(random.choice(merchants))
        goods.append(f'消费-{types[-1]}')
        payment_methods.append(random.choice(['微信支付', '银行卡', '零钱']))
    
    df = pd.DataFrame({
        '交易时间': dates,
        '交易类型': types,
        '交易对方': opponents,
        '商品': goods,
        '金额（元）': amounts,
        '支付方式': payment_methods
    })
    
    df.to_excel('organFile/test_bill.xlsx', index=False)
    print("测试数据生成成功")

if __name__ == '__main__':
    generate_test_data()