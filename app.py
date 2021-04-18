# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import pandas as pd
import requests
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.express as px
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def model():
    data_url = "https://api.covid19india.org/data.json"
    data=requests.get(data_url).json()
    delta=pd.DataFrame(data.get('key_values'))
    cases_time_series=pd.DataFrame(data.get('cases_time_series'))
    cases_time_series[["dailyconfirmed","dailydeceased","dailyrecovered","totalconfirmed","totaldeceased","totalrecovered"]]=cases_time_series[["dailyconfirmed","dailydeceased","dailyrecovered","totalconfirmed","totaldeceased","totalrecovered"]].astype(int)
    cases_time_series["dateymd"]=pd.to_datetime(cases_time_series["dateymd"])
    cases_time_series.drop(['date'],axis=1,inplace=True)
    cases_time_series["WeekDays"]=cases_time_series["dateymd"].dt.day_name()

    fig = px.bar(cases_time_series, x='dateymd', y='dailyconfirmed',
                hover_data=['dailyconfirmed', 'dailydeceased','dailyrecovered','WeekDays'], color='dailydeceased',
                labels={'dailyconfirmed':'Daily covid +ve confirmed cases','dateymd':'Dates'},height=600,width=1400)
    return(fig)

app.layout = html.Div([html.H4(children='Daily covid +ve confirmed cases'),dcc.Graph(figure=model()),html.Footer(children='Data Source: covid19india, Designed by Ashish')])

if __name__ == '__main__':
    app.run_server(debug=True)