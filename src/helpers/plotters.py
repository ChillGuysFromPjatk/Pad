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
