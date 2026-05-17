# importing libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# page config
# -----------------------------------

st.set_page_config(
    page_title='Tips Dashboard',
    layout='wide'
)

# -----------------------------------
# loading data
# -----------------------------------

@st.cache_data
def load_data():
    return pd.read_csv('tips.csv')

df = load_data()

# new column (tip_percent)

df['tip_percent'] = (df['tip'] / df['total_bill']) * 100

# -----------------------------------
# sidebar
# -----------------------------------

st.sidebar.title('Tips Dashboard')
st.sidebar.image('tips.jpg')
st.sidebar.write(
    'This dashboard uses Tips dataset for educational purposes.')

# filters
cat_filter = st.sidebar.selectbox(
    'Color Filter',
    ['None','sex','smoker','day','time']
)

num_filter = st.sidebar.selectbox(
    'Size Filter',
    ['None','total_bill','tip','size']
)

row_filter = st.sidebar.selectbox(
    'Row Filter',
    ['None','sex','smoker','day','time']
)

column_filter = st.sidebar.selectbox(
    'Column Filter',
    ['None','sex','smoker','day','time']
)

# -----------------------------------
# Convert 'None' string from UI to Python None
# -----------------------------------

def clean_filter(value):
    return None if value == 'None' else value

cat_filter = clean_filter(cat_filter)
num_filter = clean_filter(num_filter)
row_filter = clean_filter(row_filter)
column_filter = clean_filter(column_filter)

st.sidebar.markdown(
        "Made by [Hosam Fahmy](https://www.linkedin.com/in/hosam-fahmy/):heart:"

)

# -----------------------------------
# dashboard title
# -----------------------------------

st.title('Restaurant Tips Dashboard')
st.write("Interactive dashboard for analyzing restaurant bills and tips.")

# -----------------------------------
# metrics
# -----------------------------------

a1, a2, a3, a4 = st.columns(4)

a1.metric('Max Total Bill',
          round(df['total_bill'].max(),2))

a2.metric('Average Total Bill',
          round(df['total_bill'].mean(),2))
a3.metric('Max Tip',
          round(df['tip'].max(),2))
a4.metric('Average Tip %',
          round(df['tip_percent'].mean(),2))

# -----------------------------------
# scatter plot
# -----------------------------------

st.subheader('Total Bill vs Tip')

fig=px.scatter(
    data_frame=df,
    x='total_bill',
    y= 'tip',
    color=cat_filter,
    size=num_filter,
    facet_row=row_filter,
    facet_col=column_filter
)

st.plotly_chart(fig , use_container_width= True)

st.info('Customers with higher bills usually leave higher tips.')

# -----------------------------------
# charts row
# -----------------------------------

c1, c2, c3 = st.columns((4,3,3))

# chart 1
with c1:
    st.write('Total Bills by Gender')

    fig=px.bar(
        data_frame= df,
        x='sex',
        y='total_bill',
        color='sex'
    )
                
    st.plotly_chart(fig , use_container_width=True)

# chart 2
with c2:
    st.write('Tips by Smoking Status')
    
    fig=px.pie(
        data_frame= df,
        names='smoker',
        values='tip',
        hole=0.4
    )
    st.plotly_chart(fig ,use_container_width= True )

# chart 3
with c3:
    st.write('Tips by Day')
    
    fig=px.pie(
        data_frame= df,
        names='day',
        values='tip',
        hole=0.4
    )
    st.plotly_chart(fig ,use_container_width=True)
    
# -----------------------------------
# tip percentage chart
# -----------------------------------
st.subheader('Tip Percentage by Day')
 
fig=px.box(
    data_frame= df,
    x='day',
    y='tip_percent',
    color='day'
)

st.plotly_chart(fig , use_container_width= True)
              
# -----------------------------------
# dataframe
# -----------------------------------

st.subheader('Dataset')

st.dataframe(data= df)

# -----------------------------------
# download csv
# -----------------------------------

csv = df.to_csv(index=False)

st.download_button(
    'Download Dataset',
    data=csv,
    file_name='tips_data.csv',
    mime='text/csv'
)