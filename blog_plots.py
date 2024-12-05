import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd



import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def genre_trend_plot(df, genre='Action', width=800, height=600):
    # Filter the data by genre
    genre_data = df[df['Genre'].apply(lambda x: genre in x)].copy()  # Assuming Genre is a list
    color_map = {True: "#636EFA", False: "#EF553B"}  # Color map for score (e.g., True = good score, False = low score)

    if genre_data.empty:
        print(f"Genre '{genre}' not found in the dataset.")
    else:
        # Group by Year and Genre, and calculate total counts
        yearly_counts = genre_data.groupby(['Year', 'Genre']).size().unstack(fill_value=0)
        
        # Calculate average score per year and genre
        avg_score = genre_data.groupby(['Year', 'Genre'])['Score'].mean().unstack(fill_value=0)
        
        # Calculate score-based coloring (e.g., color intensity based on score)
        color_scale = ['#EF553B', '#636EFA']  # From red (low) to blue (high)

        # Create subplots with shared x-axis
        fig = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            subplot_titles=("Total Game Count Over Time", "Average Score Over Time")
        )

        # Add total count plot
        fig.add_trace(
            go.Scatter(x=yearly_counts.columns, y=yearly_counts.sum(axis=0), mode='lines', name='Total Count', line=dict(color="gray")),
            row=1, col=1
        )

        # Add average score plot with color based on score
        for i, genre in enumerate(yearly_counts.columns):
            fig.add_trace(
                go.Scatter(
                    x=avg_score.index,
                    y=avg_score[genre],
                    mode='lines+markers',
                    name=genre,
                    line=dict(color=color_map[avg_score[genre] > 5]),  # Assuming score > 5 is good
                    marker=dict(color=avg_score[genre], colorscale=color_scale, size=10)
                ),
                row=2, col=1
            )

        # Update layout
        fig.update_layout(
            title=f"Genre Trend and Score Distribution for '{genre}'",
            xaxis_title="Year",
            yaxis_title="Total Count",
            yaxis2_title="Average Score",
            height=height,
            width=width,
        )

        return fig
