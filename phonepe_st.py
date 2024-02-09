
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import matplotlib.pyplot as plt
import plotly.subplots as sp
import plotly.graph_objects as go
import json
import warnings
import requests
import geopandas as gpd
import pymysql

import streamlit as st
import base64

st.set_page_config(layout='wide')
def sidebar_bg(side_bg):
   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file) 
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

sidebar_bg(r"/Users/sathish/Desktop/light.webp")
set_png_as_page_bg("/Users/sathish/Desktop/phonepe9.webp")
from streamlit_option_menu import option_menu
with st.sidebar:
    st.title(":white[Contents]")
   
    selected =option_menu( menu_title= "Overview",
          options=["Home","Insights","Explore data"],
          icons=["house-door","graph-up-arrow","bar-chart-line"],
          menu_icon="book-fill",
          default_index=0,styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
         


t1,c1,c2,c4=st.columns([1,1,1,11])
with t1:
    title_html = '''
    <h1 style="text-align: center; color: green;">
        <a  style="text-decoration: none; color: #14CFCC;">
            ₹ Phonepe Pulse Data Visualization (2018-2022)
        </a>
    
    </h1><br>

    
'''

st.markdown(title_html, unsafe_allow_html=True)

#Aggregated transaction
path="/Users/sathish/Desktop/phonepe/pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)


#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}
if '.DS_Store' in Agg_state_list:
    Agg_state_list.remove('.DS_Store')
for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        print(j)
        p_j=p_i+j+"/"
        try:
            Agg_yr_list=os.listdir(p_j)
            print(Agg_yr_list)
            for k in Agg_yr_list:
                p_k=p_j+k
                Data=open(p_k,'r')
                D=json.load(Data)
                for z in D['data']['transactionData']:
                    Name=z['name']
                    count=z['paymentInstruments'][0]['count']
                    amount=z['paymentInstruments'][0]['amount']
                    clm['Transacion_type'].append(Name)
                    clm['Transacion_count'].append(count)
                    clm['Transacion_amount'].append(amount)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
        except:
            pass

#Succesfully created a dataframe
Agg_Trans=pd.DataFrame(clm)


Agg_Trans["State"] = Agg_Trans["State"].str.replace("andaman-&-nicobar-islands","Andaman & Nicobar")
Agg_Trans["State"] = Agg_Trans["State"].str.replace("-"," ")
Agg_Trans["State"] = Agg_Trans["State"].str.title()
Agg_Trans['State'] = Agg_Trans['State'].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

# Code for Tab Selection

if selected=="Home":
    c1,c2=st.columns([1,1],gap="small")
    
    title_html1 = '''

    <h1 style="text-align: right; color: green;">
        <a style="text-decoration: none; color: #5DADE2;">
            Transactions
        </a>
    
    </h1><br>
   
    '''
    
    with c1:
       
         st.write("BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.The Indian digital payments story has truly captured the world's imagination.From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.")
         video_file ="https://youtu.be/c_1H6vivsiA?si=8G3twA7bHx1VawSg"    

         st.video(video_file)

        
        # df = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")
    with c2:
        st.write(title_html1, unsafe_allow_html=True)
        options = ["Users", "Transactions"]
        default_index = options.index("Transactions")
        u_t = st.selectbox("", options,key='u_t',index=default_index)
        if u_t=="Transactions":

                myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
                cur = myconnection.cursor()
    # Defining SQL query
                sql_query = """
                    SELECT 
                SUM(transaction_amount) AS total_amount
                FROM 
                aggregated_transaction;
                """

# Execute the SQL query
                with myconnection.cursor() as cursor:
                    cursor.execute(sql_query)
                    result = cursor.fetchall()


                # Close the database connection
                myconnection.close()
            
                decimal_value = result[0][0]
                # st.write(f"Total Transaction Amount: {decimal_value}")
                value = result  # Replace with the actual value you want to display
                st.info(f"Total Transaction Amount: {decimal_value}")
         

           
        if u_t=="Users":
            myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
            cur = myconnection.cursor()
            # Defining SQL query
            sql_query = """
            SELECT 
        SUM(registereduser) AS total_count
        FROM map_user;"""

# Execute the SQL query
            with myconnection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                myconnection.close()
                decimal_value = result[0][0]
                st.info(f"Total Registered Users: {decimal_value}")
            #     #     Agg_Trans

    #     fig = px.choropleth(
    #     Agg_Trans,
    #     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    #     featureidkey='properties.ST_NM',
    #     locations='State',
    #     color='Transacion_count',
    #     color_continuous_scale='Reds'
    # )

    #     fig.update_geos(fitbounds="locations", visible=False)

    #     st.plotly_chart(fig)

    
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()

        st.markdown("## :violet[Overall State Data - Transactions Count]")
        cur.execute('''select states, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from map_transaction
                        where years =2019 and quarter =2 group by states order by states''')
        df1 = pd.DataFrame(cur.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
       
        df2 = pd.read_csv(r'/Users/sathish/Downloads/states_data.csv')
  
        df1['State'] = df2['state']

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)    

 
    
                   
# fig = px.choropleth(
#     Agg_Trans,
#     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#     featureidkey='properties.ST_NM',
#     locations='State',
#     color='Transacion_count',
#     color_continuous_scale='Reds'
# )

# fig.update_geos(fitbounds="locations", visible=False)

# fig.show()
   
   
if selected=="Explore data":
         # Connect to MySQL database
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
    
    
        # Streamlit UI
        st.title('Transaction Counts by State and Transaction Type')



        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
        year = st.slider("**Year**", min_value=2018, max_value=2022)
        quarter = st.slider("Quarter", min_value=1, max_value=4)
        
            # Defining SQL query template
        sql_template = """
            SELECT years, States, Transaction_type, Sum(transaction_count) as transaction_count 
            FROM aggregated_transaction 
            WHERE years=%s AND quarter=%s  
            GROUP BY years, States, Transaction_type
            ORDER BY transaction_count DESC;
            """

        # Function to execute SQL query and return results
        def fetch_data_from_database(year, quarter):
                    with myconnection.cursor() as cursor:
                        cursor.execute(sql_template, (year, quarter))
                        results = cursor.fetchall()
                    return results

                # Fetch data based on dropdown selection
        results = fetch_data_from_database(year, quarter)

                # Convert fetched data into a pandas DataFrame
        df = pd.DataFrame(results, columns=['years', 'States', 'Transaction_type', 'transaction_count'])

                # Plot the chart using Plotly
        fig = px.bar(df, x='Transaction_type', y='transaction_count', color='Transaction_type', 
                        title=f'Transaction Counts for {year} Q{quarter} by State and Transaction Type',
                        labels={'transaction_count': 'Transaction Count', 'States': 'States'},
                        barmode='stack')
        st.plotly_chart(fig)

            # Close the database connection
        myconnection.close()


 # Streamlit app
        
  
        st.title('Transaction Counts by State')
            
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
        sql_query = "SELECT distinct states FROM aggregated_transaction"

                # Execute the query and fetch results
        with myconnection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()

                # Close the database connection
        myconnection.close()

                # Extract the dropdown options from the query results
        dropdown_options = [result[0] for result in results]

            # Streamlit UI

        selected_option = st.selectbox('Select Option', dropdown_options)

            # Show selected option
            #  st.write('You selected:', selected_option)
        filtered_data = Agg_Trans[Agg_Trans['State'] == selected_option]
                # Display the filtered data
        st.write(f"Transaction counts for {selected_option}:")

            # Connect to  MySQL database
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
            
               
        st.title('Transaction Counts by State and Transaction Type')
        state=selected_option


                # Define SQL query template
        sql_template = """

                select transaction_type,transaction_count from aggregated_transaction where states=%s """

                # Function to execute SQL query and return results
        def fetch_data_from_database(state):
                    with myconnection.cursor() as cursor:
                        cursor.execute(sql_template, (state))
                        results = cursor.fetchall()
                    return results

                # Fetch data based on dropdown selection
        results = fetch_data_from_database(state)

                # Convert fetched data into a pandas DataFrame
        df = pd.DataFrame(results, columns=['Transaction_type', 'transaction_count'])

                # Plot the chart using Plotly
        fig = px.pie(df, names='Transaction_type', values='transaction_count', 
                            title='Transaction Counts by Type')
        st.plotly_chart(fig)
        myconnection.close()


    # 'Brand Count Visualization'    
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
        sql_query = "SELECT distinct brands FROM aggregated_user"

        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query)
                    brands = [row[0] for row in cursor.fetchall()]

                # Close the database connection
        myconnection.close()

                # Streamlit UI
        st.title('Brand Count Visualization')

                # Dropdown to select a brand
        selected_brand = st.selectbox('Select a Brand', brands)

                # Connect to the database again to get the count for the selected brand
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()

        sql_query_count = f"""
                    SELECT states, COUNT(*) AS brand_count
                    FROM aggregated_user
                    WHERE brands = '{selected_brand}'
                    GROUP BY states
                """

                # Execute the query
        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_count)
                    results = cursor.fetchall()

                # Close the database connection
        myconnection.close()

                # Create a DataFrame from the query results
        df = pd.DataFrame(results, columns=['States', 'Brand_Count'])

               
        st.write(f"Count for {selected_brand}: {df['Brand_Count'].sum()}")

        fig = px.bar(df, x='States', y='Brand_Count', title=f"Count of '{selected_brand}' by State")
        st.plotly_chart(fig)


        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()


             
        sql_query_states = "SELECT DISTINCT states FROM map_transaction"

   
        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_states)
                    states = [row[0] for row in cursor.fetchall()]

          
        sql_query_years = "SELECT DISTINCT years FROM map_transaction"


        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_years)
                    years = [row[0] for row in cursor.fetchall()]

                
        myconnection.close()

            
        st.title('Transaction Count by District for Selected State and Year')

                # Dropdown to select a state
        selected_state = st.selectbox('Select a State', states)

                # Dropdown to select a year
        selected_year = st.selectbox('Select a Year', years)

                # Connect to the database again to get the transaction count for the selected state and year

        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
                # Query to get the transaction count for the selected state and year
        sql_query_transaction_count = f"""
                    SELECT district,transaction_count
                    FROM map_transaction
                    WHERE states= '{selected_state}' AND years = '{selected_year}';
                """

                # Execute the query to get the transaction count for the selected state and year
        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_transaction_count)
                    results = cursor.fetchall()

                # Close the database connection
        myconnection.close()

                # Convert the query result to a DataFrame
        df = pd.DataFrame(results, columns=['District', 'Transaction_Count'])

                # Create a Plotly bar chart for the transaction count by district
        fig = px.pie(df, names='District', values='Transaction_Count', title=f'Transaction Count by District for {selected_state} ({selected_year})')
        st.plotly_chart(fig)


#Map User Visualization

                # Connect to your MySQL database
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()


                # Query distinct states from the database
        sql_query_states = "SELECT DISTINCT states FROM map_user"

                # Execute the query to get distinct states
        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_states)
                    states = [row[0] for row in cursor.fetchall()]

                # Query distinct years from the database
        sql_query_years = "SELECT DISTINCT years FROM map_user"

                # Execute the query to get distinct years
        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_years)
                    years = [row[0] for row in cursor.fetchall()]

                # Close the database connection
        myconnection.close()

                # Streamlit UI
        st.title('Transaction Count by Registered Users by District')

                # Dropdown to select a state
        selected_state = st.selectbox('Select a State', states,key="option1")

                # # Dropdown to select a year
        selected_year = st.selectbox('Select a Year', years,key='option2')

                # Connect to the database again to get the transaction count for the selected state and year

        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
                # Query to get the transaction count for the selected state and year
        sql_query_transaction_count = f"""
                SELECT districts, registereduser
                FROM map_user
                WHERE states= '{selected_state}' AND years = '{selected_year}'
                """

                # Execute the query to get the transaction count for the selected state and year
        with myconnection.cursor() as cursor:
                    cursor.execute(sql_query_transaction_count)
                    results = cursor.fetchall()

        myconnection.close()

                # Convert the query result to a DataFrame
        df = pd.DataFrame(results, columns=['Districts', 'registereduser'])

        fig = px.bar(df, x='Districts', y='registereduser', title=f'Registered Users Count by District')
        st.plotly_chart(fig)
                
        #Top_Transaction visualization

        # Connect to  MySQL database
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()

        # Get the distinct states from the database
        sql_query_states = "SELECT DISTINCT states FROM map_transaction"
        with myconnection.cursor() as cursor:
            cursor.execute(sql_query_states)
            states = [row[0] for row in cursor.fetchall()]

 

        # SQL query to fetch year-wise transaction count for the selected state
        sql_query_transaction_count = f"""
            SELECT years,quarter,transaction_count
        FROM 
            top_transaction
        WHERE 
            states = '{selected_state}'
        """

        # Execute the query
        with myconnection.cursor() as cursor:
            cursor.execute(sql_query_transaction_count)
            results = cursor.fetchall()

        # Close the database connection
        myconnection.close()

        # Convert the query result to a DataFrame
        df = pd.DataFrame(results, columns=['years', 'transaction_count','quarter'])

        # Create a Plotly chart for year-wise transaction count
        fig = px.bar(df, x='years', y='transaction_count', title=f'Year-wise Transaction Count for {selected_state}')
        st.plotly_chart(fig)


        #Top_User visualization

        # Connect to your MySQL database
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()


        # Query distinct states from the database
        sql_query_states = "SELECT DISTINCT states FROM map_user"

        # Execute the query to get distinct states
        with myconnection.cursor() as cursor:
            cursor.execute(sql_query_states)
            states = [row[0] for row in cursor.fetchall()]


        # Close the database connection
        myconnection.close()

        # Streamlit UI
        st.title('Transaction Count Visualization')

        
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()
   
        sql_query_transaction_count = f"""
        SELECT districts, registereduser
        FROM map_user
        WHERE states='{selected_state}' AND years = '{selected_year}'
        """

        # Execute the query to get the transaction count for the selected state and year
        with myconnection.cursor() as cursor:
            cursor.execute(sql_query_transaction_count)
            results = cursor.fetchall()

        # Close the database connection
        myconnection.close()

        # Convert the query result to a DataFrame
        df = pd.DataFrame(results, columns=['Districts', 'registereduser'])

        # Create a Plotly pie chart for the registered users count by district
        fig = px.pie(df, names='Districts', values='registereduser', title=f'Registered Users Count by District for {selected_state} ({selected_year})')
        st.plotly_chart(fig)





if selected=="Insights":
# Insights to 10 Queries

    st.markdown("## :violet[Insights]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    # colum1,colum2= st.columns([1,1.5],gap="large")
        # with colum1:
    select_Year = st.slider("**Year**", min_value=2018, max_value=2022, key='y_insights')
    select_Quarter = st.slider("Quarter", min_value=1, max_value=4,key='q_insights')
    if Type=="Transactions":

        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()


        questions=st.selectbox("Select your Query to get Insights",("1.Top 10 States with highest Transaction Count",
                                                    "2.Top 10 Districts with highest Transaction Count",
                                                    "3.Top 10 Pincodes with highest Transaction Amount"
                                                    ))
        if questions=="1.Top 10 States with highest Transaction Count":
            query1=f'''select states, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from 
                    aggregated_transaction WHERE years = '{select_Year}' AND quarter = '{select_Quarter}'
                    group by states order by Total desc limit 10'''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()
            dfv = pd.DataFrame(results1, columns=['states', 'Total_Transactions_Count','Total'])
            dfv
            fig = px.pie(dfv,values='Total',
                                names='states',
                                title='Top 10 States',
                                
                                hover_data=['Total_Transactions_Count'],
                                labels={'Total_Transactions_Count':'Total_Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)







        elif questions=="2.Top 10 Districts with highest Transaction Count":
            query1=f'''select district , sum(transaction_count) as Total_Count, sum(transaction_amount) as Total from map_transaction
                    where years = '{select_Year}' and quarter ='{select_Quarter}'
                group by district order by Total desc limit 10'''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()
            df= pd.DataFrame(results1, columns=['District', 'Transactions_Count','Total_Amount'])
            df
            fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
                


        elif questions=="3.Top 10 Pincodes with highest Transaction Amount":
            query1=f''' select pincodes, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction
                    where years = '{select_Year}' and quarter ='{select_Quarter}'
                    group by pincodes order by Total desc limit 10'''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()

            df= pd.DataFrame(results1, columns=['Pincode', 'Transactions_Count','Total_Amount'])
            df
            fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)



    if Type=="Users":
        
        myconnection = pymysql.connect(host='127.0.0.1',user='root',passwd='admin123',database='Phonepe')
        cur = myconnection.cursor()


        questions_user=st.selectbox("Select your Query to get Insights",("1.Top 10 mobile brands and its percentage based on the how many people use phonepe",
                                                    "2.Top 10 Districts with highest RegisteredUsers Count",
                                                    "3.Top 10 Pincodes with highest RegisteredUsers Count",
                                                    "4.Top 10 States with Total users and App opens"
                                                    ))
        
        if questions_user=="1.Top 10 mobile brands and its percentage based on the how many people use phonepe":
            query1=f'''select brands, sum(transaction_count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggregated_user 
                        where years = '{select_Year}' and quarter ='{select_Quarter}' group by brands order by Total_Count desc limit 10'''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()

            dfv = pd.DataFrame(results1, columns=['Brand', 'Total_Users','Avg_Percentage'])
            dfv
            fig = px.bar(dfv,
                                title='Top 10',
                                x="Total_Users",
                                y="Brand",
                                orientation='h',
                                color='Avg_Percentage',
                                color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)   
        
        elif questions_user=="2.Top 10 Districts with highest RegisteredUsers Count":
            query1=f'''select districts, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user 
                        where years ='{select_Year}' and quarter = '{select_Quarter}'
                        group by districts order by Total_Users desc limit 10    '''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()

            dfv = pd.DataFrame(results1, columns=['District', 'Total_Users','Total_Appopens'])
            dfv
            fig = px.bar(dfv,
                            title='Top 10',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        
        elif questions_user=="3.Top 10 Pincodes with highest RegisteredUsers Count":
            query1=f'''select Pincodes, sum(RegisteredUser) as Total_Users from top_user 
                where years = '{select_Year}' and quarter = '{select_Quarter}' group by Pincodes order by 
                Total_Users desc limit 10 '''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()

            dfv = pd.DataFrame(results1, columns=['Pincode', 'Total_Users'])
            dfv
            fig = px.pie(dfv,
                            values='Total_Users',
                            names='Pincode',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)




        elif questions_user=="4.Top 10 States with Total users and App opens":
            query1=f'''select states, sum(Registereduser) as Total_Users, sum(AppOpens) as 
                    Total_Appopens from map_user where years = '{select_Year}' and quarter = '{select_Quarter}'
                    group by states order by Total_Users desc limit 10'''
            with myconnection.cursor() as cursor:
                cursor.execute(query1)
                results1 = cursor.fetchall()
            myconnection.commit()

            dfv = pd.DataFrame(results1, columns=['State', 'Total_Users','Total_Appopens'])
            dfv
            fig = px.pie(dfv, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)




 
       