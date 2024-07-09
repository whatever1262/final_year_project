import streamlit as st
import plotly.express as px
import pandas as pd
import io

# Title of the app
st.title("Interactive IT Job Market Dashboard for Cambodia")

# Add a sidebar
st.sidebar.subheader("Dashboard Settings")

# Display a sample format
st.sidebar.markdown("### Sample Format:")
sample_data = {
    'NumericColumn1': [1, 2, 3, 4, 5],
    'NumericColumn2': [10, 20, 30, 40, 50],
    'CategoricalColumn': ['A', 'B', 'C', 'D', 'E']
}
sample_df = pd.DataFrame(sample_data)
st.sidebar.write(sample_df)

# Create a sample CSV
sample_csv = sample_df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Sample CSV",
    data=sample_csv,
    file_name='sample_format.csv',
    mime='text/csv'
)

# Setup file upload
uploaded_file = st.sidebar.file_uploader(
    label="Upload your CSV or Excel file. (200MB max)",
    type=['csv', 'xlsx']
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            df = None
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        df = None

    if df is not None:
        try:
            st.write(df)
            numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
            non_numeric_columns = list(df.select_dtypes(['object']).columns)
            non_numeric_columns.append(None)
        except Exception as e:
            st.error(f"Error processing the file: {e}")
            df = None
else:
    st.write("Please upload a file to the application.")
    df = None

if df is not None:
    # Add a select widget to the sidebar
    chart_select = st.sidebar.selectbox(
        label="Select the chart type",
        options=['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot']
    )

    if chart_select == 'Scatterplots':
        st.sidebar.subheader("Scatterplot Settings")
        st.sidebar.markdown("""
        **Scatterplots** are used to see if there is a relationship between two different things. Each dot on the chart shows one observation from the data. The position of the dot is determined by the values of the two variables being compared. 
        [Learn more](https://www.google.com/search?q=scatterplot)
        """)
        try:
            # Combine non-numeric and numeric columns
            all_columns = non_numeric_columns + numeric_columns

            x_values = st.sidebar.selectbox('X axis', options=all_columns)
            y_values = st.sidebar.selectbox('Y axis', options=all_columns)
            color_value = st.sidebar.selectbox("Color", options=all_columns)

            plot = px.scatter(data_frame=df, x=x_values, y=y_values, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            st.error(f"Error creating scatterplot: {e}")

    if chart_select == 'Lineplots':
        st.sidebar.subheader("Line Plot Settings")
        st.sidebar.markdown("""
        **Lineplots** show how something changes over time. Each point on the line represents a value at a specific time, and the line connects these points to show the trend.
        [Learn more](https://www.google.com/search?q=line+plot)
        """)
        try:
            x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
            y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.line(data_frame=df, x=x_values, y=y_values, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            st.error(f"Error creating line plot: {e}")

    if chart_select == 'Histogram':
        st.sidebar.subheader("Histogram Settings")
        st.sidebar.markdown("""
        **Histograms** show the distribution of a single variable. They divide the data into bins and count how many observations fall into each bin. This helps us see how data is spread out.
        [Learn more](https://www.google.com/search?q=histogram)
        """)
        try:
            x = st.sidebar.selectbox('Feature', options=numeric_columns)
           # bin_size = st.sidebar.slider("Number of Bins", min_value=10, max_value=100, value=40)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.histogram(x=x, data_frame=df, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            st.error(f"Error creating histogram: {e}")

    if chart_select == 'Boxplot':
        st.sidebar.subheader("Boxplot Settings")
        st.sidebar.markdown("""
        **Boxplots** show the spread and skewness of a dataset. They display the median, quartiles, and outliers, giving a summary of one or more variables' distribution.
        [Learn more](https://www.google.com/search?q=boxplot)
        """)
        try:
            y = st.sidebar.selectbox("Y axis", options=numeric_columns)
            x = st.sidebar.selectbox("X axis", options=non_numeric_columns)
            color_value = st.sidebar.selectbox("Color", options=non_numeric_columns)
            plot = px.box(data_frame=df, y=y, x=x, color=color_value)
            st.plotly_chart(plot)
        except Exception as e:
            st.error(f"Error creating boxplot: {e}")
