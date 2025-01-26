import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.graph_objs._figure import Figure


def _get_default_styles(fig: Figure, bg_color: str ="rgb(40,40,40)",
                        font_color: str = "white") -> Figure:
    fig.update_layout(
        template='seaborn',
        paper_bgcolor=bg_color,
        title_font=dict(size=24, family='Arial', color=font_color),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=14, color=font_color)
        )
    )
    fig.update_traces(
        textfont=dict(color=font_color, size=10),
    )
    return fig


def plotly_pie(df: pd.DataFrame, values: str, names: str, title: str):
    fig = px.pie(
        df, values=values, names=names, title=title,
    )
    fig = _get_default_styles(fig)
    fig.update_traces(
        textinfo='percent+label'
    )
    fig.show()


def plotly_bar(df: pd.DataFrame,x_axis: str, y_axis: str, title: str,
               x_axis_title: str, y_axis_title: str, font_color: str = "white"):
    fig = px.bar(
        df, x=x_axis, y=y_axis, title=title,
    )
    fig = _get_default_styles(fig)
    fig.update_layout(
    xaxis=dict(
        title=x_axis_title,
        tickfont=dict(size=14, color=font_color),
        titlefont=dict(size=16, color=font_color)
    ),
    yaxis=dict(
        title=y_axis_title,
        tickfont=dict(size=14, color=font_color),
        titlefont=dict(size=16, color=font_color)
    ),
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        font=dict(size=14, color=font_color)
    ))
    fig.show()


def plot_corr_matrix(df: pd.DataFrame, fig_width: int = 8, fig_height: int = 10):
    corr = df.corr()
    plt.figure(figsize=(fig_width, fig_height))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar=True,
        linewidths=0.5
    )
    plt.title("Macierz korelacji zmiennych z 'price_pln'", fontsize=16)
    plt.show()

def create_box_plot(selected_producer='All', selected_model_group='All', selected_arg='collectible'):
    filtered_df = df.copy()
    if selected_producer != 'All':
        filtered_df = filtered_df[filtered_df['producer'] == selected_producer]

    if selected_model_group != 'All':
        filtered_df = filtered_df[filtered_df['model_group'] == selected_model_group]
    
    if filtered_df.empty:
        fig = px.box()
        fig.add_annotation(text="No data available for the selected filters.",
                           xref="paper", yref="paper",
                           showarrow=False,
                           font=dict(size=20))
    else:
        fig = px.box(filtered_df, x=selected_arg, y='price_pln',
                     title=f'Comparison of Sale Prices of {selected_model_group} consoles by {selected_producer} by Value of an Argument "{selected_arg}"',
                     labels={selected_arg: selected_arg, 'price_pln': 'Price (PLN)'})
    
    fig.show()

def create_pie_chart(selected_producer='All', selected_model_group='All', selected_arg='collectible'):
    filtered_df = df.copy()
    if selected_producer != 'All':
        filtered_df = filtered_df[filtered_df['producer'] == selected_producer]

    if selected_model_group != 'All':
        filtered_df = filtered_df[filtered_df['model_group'] == selected_model_group]
    
    if not filtered_df.empty:
        fig = px.pie(filtered_df, names=selected_arg,
                     title=f'Volume of Sales of {selected_model_group} consoles by {selected_producer} by Value of an Argument "{selected_arg}"',
                     hole=0.3)
        fig.show()
    else:
        print("No data available for the selected filters.")

def create_histogram(selected_producer='All', selected_model_group='All', selected_arg='None', selected_val='None'):
    filtered_df = df.copy()
    if selected_producer != 'All':
        filtered_df = filtered_df[filtered_df['producer'] == selected_producer]

    if selected_model_group != 'All':
        filtered_df = filtered_df[filtered_df['model_group'] == selected_model_group]
        
    if selected_arg != 'None' and selected_val != 'None':
        filtered_df = filtered_df[filtered_df[selected_arg] == selected_val]

    if not filtered_df.empty:
        fig = px.histogram(filtered_df, x='price_pln', nbins=500,
                           title=f'Distribution of Sale Prices of {selected_model_group} consoles by {selected_producer} when "{selected_arg}" = "{selected_val}"',
                           labels={'price_pln': 'Price (PLN)'})
                           #marginal='rug')  # Optional: adds a rug plot
        fig.show()
    else:
        print("No data available for the selected filters.")

def create_scatter_plot(selected_arg='seller_score'):
    if not df.empty:
        fig = px.scatter(df, x='price_pln', y=selected_arg,
                         title=f'Scatter Plot of Price vs "{selected_arg}"',
                         labels={'price_pln': 'Price (PLN)', selected_arg: selected_arg})
        fig.update_traces(marker=dict(size=5))
        fig.show()
    else:
        print("No data available.")