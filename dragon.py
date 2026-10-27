# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "dragonfipy",
#     "iragca[matplotlib]",
#     "seaborn"
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    import matplotlib.pyplot as plt
    import seaborn as sns
    from iragca.matplotlib import Styles, Color
    plt.style.use(Styles.CMR10.value)
    return Color, mo, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # DragonPy

    [DragonPy](https://github.com/iragca/dragonpy) is a lightweight [dragonfi.ph](https://dragonfi.ph/) API wrapper for Python. Recommended for Analysts and Scientists and great for personal use.


    DragonFi exposes most of their API for free without authentication. **Please do not abuse their API**.
    The maintainer(s) of this Python package are not liable for any malicious or abusive acts done.

    ## Installation

    You can install the package with your favorite Python package manager [pip](https://pip.pypa.io/en/stable/installation/) or [uv](https://docs.astral.sh/uv/getting-started/installation/#installation-methods).
    - `pip install dragonfipy`
    - `uv add dragonfipy`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Usage

    Although the PyPi package name is `dragonfipy` (an existing package has used `dragonpy` as a package name 🥲) it can be imported with:
    """)
    return


@app.cell
def _():
    from dragonpy import DragonPy
    dpy = DragonPy()
    return (dpy,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As an example, let's see what we can do with DragonPy by looking at [ABS-CBN](https://www.abs-cbn.com/)'s (ticker: ABS) stock data (or change to another ticker of your choice).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    ticker = mo.ui.text("ABS", "Ticker name", label="Ticker")
    ticker
    return (ticker,)


@app.cell
def _(dpy, ticker):
    stock_profile = dpy.securities.get_stock_profile(ticker.value)
    stock_profile["description"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some data and functionalities are categorized in their own respective services. Stocks belong to `DragonPy.securities` or Funds belong to `DragonPy.funds`.
    Prices can be retrieved from `DragonPy.dashboard.get_delayed_bars()` regardless if you want to retrieve Stock or Fund price data.
    """)
    return


@app.cell
def _(dpy, ticker):
    data = dpy.dashboard.get_delayed_bars(ticker.value, candleType="1D")
    len(data["events"])
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We retrieved data worth 252 days from the API.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plotting the data

    Now we have retrieved our data. We can start plotting it.
    """)
    return


@app.cell(hide_code=True)
def _(data, mo):
    date_range = mo.ui.range_slider(
        start=min(data["events"], key=lambda x: x["timeinSeconds"])[
            "timeinSeconds"
        ],
        stop=max(data["events"], key=lambda x: x["timeinSeconds"])[
            "timeinSeconds"
        ],
        step=1,
        label="Date (in seconds)",
    )
    date_range
    return (date_range,)


@app.cell
def _(Color, data, date_range, plt, sns, ticker):
    from datetime import date

    dates = [date.fromtimestamp(d["timeinSeconds"]) for d in data["events"]]
    closing_prices = [d["close"] for d in data["events"]]
    low_prices = [d["high"] for d in data["events"]]
    high_prices = [d["low"] for d in data["events"]]
    volume = [d["volume"] for d in data["events"]]

    fig, (ax_price, ax_volume) = plt.subplots(
        2, 1,
        figsize=(14, 7),
        sharex=True,
        gridspec_kw={"height_ratios": [3, 1]},
    )

    plt.xlabel("Date")
    ax_price.set_ylabel(f"{ticker.value} (PHP)")
    ax_volume.set_ylabel("Volume")
    plt.xticks(rotation=30)
    start, end = date.fromtimestamp(date_range.value[0]), date.fromtimestamp(date_range.value[1])
    plt.xlim((start, end))
    sns.lineplot(ax=ax_price, x=dates, y=low_prices, color=Color.PUSH_TO_BG)
    sns.lineplot(ax=ax_price, x=dates, y=high_prices, color=Color.PUSH_TO_BG)
    sns.lineplot(ax=ax_price, x=dates, y=closing_prices)
    sns.lineplot(ax=ax_volume, x=dates, y=volume)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's it! There is more to DragonPy but full feature-parity with the real API isn't a priority currently but DragonPy is designed to be extensible. So feel free to request features or submit your pull request contributions on the project [GitHub](https://github.com/iragca/dragonpy).
    """)
    return


if __name__ == "__main__":
    app.run()
