import plotly.graph_objects as go


def plot_line(
    df,
    y,
    data_slice,
    title="Bitcoin Close Price",
    x_title="Timestamp",
    y_title="Close Price (USD)",
):
    """
    Строит линию цены
    """
    sliced_df = df[data_slice]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=sliced_df["Timestamp"],
            y=sliced_df[y],
            mode="lines",
            line=dict(color="blue"),
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_white",
        hovermode="x unified",
    )

    return fig


def plot_bars(
    df,
    data_slice,
    title="Bitcoin Close Price",
    x_title="Timestamp",
    y_title="Close Price (USD)",
    autosize=True,
    slider=False,
):
    """
    Строит свечной график

    Параметры:
    df - DataFrame с данными
    data_slice - срез данных (например, -240:)
    title - заголовок графика
    x_title - название оси X
    y_title - название оси Y
    autosize - автоматический подбор размера
    slider - отображать ли слайдер диапазона
    """
    fig = go.Figure()

    sliced_df = df[data_slice]

    fig.add_trace(
        go.Candlestick(
            x=sliced_df["Timestamp"],
            open=sliced_df["Open"],
            high=sliced_df["High"],
            low=sliced_df["Low"],
            close=sliced_df["Close"],
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_white",
        hovermode="x unified",
        autosize=autosize,
        xaxis_rangeslider_visible=slider,
    )

    return fig


def time_series_split(df, train_size=0.6, test_size=0.2, oot_size=0.2):
    """
    Делит временной ряд на TRAIN / TEST / OOT по заданным долям.

    train_size + test_size + oot_size должно быть равно 1.0
    """
    n = len(df)
    train_end = int(n * train_size)
    test_end = train_end + int(n * test_size)

    train_df = df.iloc[:train_end]
    test_df = df.iloc[train_end:test_end]
    oot_df = df.iloc[test_end:]

    for name, df in zip(["TRAIN", "TEST", "OOT"], [train_df, test_df, oot_df]):
        start = df["Timestamp"].iloc[0]
        end = df["Timestamp"].iloc[-1]
        print(f"{name}: {start} → {end}")

    return train_df.copy(), test_df.copy(), oot_df.copy()
