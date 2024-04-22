import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# Google Fonts URL
google_fonts_url = """
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
"""
@st.cache_data
def load_data():
    # Load data from a CSV file
    return pd.read_csv("movies_updated.csv")

# Load data using the cached function
dfMovie = load_data()
df_top_20_movies_sorted = dfMovie.sort_values(by='budget', ascending=False).head(20).sort_values(by='revenue', ascending=False)

# App configurations
css = """
<style>
/* Main app styling */
.main {
     background: linear-gradient(to right, #000000, #808080); /* Gradient background from black to grayish */
    padding: 10px;
    font-family: 'Open Sans', sans-serif;
}

/* Sidebar styling */
.sidebar {
    background-color: #e0f7fa;
    padding: 15px;
    border-right: 2px solid #00796b;
    font-family: 'Roboto', sans-serif;
}
.sidebar-image {
    padding: 10px;
    background-color: #e0f7fa; /* Light teal */
    border-radius: 10px;
    border: 2px solid #00796b; /* Darker teal */
    text-align: center; /* Center the image */
    margin-bottom: 20px; /* Add margin below the image */
}

/* Title styling */
h1 {
    color: #00796b;
    font-family: 'Roboto', sans-serif;
    font-weight: 700;
    text-align: center;
    margin-bottom: 20px;
}

/* Section header styling */
h3 {
    color: #004d40;
    font-family: 'Roboto', sans-serif;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Paragraph styling */
p.desc {
    background-color: #b2dfdb;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #004d40;
    margin-bottom: 20px;
    font-family: 'Open Sans', sans-serif;
}

/* Footer styling */
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    color: white;
    background-color: #00796b;
    text-align: center;
    padding: 10px;
    font-family: 'Roboto', sans-serif;
    font-size: 20px
}
/* Button styling */
button[data-baseweb="button"] {
    background-color: #00796b; /* Teal */
    color: white;
    border-radius: 8px;
    font-family: 'Roboto', sans-serif;
    font-weight: 600;
    padding: 10px;
    width: 100%;
    text-align: left;
    transition: background-color 0.3s ease;
}

button[data-baseweb="button"]:hover {
    background-color: #005f73; /* Darker teal on hover */
}

button[data-baseweb="button"]:active {
    background-color: #004c57; /* Even darker teal when active */
}
</style
"""

# Apply the CSS to the app
def main():
    st.sidebar.image('data_analysis_image.jpg', caption='Top Movies', use_column_width=True, class_name='sidebar-image')
    # Set the title for the sidebar
    st.sidebar.title("Navigation")

    # Create buttons for navigating between pages
    home_button = st.sidebar.button("Home")
    data_exploration_button = st.sidebar.button("Data Exploration")
    visualizations_button = st.sidebar.button("Visualizations")

    # Determine which page to display based on the button pressed
    if home_button:
        page = "Home"
    elif data_exploration_button:
        page = "Data Exploration"
    elif visualizations_button:
        page = "Visualizations"
    else:
        page = "Home"

    if page == "Home":
        st.title("Welcome to Top Movies Analysis App")
        st.write("""
        Here's an example of additional information you can include in your app's introductory section to help users better understand what your app offers and how they can benefit from it:

---

**Welcome to the Top Movies Analysis App**

This app provides an in-depth analysis of the top 20 movies based on various factors such as budget, revenue, director, and release year. Explore the data and interactive visualizations to gain valuable insights into the world of top-grossing films.

### Key Features:

- **Data Exploration:** Dive into the data with a customizable view. Filter movies by release year and explore different columns such as budget, revenue, director, and more.

- **Visualizations:** Visualize data trends and relationships using interactive charts and plots. Explore how factors like budget and revenue are distributed among the top 20 movies.

- **Director Comparisons:** Compare the average budget and revenue of movies by director. Discover which directors achieve the highest returns on their projects.

- **Release Year Trends:** Analyze how the release year impacts the number of top movies and other factors.

- **Runtime Distribution:** Understand how movie durations vary and which runtimes are most common among top movies.

- **Top Movies by Vote Average:** Examine the top 10 movies based on vote average and explore what makes these movies stand out.

Whether you're a movie enthusiast, a data analyst, or simply curious about the world of top-grossing films, this app offers insights into the key aspects of these movies. Start exploring the data and uncovering interesting patterns and trends today!
        """)
        
    elif page == "Data Exploration":
        st.title("Data Exploration")
        st.dataframe(df_top_20_movies_sorted[['original_title', 'budget', 'revenue', 'director', 'release_year']])
        
        st.write("Use the options below to filter and sort the data.")
        filter_year = st.slider("Filter by release year:", int(df_top_20_movies_sorted['release_year'].min()), int(df_top_20_movies_sorted['release_year'].max()), (int(df_top_20_movies_sorted['release_year'].min()), int(df_top_20_movies_sorted['release_year'].max())))
        filtered_data = df_top_20_movies_sorted[(df_top_20_movies_sorted['release_year'] >= filter_year[0]) & (df_top_20_movies_sorted['release_year'] <= filter_year[1])]
        
        st.dataframe(filtered_data)
        
    elif page == "Visualizations":
        st.title("Visualizations")
        
        # Scatter plot of Budget vs Revenue
        st.header("Budget vs Revenue")
        # Group the data by original title and calculate the sum of budget and revenue
        grouped_data = df_top_20_movies_sorted.groupby('original_title').agg({'budget': 'sum', 'revenue': 'sum'}).reset_index()

        # Create the bar chart
        fig = go.Figure()

        # Define color palette
        budget_color = 'indigo'  # Rich purple color for budget
        revenue_color = 'coral'  # Coral color for revenue

        # Add a bar trace for budget
        fig.add_trace(go.Bar(
            x=grouped_data['original_title'],
            y=grouped_data['budget'],
            name='Budget',
            marker_color=budget_color  # Apply the color for budget
        ))

        # Add a bar trace for revenue
        fig.add_trace(go.Bar(
            x=grouped_data['original_title'],
            y=grouped_data['revenue'],
            name='Revenue',
            marker_color=revenue_color  # Apply the color for revenue
        ))

        # Update the layout
        fig.update_layout(
            title='Total Budget and Revenue by Movie',
            xaxis_title='Movie Title',
            yaxis_title='Amount',
            barmode='stack',  # Change barmode to stack for stacked bars
            template='plotly_white',  # Apply a clean, white theme
            xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
            legend_title_text='Legend',  # Add a title to the legend
            font=dict(family="Arial, sans-serif", size=12, color='black'),  # Customize font
            hovermode='x unified'  # Add hover mode for unified display
        )

        # Show the plot
        st.plotly_chart(fig)
        
        # Pie chart of Revenue Distribution
        st.header("Revenue Distribution")
                # Create a horizontal bar chart
        fig = go.Figure()

        # Add a bar trace for revenue
        fig.add_trace(go.Bar(
            y=df_top_20_movies_sorted['original_title'],  # Movie titles on y-axis
            x=df_top_20_movies_sorted['revenue'],  # Revenue on x-axis
            orientation='h',  # Make the bar chart horizontal
            marker=dict(color='lightcoral')  # Use an attractive color
        ))

        # Update layout
        fig.update_layout(
            title='Revenue Distribution by Movie (Horizontal Bar Chart)',
            xaxis_title='Revenue',
            yaxis_title='Movie Title',
            template='plotly_white',  # Apply a clean, white theme
            yaxis=dict(autorange='reversed'),  # Reverse the y-axis to order movies from top revenue to lowest
            font=dict(family="Arial, sans-serif", size=12, color='black')  # Customize font
        )

        # Show the plot
        st.plotly_chart(fig)
        
        # Line plot of Release Year Trends
        st.header("Release Year Trends")
        release_year_counts = df_top_20_movies_sorted['release_year'].value_counts().sort_index()
        fig = px.line(x=release_year_counts.index, y=release_year_counts.values)

        # Add markers and customize color
        fig.update_traces(mode='lines+markers', marker=dict(symbol='circle', size=18, color='blue'), line=dict(color='white'))

        # Update the layout of the plot
        fig.update_layout(
            title='Number of Movies Released by Year',
            xaxis_title='Release Year',
            yaxis_title='Number of Movies',
            template='plotly_white'  # Optional: Add a white theme for better visual appearance
        )

        # Display the plot using Streamlit
        st.plotly_chart(fig)
        
        # Histogram of Runtime Distribution
       # Set the style of the plots to enhance appearance
        sns.set_style("whitegrid")

       # Header for runtime distribution
        st.header("Runtime Distribution")

        # Create the runtime density plot
        plt.figure(figsize=(8, 6))

        # Use kdeplot for a density plot
        sns.kdeplot(df_top_20_movies_sorted['runtime'], color='mediumorchid', fill=True, linewidth=2)

        # Add markers for key points on the line
        sns.kdeplot(df_top_20_movies_sorted['runtime'], color='navy', linestyle='--', label='Runtime Density')

        # Set the plot title and labels
        plt.title('Runtime Density', fontsize=14, fontweight='bold')
        plt.xlabel('Runtime (minutes)', fontsize=12)
        plt.ylabel('Density', fontsize=12)

        # Add a grid for better readability
        plt.grid(True, alpha=0.5)

        # Add a legend for clarity
        plt.legend()

        # Show the plot using st.pyplot()
        st.pyplot(plt)


        #Budget vs Director
        # Budget vs Director
        st.header("Budget vs Director")

# Use Plotly bar chart to visualize budget by director
        fig = px.bar(df_top_20_movies_sorted, x='director', y='budget', color='director',
             title='Budget by Director', labels={'budget': 'Budget ($)'})
        fig.update_layout(xaxis_title='Director', yaxis_title='Budget ($)', showlegend=False)
        st.plotly_chart(fig)

        
        # Bar chart of Vote Average
        st.header("Top 10 Movies by Vote Average")
        top_10_movies = df_top_20_movies_sorted.nlargest(10, 'vote_average')
        fig = px.bar(top_10_movies, x='original_title', y='vote_average', color='director')
        fig.update_layout(title='Top 10 Movies by Vote Average', xaxis_title='Movie Title', yaxis_title='Vote Average')
        st.plotly_chart(fig)
        # Revenue vs Director
       # Revenue vs Director
        # Section header
        st.header("Revenue vs Director")

        # Create the bar plot using sns.barplot
        fig, ax = plt.subplots(figsize=(12, 8))

        # Create the bar plot
        sns.barplot(x='revenue', y='director', data=df_top_20_movies_sorted, color='skyblue', ax=ax)

        # Set plot title and axis labels
        ax.set_title('Revenue vs Director', fontsize=16, fontweight='bold')
        ax.set_xlabel('Revenue ($)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Director', fontsize=14, fontweight='bold')

        # Customize the x-axis tick labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        # Add gridlines for better readability
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)

        # Annotate bars with revenue values
        for i, p in enumerate(ax.patches):
            ax.annotate(f'${p.get_width():,.0f}',
                        (p.get_width() + 5, p.get_y() + p.get_height() / 2),
                        ha='left', va='center', fontsize=12, color='black')

        # Customize the appearance of the plot
        sns.despine(left=True, bottom=True)  # Remove unnecessary spines
        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)

        # Display the plot using Streamlit's st.pyplot
        st.pyplot(fig)



       # Top 10 movies by vote average
        st.header("Top 10 Movies by Vote Average")

# Filter the top 10 movies by vote average
        top_10_movies = df_top_20_movies_sorted.nlargest(10, 'vote_average')

# Create a bar chart using Plotly Express
        fig = px.bar(
            top_10_movies,
            x='original_title',
            y='vote_average',
            title='Top 10 Movies by Vote Average',
            labels={'original_title': 'Movie Title', 'vote_average': 'Vote Average'},
            color='vote_average',  # Color the bars based on vote average
            color_continuous_scale='bluered',  # Color scale for better visual differentiation
            template='plotly_white'  # Choose a lighter template for better visibility
        )

        # Update layout for better readability
        fig.update_layout(
            xaxis_title_text='Movie Title',
            yaxis_title_text='Vote Average',
            xaxis_tickangle=45  # Rotate x-axis labels for readability
        )

# Display the plot in Streamlit
        st.plotly_chart(fig)

        
        # Comparison of Budget and Revenue by Director
        st.header("Comparison of Budget and Revenue for Top 20 Movies by Director")
        budget_means = df_top_20_movies_sorted.groupby('director')['budget'].mean()
        revenue_means = df_top_20_movies_sorted.groupby('director')['revenue'].mean()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=budget_means.index, y=budget_means.values, name='Budget', marker_color='skyblue'))
        fig.add_trace(go.Bar(x=revenue_means.index, y=revenue_means.values, name='Revenue', marker_color='salmon'))
        
        fig.update_layout(title='Comparison of Budget and Revenue for Top 20 Movies by Director', xaxis_title='Director', yaxis_title='Amount ($)', barmode='group')
        st.plotly_chart(fig)
        
        # Add more visualizations as needed...

    # Footer
    st.markdown("<footer class='footer'>© 2024 Top Movies Analysis App  Made By Waqar Haider❤️ </footer> ", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

