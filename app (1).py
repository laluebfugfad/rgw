import re
import jieba
from collections import Counter
from pyecharts.charts import  WordCloud
from pyecharts import options as opts
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def remove(text):
    # 这个正则表达式匹配了常见的中文标点符号
    chinese_punctuation = re.compile(r'[\u3002\uFF1F\uFF01\u3001\uff0c\u300c\u300d\u300e\u300f\u2018\u2019\u201c\u201d\u2014\u2026\u2013\uFF0E\u300a\u300b\uff1b\uff1a\u3000\u000A]')
    return chinese_punctuation.sub('', text)

def tokenize(text):
    return jieba.cut(text)


#统计
def count_words(text):
    tokens=list(tokenize(text))
    freq_dict=Counter(tokens)
    return freq_dict


path='demo.txt'
with open(path,'r',encoding='utf-8')as file:
    text=file.read()
#除去标点符号
text=remove(text)

dict1={}

word_freq=count_words(text)
for word,freq in word_freq.most_common():
    if len(dict1)<=20:
        dict1.update({f'{word}':freq})

#创建实例
wordcloud=WordCloud(init_opts=opts.InitOpts(width="400px",height="600px")
)

wordcloud.add("",list(dict1.items()),
             #设置词距
              word_gap=40,
              #设置词大小范围
              word_size_range=[20,100]
              )

#设置全局配置
wordcloud.set_global_opts(
    title_opts=opts.TitleOpts(title="文字词云"),
    #设置画布大小
)
#设置样式
wordcloud.set_series_opts(
    label_opts=opts.LabelOpts(
        font_size=20

    )
)
wordcloud.render("wordcloud.html")


#侧边栏图像类型选择
def main():
    #指定默认字体：微软雅黑
    plt.rcParams['font.sans-serif']=['Microsoft YaHei']
    #解决负号‘-’显示为方块
    plt.rcParams['axes.unicode_minus']=False
    top_20_word=dict(word_freq.most_common(20))
    st.write("词频前20词汇：")


#图形选择
    selected_graph=st.selectbox(
    '选择图形类型',('柱状图','折线图','饼图','条形图','水平条形图','散点图','箱型图')
)

#数据准备
    data=pd.DataFrame(list(top_20_word.items()),columns=['词汇','频率'])

#根据选择展示图形
    if selected_graph == '柱状图':
        fig, ax = plt.subplots()
        ax.bar(data['词汇'], data['频率'])
        ax.set_title('词频柱状图')
        st.pyplot(fig)

    elif selected_graph == '折线图':
        fig, ax = plt.subplots()
        ax.plot(data['词汇'], data['频率'])
        ax.set_title('词频折线图')
        st.pyplot(fig)

    elif selected_graph == '饼图':
        fig, ax = plt.subplots()
        ax.pie(data['频率'], labels=data['词汇'], autopct='%1.1f%%')
        ax.set_title('词频饼图')
        st.pyplot(fig)

    elif selected_graph == "条形图":
        fig, ax = plt.subplots()
        ax.barh(data['词汇'], data['频率'])
        ax.set_title('词频条形图')
        st.pyplot(fig)

    elif selected_graph == '水平条形图':
        fig, ax = plt.subplots()
        ax.barh(data['词汇'], data['频率'])
        ax.set_title('词频水平条形图')
        st.pyplot(fig)

    elif selected_graph == '散点图':
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=data, x='词汇', y='频率', ax=ax)
        ax.set_title('词频散点图')
        st.pyplot(fig)

    elif selected_graph == '箱型图':
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=data['频率'], ax=ax)
        ax.set_title('词频箱型图')
        st.pyplot(fig)

#渲染图标到图片     

if __name__=="__main__":
    main()

    



#