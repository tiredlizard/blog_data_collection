import numpy as np
import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from blog_plots import *
import streamlit as st
import ast

data = pd.read_csv('games_data.csv')
data['Year'] = pd.to_numeric(data['Year'], errors='coerce', downcast='integer')

list_columns = ['Genre', 'Perspective', 'Gameplay', 'Interface', 'Setting']

# Convert string representations of lists to actual lists
for col in list_columns:
    data[col] = data[col].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else [])

st.title("Play With Game Data")

tab1, tab2, tab3 = st.tabs(['Explore', 'Find a Game by Criteria', 'Find a Game by Title'])

# Setup
setting_options = [
    'Asia', 
    'America',
    'Caribbean',
    'Contemporary', 
    'Cyberpunk / dark sci-fi', 
    'Europe', 
    'Fantasy',  
    'Japan', 
    'Medieval', 
    'Post-apocalyptic', 
    'Sci-fi / futuristic',
    'Steampunk',
    'Western'
]

genre_options = ['Action', 'Adventure', 'Compilation', 
                                'Educational', 'Gambling', 'Puzzle', 
                                'Racing / Driving', 'Role-playing (RPG)', 'Simulation', 
                                'Special edition', 'Sports', 'Strategy / tactics']


persp_options = ['1st-person', '3rd-person', 'Behind view', 'Side view', 
                                  'Diagonal-down', 'Top-down',  'Audio game', 'Text-based / Spreadsheet']

inter_options = ['Direct control', 'Menu structures', 'Motion control', 'Multiple units/characters control',
                                     'Point and select', 'Text parser', 'Voice control']

gameplay_options = [
        'Action RPG', 
        'Arcade', 
        'Beat \'em up / brawler', 
        'Board game', 
        'Cards / tiles', 
        'Graphic adventure', 
        'Interactive fiction / text adventure', 
        'Japanese-style RPG (JRPG)', 
        'Managerial / business simulation', 
        'Mini-games', 
        'Music / rhythm', 
        'Platform', 
        'Puzzle elements', 
        'RPG elements', 
        'Shooter', 
        'Survival horror',
        'Visual novel'
    ]

month_options = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']

with tab1:
    st.write('Take a brief look at a few variables.')
    # Convert 'Year' column to a categorical type
    data['Year'] = pd.Categorical(data['Year'], ordered=True)

    input_genre = st.radio('Select a genre to display:', genre_options, horizontal = True)

    # Filter the data where the input genre is in the Genre list for each row
    genre_data = data[data['Genre'].apply(lambda x: input_genre in x)].copy()
    
    # Group by 'Year' and count the occurrences for each year
    genre_counts = genre_data.groupby('Year').size().reset_index(name='Count')
    
    # Convert 'Year' to a categorical type (factor) and ensure consistent range of years
    min_year = genre_counts['Year'].min()
    max_year = genre_counts['Year'].max()
    
    # Create a complete range of years to ensure all years are represented
    all_years = pd.DataFrame({'Year': range(min_year, max_year + 1)})
    
    # Merge the complete years range with the genre_counts to include years with zero count
    genre_counts = pd.merge(all_years, genre_counts, on='Year', how='left').fillna({'Count': 0})
    
    # Convert 'Year' to a categorical type (factor) with the correct order
    genre_counts['Year'] = pd.Categorical(genre_counts['Year'], categories=range(min_year, max_year + 1), ordered=True)

    # Plot the count per year with Plotly
    fig = px.line(genre_counts, x='Year', y='Count', title=f"Genre '{input_genre}' Count Over Time")
    st.plotly_chart(fig)

    ##### ----------------------

    # Explode the 'Setting' column into separate rows
    genre_data_exploded = data.explode('Setting').dropna(subset=['Setting'])
    
    # Group by 'Year' and 'Setting' and count occurrences
    setting_year_counts = genre_data_exploded.groupby(['Year', 'Setting']).size().reset_index(name='Count')

    selected_settings = st.multiselect('Select Settings to Display:', setting_options, default='Fantasy')

    # Filter the data based on selected settings
    filtered_data = setting_year_counts[setting_year_counts['Setting'].isin(selected_settings)]
    
    fig = px.bar(filtered_data, 
                 x='Year', 
                 y='Count', 
                 color='Setting', 
                 title="Setting Count Over Time",
                 hover_data={'Year': False, 'Setting': True, 'Count': True})
    
    # Update layout for better interactivity
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Count",
        barmode='stack',  # Stacked bar chart for multiple settings
        xaxis={'categoryorder': 'category ascending'},  # Ensure years are ordered
        hovermode='x unified',  # Show hover information across all bars of the same year
        height=600
    )

    st.plotly_chart(fig)




    st.subheader('Release Month')
    month_input = st.select_slider("Month:", month_options)
    month_data = data[data['Released'] == month_input]
    nunique = month_data['Released'].shape[0]
    st.write(f"There were {nunique} game(s) released on the Switch in {month_input}.")


    # ------------------
    # variable_input = st.selectbox('Select variable to compare with Score:', options=data.columns)

    # # Create a box plot comparing Score to the selected variable
    # fig = px.box(data, x=variable_input, y='Score', title=f'Comparison of Score by {variable_input}')

    # # Display the plot
    # st.plotly_chart(fig)


    # variable_input = st.selectbox('Select variable to compare with Score:', options=['Genre', 'Setting', 'Perspective', 'Interface', 'Year'])

    # # Filter the dataframe based on the selected variable
    # if variable_input == "Setting":
    #     selected_option = st.selectbox(f"Select Setting:", options=data['Setting'].explode().unique())  # Explode setting lists for selection
    #     filtered_data = data[data['Setting'].apply(lambda x: selected_option in x)]
    # elif variable_input == "Perspective" or variable_input == "Interface":
    #     selected_option = st.selectbox(f"Select {variable_input}:", options=data[variable_input].unique())
    #     filtered_data = data[data[variable_input] == selected_option]
    # else:
    #     filtered_data = data.copy()

    # # Group by the selected variable and calculate the average score for each group
    # grouped_data = filtered_data.groupby(variable_input)['Score'].mean().reset_index()

    # # Create a bar plot to show the average score by the selected variable
    # fig = px.bar(grouped_data, x=variable_input, y='Score', title=f'Average Score by {variable_input}')

    # # Display the plot
    # st.plotly_chart(fig)





with tab2:
    st.write('Find games based on your (hopefully reasonable) selections.')
    genre_input = st.selectbox('Select Genre:', options=genre_options)  # Single genre selected
    gameplay_input = st.multiselect('Select Gameplay:', options=gameplay_options)  # Multiple gameplay options can be selected
    setting_input = st.radio('Select Setting:', options=setting_options, 
                             horizontal=True)  # Multiple settings can be selected


    # Create a slider to filter by critic score
    score_input = st.slider(
        "Select Minimum Critic Score:",
        min_value=70,  # Assuming critic scores are between 0 and 100
        max_value=100,
        value=90,  # Default value, can be adjusted as needed
        step=1,
    )

    # Ensure 'Critics' column is numeric
    data['Critics'] = pd.to_numeric(data['Critics'], errors='coerce')

    # Create a filtered copy of the data to avoid modifying the original data
    filtered_data = data.copy()

    # Filter by Genre (if a selection was made)
    if genre_input:
        filtered_data = filtered_data[filtered_data['Genre'].apply(lambda x: genre_input in x if isinstance(x, list) else False)]

    # Filter by Gameplay (if a selection was made)
    if gameplay_input:
        filtered_data = filtered_data[filtered_data['Gameplay'].apply(lambda x: any(game in x for game in gameplay_input) if isinstance(x, list) else False)]

    if setting_input:
        filtered_data = filtered_data[filtered_data['Setting'].apply(lambda x: setting_input in x if isinstance(x, list) else False)]

 
    # Check if filtered data is empty and display a message if so
    if filtered_data.empty:
        st.write("No games match the selected criteria.")
    else:
        filtered_data = filtered_data[filtered_data['Critics'] >= score_input]
        filtered_data = filtered_data.drop(columns = ['Score', 'Setting', 'Released'])
        st.subheader("Criterion Matches")
        st.write(f"Showing games with a critic score of {score_input}% or higher, matching selections:")
        st.dataframe(filtered_data)


with tab3:
    st.write("Find a game you know, if it's in this dataset. No typos and no guarantees.")
    game_name = st.text_input("Name of Game:", 'Celeste')
    name_filter = data[data['Title'] == game_name]
    st.dataframe(name_filter)