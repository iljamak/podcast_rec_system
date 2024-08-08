import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from pil_for_dash import get_pils
from PIL import Image
import dash_bootstrap_components as dbc
from quering_functions import find_closest_by_category,get_most_popular,get_sbert_top,get_avg_wiki_emb_top,text_to_recommendations
from quering_functions import get_optimal_recommendations
import pandas as pd
import numpy as np


#reading adn loading datasets to make them pointers-like and not loading them each time
dataset_main = pd.read_csv('datasets/podcasts.csv')
sbert_cos_sim = np.load('datasets/cos_sim_sbert.npy') #better, than BERT, so i sticked to it
wiki_avg_cos_sim = np.load("datasets/wiki_avg_cos_sim.npy") # suprisingly, works pretty well, adding a grain of
                                                            # freedom to topics

sbert_embeddings = np.load('datasets/sbert_embeddings.npy')
# f.e. this prompt: "podcast about scientific approach to health and biohacking"
# try yourself, good luck :D

external_stylesheets = ['/assets/styles.css'] # a folder, where css styles are stored

#i'm using dash, because i have some experience with it and its easy to make raw prototype
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Link(
                rel='stylesheet',
                href='/assets/styles.css',
            ),

        dcc.Dropdown(
            id='my_dropdown',
            options=[
                {"label": "Same category", "value": "1"},
                {"label": "Most popular", "value": "2"},
                {"label": "BERT embeddings(not implemented)", "value": "3"},
                {"label": "SBERT Embeddings(Best-2)", "value": "4"},
                {"label":"Avearged embedings from wikipedia", "value": "5"},
                {"label": "Optimal recommendations(Best-1)", "value": "6"},
                {"label": "Try to write what you want to listen to,just write it and press Recommend","value":"7"}

            ],
            value='1',
            style={'width': '300px', 'margin-bottom': '20px'}
        ),
        dcc.Input(
            id='my_input',
            type='text',
            placeholder='iTunes ID or podcast name',
            style={'width': '300px','height':'30px', 'margin-bottom': '20px'}
        ),
    ], style={'margin-bottom': '20px'}),
    html.Div([
        html.Button('Recommend', id='load_images_button',className='button', n_clicks=0)
    ], style={'text-align': 'center', 'margin-bottom': '20px',}),
    html.Div(
        id='image_container',
        children=[],
        # Set your container to be a flexbox with wrap
        style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'flex-start'}
    ),
], style={'width': '80%', 'max-width': '1000px', 'margin': 'auto', 'padding': '20px'})

@app.callback(
    Output('image_container', 'children'),
    [Input('load_images_button', 'n_clicks')],
    [State('my_dropdown', 'value'),
     State('my_input', 'value')]
)
def update_output(n_clicks, dropdown_value, input_value):
    print(n_clicks)
    if dropdown_value == "1":
        try:
            input_value = str(input_value).strip()
            df = find_closest_by_category(input_value,dataset_main,10) # can throw FileNotFoundError
        except Exception as e:
            print(e)
            df = None
    elif dropdown_value == "2":
        df = get_most_popular(dataset_main,10)
    elif dropdown_value == "4":
        try:
            input_value = str(input_value).strip()
            df = get_sbert_top(dataset_main,input_value,sbert_cos_sim)
        except:
            df = None
    elif dropdown_value == "5":
        try:
            input_value = str(input_value).strip()
            df = get_avg_wiki_emb_top(dataset_main,input_value,wiki_avg_cos_sim)
        except:
            df = None
    elif dropdown_value == "6":
        try:
            input_value = str(input_value).strip()
            df = get_optimal_recommendations(dataset_main,sbert_cos_sim,input_value)
        except:
            df = None
    elif dropdown_value == "7":
        try:
            input_value = str(input_value).strip()
            df = text_to_recommendations(dataset_main,sbert_embeddings,input_value)
        except:
            df = None
    else:
        df = None
    pils = get_pils(df)  # Replace with actual function to get image sources
    # Adjust the width of each image container to be 20% (1/5) of the parent container
    # Assuming 5 images per row, so 20% each
    children = [
        html.Div([
            html.Img(src=pils[i][0], style={'width': '100%', 'height': 'auto'}),
            html.P(pils[i][1], style={'text-align': 'center'},className='text-below')
        ], style={'width': '18%', 'margin': '1%'})  # Adjust margins to fit 5 per row
        for i in range(10)
    ]
    return children


#app.css.append_css({"external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"})
if __name__ == '__main__':
    app.run_server(debug=True)
