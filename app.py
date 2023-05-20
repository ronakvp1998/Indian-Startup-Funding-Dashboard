import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk

st.set_page_config(layout='wide',page_title='Indian Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    # Total Invested Amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg amount infused in a startup
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # Total funded startup
    startup_funded = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1 :
        st.metric('Total',str(total) + ' Cr')

    with col2:
        st.metric('Max',str(max_funding)+ ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding))+' Cr')

    with col4:
        st.metric('Funded Startups',str(startup_funded))

    st.header('MoM Graph')
    selected_options = st.selectbox('Select Types',['Total','Counts'])
    if selected_options == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3,ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)
    # Load the recent 5 investments of the investors
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%0.01f')
        st.pyplot(fig1)

    col11, col22 = st.columns(2)
    with col11:

        vertical_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Rounds')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%0.01f')
        st.pyplot(fig1)
    with col22:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Sectors invested in City')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%0.01f')
        st.pyplot(fig1)


    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp',"Investor"])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('StartUp Analysis')

elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2 :
        load_investor_details(selected_investor)




