import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import sqlite3

conn = sqlite3.connect("heb_prices.db")
cursor = conn.cursor()

cursor.execute("SELECT item, price, date FROM prices")
prices = cursor.fetchall()

app = dash.Dash()

fig = px.line(prices, x="date", y="price", color="item")

table = html.Table([
    html.Tr([html.Th("Item"), html.Th("Price"), html.Th("Date")])
] + [
    html.Tr([html.Td(price[0]), html.Td(price[1]), html.Td(price[2])]) for price in prices
])

app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.Hr(),
    table
])

app.run_server(debug=True)

conn.close()
