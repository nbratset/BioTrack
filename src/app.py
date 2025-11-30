import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px


def parse_csvs(taxa_otu_file, alpha_div_file, beta_pcoa_file):
    taxa_otu_df = pd.read_csv(taxa_otu_file, index_col=0)
    alpha_div_df = pd.read_csv(alpha_div_file, index_col=0)
    beta_pcoa_df = pd.read_csv(beta_pcoa_file, index_col=0)
    return taxa_otu_df, alpha_div_df, beta_pcoa_df


def parse_rf_export(rf_file):
    # import results/rf_report.txt
    # parses rf_report.txt
    pass


def plot_top_taxa():
    # plots top x (10 by default) taxa of the patient
    pass


def plot_alpha_diversity():
    # plots shannon and richness a div
    pass


def plot_pca():
    # plots PCA 1 and 2 from beta_div_coords file
    pass


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
    # fig = generate_example_fig()
    # table = generate_example_table(max_rows=5)

    # create_report(date, patient_id, [fig, table], dev_mode=True)


if __name__ == "__main__":
    main()
