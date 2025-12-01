import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import sys


def parse_csvs(taxa_otu_file, alpha_div_file, beta_pcoa_file):
    '''Converts 3 primary csvs to dataframes for later plotting.'''
    try:
        taxa_otu_df = pd.read_csv(taxa_otu_file, index_col=0)
    except FileNotFoundError as e:
        print('Missing Taxa/OTU File')
        sys.exit(0)
    try:
        alpha_div_df = pd.read_csv(alpha_div_file, index_col=0)
    except FileNotFoundError as e:
        print('Missing alpha diversity File')
        sys.exit(0)
    try:
        beta_pcoa_df = pd.read_csv(beta_pcoa_file, index_col=0)
    except FileNotFoundError as e:
        print('Missing beta diversity File')
        sys.exit(0)
    return taxa_otu_df, alpha_div_df, beta_pcoa_df


def parse_rf_export(rf_file):
    prediction = ''
    line_list = []
    with open(rf_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_list.append(line)
            split = line.strip().split("'")
            if 'Predictions: [' in split:
                prediction = split[1]
    if prediction == '':
        print(f'Cannot find prediction in {rf_file}')
    else:
        return prediction

def get_patient(df):
    '''Gets patient identifier for later searching in the csvs'''
    patient = df[df["Condition"] == 'Patient'].index.to_list()
    if len(patient) > 1:
        print('Check metadata file, multiple patients were found!')
        sys.exit(0)
    elif len(patient) == 0:
        print('Check metadata file, no patients found!')
        sys.exit(0)
    elif len(patient) == 1:
        return patient[0]


def plot_top_taxa(df, patient):
    '''Plots a pie chart of the top 10 taxa.'''
    taxa_list = df.loc[patient].head(10)  # filter by patient and top 10 taxa
    filtered_df = pd.DataFrame(taxa_list)  # convert back to a dataframe
    fig = px.pie(filtered_df,
                 values=patient,
                 names=filtered_df.index,
                 title=f'Pie Chart of {patient} Top 10 Taxa',
                 hole=.3)
    return fig


def plot_alpha_diversity(df, type):
    '''Plots a boxplot of alpha diversity.
       You can choose between Shannon or Simpson with the type variable.'''
    fig = px.box(df,
                 x=type,
                 y='Condition',
                 color='Condition',
                 title=f'{type} Alpha Diversity Per Condition')
    fig.update_xaxes(title_text=f'Alpha Diversity ({type})') 
    return fig


def plot_pca(df):
    '''Plots PC1 and PC2'''
    df['markersize'] = 1
    fig = px.scatter(df, x='PC1', y='PC2', color='Condition', color_discrete_map={'Patient': 'red', 'Healthy control': 'green', 'Ulcerative colitis':'blue', "Crohn's disease": 'purple'}, size='markersize')
    fig.data = fig.data[::-1]
    fig.write_html("interactive_plot.html")
    return fig


def plot_diff_abundance():
    # plots differential abundance info?
    pass


def generate_example_fig():
    ''' This is an example figure from the dash documentation for testing.'''
    df = pd.DataFrame({"Fruit": ["Apples", "Oranges",
                                 "Bananas", "Apples",
                                 "Oranges", "Bananas"],
                       "Amount": [4, 1, 2, 2, 4, 5],
                       "City": ["SF", "SF", "SF", "Montreal",
                                "Montreal", "Montreal"]})
    fig = px.bar(df,
                 x="Fruit",
                 y="Amount",
                 color="City",
                 barmode="group")
    return fig


def generate_example_table(max_rows=10):
    ''' This is an example table from the dash documentation for testing.'''
    dataframe = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv',  # noqa
                            index_col=0,
                            usecols=[0, 1, 2, 3, 4])
    table = html.Table([html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),  # noqa
                       html.Tbody([html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))])])  # noqa
    return table


def create_report(date, patient_id, data, dev_mode=False):
    ''' Creates an interactive dashboard when run.
        You can access this dashboard at:
            http://127.0.0.1:8050/ (this is a local address)
        Right click on the dashboard to save or print to PDF.
    '''
    fig = data[0]
    table = data[1]

    disclaimer = '''This report was generated using BioTrack,
                an open-source gut microbiome analysis software.
                DISCLAIMER: This report does not provide medical advice.
                The information in this report is intended to be
                reviewed by a medical professional and cannot
                independently provide medical diagnoses. Always seek
                the advice of your physician or medical health provider
                for an official diagnosis and treatment information.'''

    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = html.Div([
        # Title
        html.H1("Gut Microbiome Report"),
        # Patient name and date
        html.Div(children=[html.H3(f"{patient_id}"), html.P(f"{date}")],
                 style={'margin-top': 10,
                        'display': 'flex',
                        'justifyContent': 'space-around',
                        'alignItems': 'center'}),
        # Summary
        html.Div(html.H2("Summary")),

        html.Div(html.H3(children='US Agriculture Exports (2011)')),
        html.Div(table,
                 style={'margin-left': 10,
                        'display': 'flex',
                        'align': 'center'}),
        # Taxa Block
        html.Div(html.H2("Patient's Top 10 Taxa")),
        # Example Plotly Integration
        dcc.Graph(id='example-graph', figure=fig),

        # Alpha Block
        html.Div(html.H2("Patient Alpha Diversity Compared to the Model")),
        # Example Plotly Integration
        dcc.Graph(id='example-graph', figure=fig),

        # PCOA Block
        html.Div(html.H2("Patient PCA Compared to the Model")),
        # Example Plotly Integration
        dcc.Graph(id='example-graph', figure=fig),

        # Model Statistics Block
        html.Div(html.H2("Model Statistics")),
        # Example Plotly Integration
        dcc.Graph(id='example-graph', figure=fig),

        # Footer - Disclaimer
        html.Div(html.H5(f"{disclaimer}"))

        ], className='report-container')

    app.run(debug=dev_mode, port=8050)


def main():
    '''This main runs on the example data for testing/building the report.'''
    # add argparse here

    patient_id = 'John Doe'
    date = '11/25/2025'
    taxa_file = 'input_data/otu.csv'
    alpha_file = 'results/alpha_diversity.csv'
    beta_file = 'results/beta_diversity_coords.csv'

    taxa, alpha, beta = parse_csvs(taxa_file, alpha_file, beta_file)
    id = get_patient(alpha)
    prediction = parse_rf_export('results/rf_report.txt')

    # fig = plot_top_taxa(taxa, id)
    # fig = plot_alpha_diversity(alpha, 'Shannon')
    # fig = plot_alpha_diversity(alpha, 'Simpson')
    fig = plot_pca(beta)
    # Examples
    # fig = generate_example_fig()
    table = generate_example_table(max_rows=5)

    # create_report(date, patient_id, [fig, table], dev_mode=True)


if __name__ == "__main__":
    main()
