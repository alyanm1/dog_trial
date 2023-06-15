from dash import dcc, html
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64
from PIL import Image
import io
from io import BytesIO, BufferedReader
from io import BytesIO
import numpy as np
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True)

server = app.server

gif_path = "assets/loading.gif"

app.layout = html.Div(
    [
        
        html.Div(
            [
                html.Img(
                    src=dash.get_asset_url('Logo.png'),
                    style={'height': '40%', 'width': '40%'}
                )
            ],
            style={'textAlign': 'center'}
        ),
        html.H4(
            "What's that doggie in the window?",
            style={
                'text-align': 'center',
                'font-family': 'Gill Sans',
                'font-size': '32px',
                'color': '#F79D59',
                'font-weight':'bold'
            }
        ),
        html.P(" "),
        html.Div(
            [
                dbc.Container(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "File Upload",
                                style={
                                    'background-color': '#bde6d3',
                                    'color': 'white',
                                    'font-family': 'Verdana',
                                    'text-align': 'center',
                                    'font-weight':'bold'
                                }
                            ),
                            dbc.CardBody(
                                html.Div(
                                    [
                                        dcc.Upload(
                                            id="upload-image",
                                            children=html.Div(
                                                id='upload-content',
                                                style={'width': '100%', 'height': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
                                            ),
                                            style={
                                                'font-family': 'Trebuchet MS',
                                                'color': 'white',
                                                'height': '200px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'solid',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin' : '2px',
                                                'background-color': '#FFFFFF',
                                                'font-family': 'Verdana',
                                                'width': '80%',
                                                'margin': 'auto'
                                            },
                                            multiple=True,
                                            className="upload-box",
                                            accept='image/*',
                                        ),
                                        
                                    ],
                                    className='custom-upload-box'
                                )
                            ),
                            
                        ],
                        className='theme-card',
                        style={'margin-bottom': '20px', 'font-family': 'Verdana'}
                    )
                ),
                html.Div(
                    [
                        dbc.Button(
                            'Send my photo!',
                            color='primary',
                            id='process-file-btn',
                            n_clicks=0
                        )
                    ],
                    style={
                        'display': 'flex',
                        'justify-content': 'center',
                        'margin-bottom': '20px',
                        'font-family': 'Verdana'
                    }
                ),
                html.Div(
                    id='loading-animation',
                    style={'textAlign': 'center', 'margin-top': '20px'}
                ),
                html.Div(
                    [
                        dbc.Button(
                            'Tell me the breed!',
                            color='primary',
                            id='api-btn',
                            n_clicks=0
                        )
                    ],
                    style={
                        'display': 'flex',
                        'justify-content': 'center',
                        'margin-bottom': '20px',
                        'font-family': 'Verdana'
                    }
                ),
                html.Div(id='api-text', children=html.P('Made by. Happy Hippos')),
                html.Div(id='output-data',
                         style={
                'text-align': 'center',
                'font-family': 'Verdana',
                'font-size': '45px',
                'color': '#007864',
                'font-weight':'bold'
            })
            ]
        )
    ]
)
            
def parse_contents(contents, filename):
    return html.Div(
        [
            html.Div(
                html.Img(src=contents, style={'max-width': '100%', 'max-height': '100%', 'width': 'auto', 'height': 'auto'}),
                style={'width': '100%', 'height': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'overflow': 'hidden'}
            ),
            html.Hr()
        ],
        style={'width': '100%', 'height': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}
    )


@app.callback(
    Output('upload-content', 'children'),
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename'),
     State('upload-image', 'last_modified')],
    prevent_initial_callback=True
)
def process_image(contents, filenames, last_modified):
    if contents is not None and filenames is not None:
        output_children = [
            parse_contents(content, filename) for content, filename in zip(contents, filenames)
        ]
        return output_children

    return []

@app.callback(
    Output('loading-animation', 'children'),
    Input('process-file-btn', 'n_clicks')
)

def update_loading_animation(n_clicks):
    print("update_loading_animation", n_clicks)
    if n_clicks % 2 == 1:
        #gif_path = gif_path  # Update with the correct path relative to the assets directory
        return html.Div(
            [
                html.Img(
                    src=gif_path,
                    style={'height': '200px', 'width': '200px'}
                ),
                html.H5("Identifying the breed...")
            ],
            style={'textAlign': 'center', 'margin-top': '20px'}
        )
    else:
        return html.Div()

@app.callback(
    Output('output-data', 'children'),
    [Input('api-btn', 'n_clicks')],
    [State('upload-image', 'contents'),
     State('upload-image', 'filename')]
)

def process_file(n_clicks, contents, filenames):
    print("hide imag", n_clicks)
    
    if n_clicks > 0:
        update_loading_animation(0)
    
    if n_clicks > 0 and contents and filenames:
        output_children = []  # Initialize the output_children list
        
        for content, filename in zip(contents, filenames):
   
            with open(filename, 'wb') as f:
                    f.write(content.encode('utf8'))
            
        bytes = base64.b64decode(content.split(',')[1]) 

        img = Image.open(io.BytesIO(bytes))
        

        img = img.resize((224, 224))
        arr = np.array(img)
        arr_shape = str(arr.shape)
        arr_dtype = str(arr.dtype)
        arr_bytes = arr.tobytes()
        files = {"my_file": arr_bytes}
        data_dic = {'shape': arr_shape, "dtype": arr_dtype}
        
        output = requests.post("https://dog-pred-nq4ekl2z7q-nw.a.run.app/predict", data = data_dic, files = files)
        
        word_in_string = eval(output.json()["response"])
        if len(word_in_string) == 1:
            final = word_in_string
            output_children = html.Div(f"This dog is a {final[0]}!")
        else:
            final = ", ".join(word_in_string[::-1])
            output_children = html.Div(f"These dogs are {final}!")
        
        return output_children
    
    return []

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
    
    
    
    