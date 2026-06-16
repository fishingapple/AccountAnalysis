import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def plot_category_distribution(df):
    expense_df = df[df['收支类型'] == '支出']
    
    category_counts = expense_df['交易类型'].value_counts().reset_index()
    category_counts.columns = ['交易类型', '次数']
    
    fig = px.pie(category_counts, values='次数', names='交易类型', 
                 title='消费类别分布',
                 hole=0.3,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    
    return fig

def plot_amount_by_category(df):
    expense_df = df[df['收支类型'] == '支出']
    
    amount_by_category = expense_df.groupby('交易类型')['金额'].sum().reset_index()
    amount_by_category = amount_by_category.sort_values('金额', ascending=False)
    
    fig = px.bar(amount_by_category, x='交易类型', y='金额',
                 title='各消费类别金额统计',
                 color='金额',
                 color_continuous_scale='Blues',
                 labels={'金额': '金额(元)', '交易类型': '消费类别'})
    
    fig.update_layout(title_x=0.5, xaxis_tickangle=-45)
    
    return fig

def plot_amount_by_month(df):
    df['月份'] = df['交易时间'].dt.to_period('M').astype(str)
    
    monthly_data = df.groupby(['月份', '收支类型'])['金额'].sum().reset_index()
    
    fig = px.line(monthly_data, x='月份', y='金额', color='收支类型',
                  title='月度收支趋势',
                  labels={'金额': '金额(元)', '月份': '月份'},
                  markers=True)
    
    fig.update_layout(title_x=0.5)
    
    return fig

def plot_amount_by_weekday(df):
    expense_df = df[df['收支类型'] == '支出']
    
    expense_df['星期'] = expense_df['交易时间'].dt.dayofweek
    weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
    expense_df['星期'] = expense_df['星期'].map(weekday_map)
    
    weekday_amount = expense_df.groupby('星期')['金额'].sum().reset_index()
    weekday_order = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    weekday_amount['星期'] = pd.Categorical(weekday_amount['星期'], categories=weekday_order, ordered=True)
    weekday_amount = weekday_amount.sort_values('星期')
    
    fig = px.bar(weekday_amount, x='星期', y='金额',
                 title='每周各天消费金额',
                 color='金额',
                 color_continuous_scale='Viridis',
                 labels={'金额': '金额(元)', '星期': '星期'})
    
    fig.update_layout(title_x=0.5)
    
    return fig

def plot_amount_by_hour(df):
    expense_df = df[df['收支类型'] == '支出']
    
    expense_df['小时'] = expense_df['交易时间'].dt.hour
    
    hourly_amount = expense_df.groupby('小时')['金额'].sum().reset_index()
    
    fig = px.line(hourly_amount, x='小时', y='金额',
                  title='一天中各时段消费金额',
                  labels={'金额': '金额(元)', '小时': '小时'},
                  markers=True,
                  color_discrete_sequence=['#636EFA'])
    
    fig.update_layout(title_x=0.5)
    
    return fig

def plot_top_merchants(df):
    expense_df = df[df['收支类型'] == '支出']
    
    top_merchants = expense_df.groupby('交易对方')['金额'].sum().reset_index()
    top_merchants = top_merchants.sort_values('金额', ascending=False).head(10)
    
    fig = px.bar(top_merchants, x='交易对方', y='金额',
                 title='消费最多的前10个商户',
                 color='金额',
                 color_continuous_scale='Reds',
                 labels={'金额': '金额(元)', '交易对方': '商户'})
    
    fig.update_layout(title_x=0.5, xaxis_tickangle=-45)
    
    return fig

def get_summary_stats(df):
    stats = {}
    
    stats['总交易笔数'] = len(df)
    
    expense_df = df[df['收支类型'] == '支出']
    income_df = df[df['收支类型'] == '收入']
    
    stats['总支出'] = expense_df['金额'].sum()
    stats['总收入'] = income_df['金额'].sum()
    stats['净收支'] = stats['总收入'] - stats['总支出']
    
    stats['平均单笔消费'] = expense_df['金额'].mean()
    stats['最大单笔消费'] = expense_df['金额'].max()
    stats['最小单笔消费'] = expense_df['金额'].min()
    
    stats['消费类别数'] = expense_df['交易类型'].nunique()
    stats['消费商户数'] = expense_df['交易对方'].nunique()
    
    return stats