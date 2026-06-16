import pandas as pd
import os

def detect_bill_type(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        
        first_row = str(df.iloc[0, 0]).strip() if not df.empty else ""
        second_row = str(df.iloc[1, 0]).strip() if len(df) > 1 else ""
        
        if "微信支付" in first_row or "微信账单" in first_row:
            return "wechat"
        elif "支付宝" in first_row or "alipay" in first_row.lower():
            return "alipay"
        elif "交易时间" in second_row and "交易类型" in str(df.iloc[1, 1]):
            if "金额（元）" in str(df.iloc[1, :].values):
                return "wechat"
            elif "收/支" in str(df.iloc[1, :].values):
                return "alipay"
        
        return None
    except Exception as e:
        return None

def parse_wechat_bill(file_path):
    try:
        df = pd.read_excel(file_path, header=1)
        
        columns = df.columns.tolist()
        rename_dict = {}
        for col in columns:
            if '交易时间' in str(col):
                rename_dict[col] = '交易时间'
            elif '交易类型' in str(col):
                rename_dict[col] = '交易类型'
            elif '交易对方' in str(col):
                rename_dict[col] = '交易对方'
            elif '商品' in str(col):
                rename_dict[col] = '商品'
            elif '金额' in str(col) and '元' in str(col):
                rename_dict[col] = '金额'
            elif '支付方式' in str(col):
                rename_dict[col] = '支付方式'
        
        df = df.rename(columns=rename_dict)
        
        required_cols = ['交易时间', '交易类型', '交易对方', '金额']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"缺少必要列: {col}")
        
        df['金额'] = pd.to_numeric(df['金额'], errors='coerce')
        df['交易时间'] = pd.to_datetime(df['交易时间'], errors='coerce')
        
        df = df.dropna(subset=['交易时间', '金额'])
        
        df['收支类型'] = df['金额'].apply(lambda x: '支出' if x < 0 else '收入')
        df['金额'] = df['金额'].abs()
        
        return df
    except Exception as e:
        raise ValueError(f"解析微信账单失败: {str(e)}")

def parse_alipay_bill(file_path):
    try:
        df = pd.read_excel(file_path, header=1)
        
        columns = df.columns.tolist()
        rename_dict = {}
        for col in columns:
            if '交易时间' in str(col):
                rename_dict[col] = '交易时间'
            elif '交易类型' in str(col):
                rename_dict[col] = '交易类型'
            elif '交易对方' in str(col):
                rename_dict[col] = '交易对方'
            elif '商品说明' in str(col):
                rename_dict[col] = '商品'
            elif '金额' in str(col) and '元' not in str(col):
                rename_dict[col] = '金额'
            elif '收/支' in str(col):
                rename_dict[col] = '收支类型'
        
        df = df.rename(columns=rename_dict)
        
        required_cols = ['交易时间', '交易类型', '交易对方', '金额', '收支类型']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"缺少必要列: {col}")
        
        df['金额'] = pd.to_numeric(df['金额'], errors='coerce')
        df['交易时间'] = pd.to_datetime(df['交易时间'], errors='coerce')
        
        df = df.dropna(subset=['交易时间', '金额'])
        
        return df
    except Exception as e:
        raise ValueError(f"解析支付宝账单失败: {str(e)}")

def parse_bill(file_path):
    bill_type = detect_bill_type(file_path)
    
    if bill_type == 'wechat':
        return parse_wechat_bill(file_path), '微信'
    elif bill_type == 'alipay':
        return parse_alipay_bill(file_path), '支付宝'
    else:
        raise ValueError("无法识别账单类型，请确保是微信或支付宝账单")

def get_available_files(folder_path):
    files = []
    if os.path.exists(folder_path):
        for f in os.listdir(folder_path):
            if f.lower().endswith('.xlsx') or f.lower().endswith('.xls'):
                files.append(f)
    return sorted(files)