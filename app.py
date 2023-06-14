import pandas as pd
from dash import Dash, dcc, html
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests 
import base64
from API import predict_image

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY], suppress_callback_exceptions=True)

server = app.server

gif_path = "/Users/alya/code/AtinDhawan/DOG_IDENTIFIER/Assets/loading.gif"

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
            "Who's that doggie in the window?",
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
                                    'font-family': 'Verdana'
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
                            'Find the breed!',
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
                html.Div(id='api-text', children=html.P('API Response Text')),
                html.Div(id='output-data')
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
    if n_clicks > 0:
        gif_path = '/assets/loading.gif'  # Update with the correct path relative to the assets directory
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
    Output('loading-animation', 'style'),
    Output('api-text', 'style'),
    Input('api-response', 'children')
)

def update_visibility(api_response):
    loading_animation_style = {'display': 'none'}
    api_text_style = {'display': 'none'}
    
    if api_response is not None:
        loading_animation_style = {'display': 'none'}
        api_text_style = {'display': 'block'}
    
    return loading_animation_style, api_text_style

@app.callback(
    Output('output-data', 'children'),
    [Input('process-file-btn', 'n_clicks')],
    [State('upload-image', 'contents'),
     State('upload-image', 'filename')]
)

def process_file(n_clicks, contents, filenames):
    if n_clicks > 0 and contents and filenames:
        corrected_images = []
        output_children = []  # Initialize the output_children list
        
        for content, filename in zip(contents, filenames):
    # Append the loading animation to the output_children list
            output_children.append(
        html.Div([
            html.Img(
                src=gif_path,
                style={'height': '100px', 'width': '100px'}
            ),
            html.H5("Processing Image...")
        ],
        style={'textAlign': 'center', 'margin-top': '20px'})
    )
            
            # Save the uploaded image to a file
        with open(filename, 'wb') as f:
                f.write(content.encode('utf8'))
            
            # Make the API request to correct the image
        response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(filename, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': 'WuhU7hKwGiPcMWn4HZFSVfo9'},
            )
            
        if response.status_code == 200:
                # Save the corrected image to a file
                corrected_filename = f'corrected_{filename}'
                with open(corrected_filename, 'wb') as out:
                    out.write(response.content)
                
                corrected_images.append(corrected_filename)
                
                api_text = response.json().get('text')
                
                output_children.append(html.P(api_text))
        
        if corrected_images:
            output_children += [
                html.Div([
                    html.H5("Corrected Image"),
                    html.Img(src=corrected_image),
                    html.Hr()
                ]) for corrected_image in corrected_images
            ]
        else:
            output_children = html.Div("Error occurred during image correction")
        
        return output_children
    
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    