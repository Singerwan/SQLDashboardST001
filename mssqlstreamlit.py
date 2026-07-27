import pyodbc
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np


st.set_page_config(layout="wide")
# establish connection 
conn=pyodbc.connect(
"Driver={SQL Server};"
"Server=SINGERWANGALAXY\\SQLEXPRESS;"
"Database=SalesDB;"
"Trusted_Connection=yes;"
)

if conn:
    print('True')
    
## query 
query= 'select * from Sales.OrdersArchive'
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()

    
MscfSqldfPrb=pd.DataFrame(np.array(rows),columns=['OrderID'
      ,'ProductID'
      ,'CustomerID'
      ,'SalesPersonID'
      ,'OrderDate'
      ,'ShipDate'
      ,'OrderStatus'
      ,'ShipAddress'
      ,'BillAddress'
      ,'Quantity'
      ,'Sales'
      ,'CreationTime'])

### data type convert 
MscfSqldfPrb['OrderID']=MscfSqldfPrb['OrderID'].astype(str)
MscfSqldfPrb['ProductID']=MscfSqldfPrb['ProductID'].astype(str)
MscfSqldfPrb['CustomerID']=MscfSqldfPrb['CustomerID'].astype(str)
MscfSqldfPrb['SalesPersonID']=MscfSqldfPrb['SalesPersonID'].astype(int)
MscfSqldfPrb['Sales']=MscfSqldfPrb['Sales'].astype(int)
MscfSqldfPrb['Quantity']=MscfSqldfPrb['Quantity'].astype(int)
MscfSqldfPrb['CreationTime']=pd.to_datetime(MscfSqldfPrb['CreationTime'])
MscfSqldfPrb['OrderDate']=pd.to_datetime(MscfSqldfPrb['OrderDate'])
MscfSqldfPrb['ShipDate']=pd.to_datetime(MscfSqldfPrb['ShipDate'])

# header 
st.title('Dashboard via SQL')
vidfile=open("./assets/videos/sql.mp4","rb").read()
st.video(vidfile,loop=True, autoplay=True, muted=False )
# audio same syntax as video = only exception the required  format argument
# double check data types 
with st.expander('Display DataTypes of all columns'):
    st.write(MscfSqldfPrb.dtypes)

if st.checkbox('Hide | Show DataFrame'):
    st.dataframe(MscfSqldfPrb)
    

# plotting 

st.subheader('please select your chart type')
chart_type=st.selectbox(' chart type dropdown box :' ,[     'Scatter Plot',
                                                            'Line Chart',
                                                            'Bar Chart',
                                                            'Histogram',
                                                            'Box Plot',
                                                            'Pie Chart',
                                                            '3D Scatter Plot'] ,
                        key='chart_type_select_box1')


# visualize the relationship between sepal length and sepal width , colored by species
if chart_type =='Scatter Plot':
    fig = px.scatter(MscfSqldfPrb,
                     x='Quantity',
                     y= 'Sales',
                     color='ProductID',
                     title='Quantity VS Sales')
    st.plotly_chart(fig)
    
# since line charts typically require time-series data 
elif chart_type=='Line Chart':
    MscfSqldfPrb_sorted = MscfSqldfPrb.sort_values(by='Sales')
    fig = px.line(MscfSqldfPrb_sorted, 
                  x='OrderDate',
                  y='Sales',
                  color='CustomerID',
                  markers=True,
                  title='Orders OverTime')
    st.plotly_chart(fig)
     
# display the average sepal length of each species using a bar chart 
elif chart_type=='Bar Chart':
    avg_sepal_length =MscfSqldfPrb.groupby('CustomerID')['Sales'].sum().reset_index()
    fig = px.bar(avg_sepal_length, 
                 x=avg_sepal_length['CustomerID'],
                 y=avg_sepal_length['Sales'],
                 color='CustomerID',
                 title='Orders-Total per Customer')
    st.plotly_chart(fig)    
    
# show distribution of sepal lengths across all species
elif chart_type=='Histogram':
    fig=px.histogram(MscfSqldfPrb, 
                     x='Sales',
                     nbins=40,
                     title='Order Distribution')
    st.plotly_chart(fig)
    
# visulize the distribution of sepal lengths for each species using a box plot
elif chart_type =='Box Plot':
    fig = px.box( MscfSqldfPrb,
                  x='ProductID',
                  y='Sales',
                  title=' Sales peR Product')
    st.plotly_chart(fig)
    
# display the distribution of species in the dataset 
elif chart_type=='Pie Chart':
    species_count =MscfSqldfPrb['ProductID'].value_counts().reset_index()
    # ----------------------------------------------.re
    fig = px.pie( species_count,
                  names=species_count['ProductID'],    # label|legend
                  values=species_count['count'],
                  hover_data=[('count'),('ProductID')],
                  hole=True,
                  title='ProductID Proportion |Percentage % ')
    st.plotly_chart(fig)
    
# create a 3D scatter plot showing the sepal length , sepal width, and petal length color by species
elif chart_type=='3D Scatter Plot':
    fig=px.scatter_3d(MscfSqldfPrb,
                      x='ProductID',
                      y='Sales',
                      z='Quantity',
                      color='CustomerID',
                      title='3D Scatter Plot of Sales DataFrame') 
    st.plotly_chart(fig)
    
