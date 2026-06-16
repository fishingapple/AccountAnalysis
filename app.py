import streamlit as st
import os
import pandas as pd

from bill_parser import parse_bill, get_available_files
from visualizer import (
    plot_category_distribution,
    plot_amount_by_category,
    plot_amount_by_month,
    plot_amount_by_weekday,
    plot_amount_by_hour,
    plot_top_merchants,
    get_summary_stats
)

ORGAN_FILE_FOLDER = os.path.join(os.path.dirname(__file__), 'organFile')

def main():
    st.set_page_config(page_title="账单分析系统", layout="wide")
    
    st.title("微信/支付宝账单分析系统")
    st.markdown("---")
    
    available_files = get_available_files(ORGAN_FILE_FOLDER)
    
    if not available_files:
        st.warning("organFile文件夹中没有找到Excel文件，请先将账单文件放入该文件夹")
        return
    
    selected_file = st.selectbox("请选择要分析的账单文件", available_files)
    
    if st.button("开始分析"):
        file_path = os.path.join(ORGAN_FILE_FOLDER, selected_file)
        
        try:
            df, bill_type = parse_bill(file_path)
            
            st.success(f"成功识别并解析{bill_type}账单")
            
            st.markdown("---")
            st.subheader("数据概览")
            
            stats = get_summary_stats(df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("总交易笔数", stats['总交易笔数'])
            col2.metric("总支出(元)", f"{stats['总支出']:.2f}")
            col3.metric("总收入(元)", f"{stats['总收入']:.2f}")
            
            col4, col5, col6 = st.columns(3)
            col4.metric("净收支(元)", f"{stats['净收支']:.2f}")
            col5.metric("平均单笔消费(元)", f"{stats['平均单笔消费']:.2f}")
            col6.metric("消费商户数", stats['消费商户数'])
            
            st.markdown("---")
            st.subheader("消费类别分布")
            
            fig1 = plot_category_distribution(df)
            st.plotly_chart(fig1, use_container_width=True)
            
            st.markdown("---")
            st.subheader("各消费类别金额统计")
            
            fig2 = plot_amount_by_category(df)
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")
            st.subheader("月度收支趋势")
            
            fig3 = plot_amount_by_month(df)
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown("---")
            st.subheader("每周各天消费金额")
            
            fig4 = plot_amount_by_weekday(df)
            st.plotly_chart(fig4, use_container_width=True)
            
            st.markdown("---")
            st.subheader("一天中各时段消费金额")
            
            fig5 = plot_amount_by_hour(df)
            st.plotly_chart(fig5, use_container_width=True)
            
            st.markdown("---")
            st.subheader("消费最多的前10个商户")
            
            fig6 = plot_top_merchants(df)
            st.plotly_chart(fig6, use_container_width=True)
            
            st.markdown("---")
            st.subheader("原始数据预览")
            st.dataframe(df.head(20))
            
        except Exception as e:
            st.error(f"分析失败: {str(e)}")

if __name__ == "__main__":
    main()