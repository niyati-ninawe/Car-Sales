import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Setup page
st.set_page_config(page_title="Car Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("synthetic_car_sales.xlsx")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🔎 Filter Options")
brand_filter = st.sidebar.multiselect("Select Company", df['Company'].unique(), default=df['Company'].unique())
region_filter = st.sidebar.multiselect("Select Region", df['Dealer_Region'].unique(), default=df['Dealer_Region'].unique())
min_price, max_price = st.sidebar.slider("Select Price Range", int(df['Price ($)'].min()), int(df['Price ($)'].max()), (int(df['Price ($)'].min()), int(df['Price ($)'].max())))

# Apply filters
filtered_df = df[(df['Company'].isin(brand_filter)) & 
                 (df['Dealer_Region'].isin(region_filter)) & 
                 (df['Price ($)'] >= min_price) & 
                 (df['Price ($)'] <= max_price)]

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Sales Manager View", "📊 Marketing View", "📌 Stakeholder Overview"])

# ----------------------------- SALES MANAGER TAB -----------------------------
with tab1:
    st.header("📈 Sales Overview and Trends")
    
    st.markdown("**1. Sales by Year**")
    st.write("This bar chart shows total car sales volume by year to identify sales trends over time.")
    year_sales = filtered_df.groupby('Year').size().reset_index(name='Sales Count')
    st.bar_chart(data=year_sales, x='Year', y='Sales Count')

    st.markdown("**2. Average Selling Price by Year**")
    avg_price = filtered_df.groupby('Year')['Price ($)'].mean().reset_index()
    fig = px.line(avg_price, x='Year', y='Price ($)', title='Average Selling Price per Year')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**3. Sales by Car Body Style**")
    style_sales = filtered_df['Body Style'].value_counts().reset_index()
    style_sales.columns = ['Body Style', 'Count']
    fig = px.pie(style_sales, values='Count', names='Body Style', title='Distribution of Body Styles Sold')
    st.plotly_chart(fig)

    st.markdown("**4. Top 10 Dealers by Revenue**")
    dealer_revenue = filtered_df.groupby('Dealer_Name')['Price ($)'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(dealer_revenue)

    st.markdown("**5. Monthly Sales Trend**")
    monthly = filtered_df.groupby('Month').size()
    st.line_chart(monthly)

# Continued below...
# ----------------------------- MARKETING MANAGER TAB -----------------------------
with tab2:
    st.header("📊 Marketing Insights")

    st.markdown("**6. Price Distribution**")
    st.write("This histogram helps understand the overall pricing strategy and demand clusters.")
    fig = px.histogram(filtered_df, x='Price ($)', nbins=30, title='Distribution of Car Prices')
    st.plotly_chart(fig)

    st.markdown("**7. Price vs. Annual Income**")
    st.write("This scatter plot shows if higher income customers tend to buy costlier cars.")
    fig = px.scatter(filtered_df, x='Annual Income', y='Price ($)', color='Gender', title='Annual Income vs. Car Price')
    st.plotly_chart(fig)

    st.markdown("**8. Popular Colors**")
    color_count = filtered_df['Color'].value_counts().reset_index()
    color_count.columns = ['Color', 'Count']
    fig = px.bar(color_count, x='Color', y='Count', title='Car Color Preferences')
    st.plotly_chart(fig)

    st.markdown("**9. Transmission Type Preferences**")
    transmission_count = filtered_df['Transmission'].value_counts().reset_index()
    transmission_count.columns = ['Transmission', 'Count']
    fig = px.pie(transmission_count, values='Count', names='Transmission', title='Manual vs Automatic Sales Share')
    st.plotly_chart(fig)

    st.markdown("**10. Gender-wise Sales Volume**")
    fig = px.histogram(filtered_df, x='Gender', color='Gender', title='Sales by Gender')
    st.plotly_chart(fig)

    st.markdown("**11. Top 10 Companies by Volume**")
    top_companies = filtered_df['Company'].value_counts().head(10).reset_index()
    top_companies.columns = ['Company', 'Count']
    fig = px.bar(top_companies, x='Company', y='Count', title='Top Car Companies by Sales Volume')
    st.plotly_chart(fig)

    st.markdown("**12. Body Style Preference by Gender**")
    fig = px.sunburst(filtered_df, path=['Gender', 'Body Style'], title='Gender-wise Body Style Breakdown')
    st.plotly_chart(fig)

    st.markdown("**13. Dealer Region vs Sales Count**")
    fig = px.bar(filtered_df['Dealer_Region'].value_counts().reset_index(),
                 x='index', y='Dealer_Region',
                 title="Sales Count by Dealer Region", labels={'index': 'Region', 'Dealer_Region': 'Sales'})
    st.plotly_chart(fig)

# ----------------------------- STAKEHOLDER TAB -----------------------------
with tab3:
    st.header("📌 Strategic Overview for Stakeholders")

    st.markdown("**14. Revenue by Region**")
    region_revenue = filtered_df.groupby('Dealer_Region')['Price ($)'].sum().sort_values(ascending=False).reset_index()
    fig = px.bar(region_revenue, x='Dealer_Region', y='Price ($)', title='Total Revenue by Region')
    st.plotly_chart(fig)

    st.markdown("**15. Annual Income Distribution**")
    fig = px.box(filtered_df, y='Annual Income', points="all", title='Distribution of Annual Income')
    st.plotly_chart(fig)

    st.markdown("**16. Top Performing Dealers (by Sales Count)**")
    dealer_sales = filtered_df['Dealer_Name'].value_counts().head(10).reset_index()
    dealer_sales.columns = ['Dealer_Name', 'Sales Count']
    st.table(dealer_sales)

    st.markdown("**17. Correlation Heatmap**")
    numeric_df = filtered_df[['Annual Income', 'Price ($)', 'Month', 'Year']]
    fig, ax = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.markdown("**18. Yearly Revenue Trend**")
    yearly_revenue = filtered_df.groupby('Year')['Price ($)'].sum().reset_index()
    fig = px.line(yearly_revenue, x='Year', y='Price ($)', title='Revenue by Year')
    st.plotly_chart(fig)

    st.markdown("**19. Engine Type Popularity**")
    engine_count = filtered_df['Engine'].value_counts().head(10).reset_index()
    engine_count.columns = ['Engine', 'Count']
    fig = px.bar(engine_count, x='Engine', y='Count', title='Top Engine Types by Sales')
    st.plotly_chart(fig)

    st.markdown("**20. Average Price by Body Style**")
    avg_price_body = filtered_df.groupby('Body Style')['Price ($)'].mean().reset_index()
    fig = px.bar(avg_price_body, x='Body Style', y='Price ($)', title='Average Price per Body Style')
    st.plotly_chart(fig)

    st.markdown("**21. Data Table Preview**")
    st.write("Full dataset preview (filtered):")
    st.dataframe(filtered_df.head(100))

# End of app
