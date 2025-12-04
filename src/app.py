import argparse
from datetime import date
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import sys


def parse_csvs(taxa_otu_file, alpha_div_file, beta_pcoa_file, diff_file):
    '''Converts 3 primary csvs to dataframes for later plotting.'''
    try:
        taxa_otu_df = pd.read_csv(taxa_otu_file, index_col=0)
    except FileNotFoundError:
        print('Missing Taxa/OTU File')
        return 'Missing Taxa/OTU File'
        # sys.exit(0)
    try:
        alpha_div_df = pd.read_csv(alpha_div_file, index_col=0)
    except FileNotFoundError:
        print('Missing alpha diversity File')
        return 'Missing alpha diversity File'
        # sys.exit(0)
    try:
        beta_pcoa_df = pd.read_csv(beta_pcoa_file, index_col=0)
    except FileNotFoundError:
        print('Missing beta diversity File')
        return 'Missing beta diversity File'
        # sys.exit(0)
    try:
        diff_df = pd.read_csv(diff_file, index_col=0)
    except FileNotFoundError:
        print('Missing Differential Abundance File')
        return 'Missing Differential Abundance File'
        # sys.exit(0)
    return taxa_otu_df, alpha_div_df, beta_pcoa_df, diff_df


def parse_rf_export(rf_file):
    prediction = ''
    line_list = []
    try:
        file = open(rf_file, 'r', encoding='utf-8')
    except FileNotFoundError:
        print('Cannot find RF_report File!')
        sys.exit(0)
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
    fig = px.scatter(df,
                     x='PC1',
                     y='PC2',
                     color='Condition',
                     color_discrete_map={
                         'Patient': 'red',
                         'Healthy control': 'green',
                         'Ulcerative colitis': 'blue',
                         "Crohn's disease": 'purple'})
    fig.data = fig.data[::-1]
    return fig


def plot_diff_abundance(df):
    fig = px.bar(df, x=df.index, y='Diff')
    fig.update_xaxes(title_text=f'Taxa')
    fig.update_yaxes(title_text=f'Abundance (Healthy - Disease)')
    return fig


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


def generate_table(dataframe, max_rows=10):
    ''' This is an example table from the dash documentation for testing.'''
    table = html.Table([html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])),  # noqa
                       html.Tbody([html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))])])  # noqa
    return table


def create_report(date, patient_name, id, result,
                  taxa, alpha, beta, diff, dev_mode=False):
    ''' Creates an interactive dashboard when run.
        You can access this dashboard at:
            http://127.0.0.1:8050/ (this is a local address)
        Right click on the dashboard to save or print to PDF.
    '''

    disclaimer = '''This report was generated using BioTrack,
                an open-source gut microbiome analysis software.
                DISCLAIMER: This report does not provide medical advice.
                The information in this report is intended to be
                reviewed by a medical professional and cannot
                independently provide medical diagnoses. Always seek
                the advice of your physician or medical health provider
                for an official diagnosis and treatment information.'''

    summary = f'''Patient's Health Prediction: {result}'''

    app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
    app.layout = html.Div([
        html.H5(f"Generated on {date} using BioTrack",
                style={'color': '#ffffff'}),
        # Title
        html.H1("Gut Microbiome Report"),

        # Summary
        html.Div(html.H2("Summary")),
        html.Div(children=[html.P(f"Patient: {patient_name} ({id})"),
                           html.P(f"Date:{date}")]),
        html.P(f"{summary}"),

        # Taxa Block
        html.Div(html.H2("Patient's Top 10 Taxa")),
        dcc.Graph(id='Top Taxa', figure=plot_top_taxa(taxa, id)),

        # Alpha Block
        html.Div(html.H2("Patient Alpha Diversity Compared to the Model")),
        dcc.Graph(id='Shannon', figure=plot_alpha_diversity(alpha, 'Shannon')),
        dcc.Graph(id='Simpson', figure=plot_alpha_diversity(alpha, 'Simpson')),

        # PCOA Block
        html.Div(html.H2("PCoA Plot (Bray-Curtis)")),
        dcc.Graph(id='PCA Plot', figure=plot_pca(beta)),

        # Diff Abundance
        html.Div(html.H2("Differential Abundance")),
        dcc.Graph(id='Differential Abundance',
                  figure=plot_diff_abundance(diff)),

        # Footer - Disclaimer
        html.Div(html.H2("Additional Info")),
        html.Div(html.H5(f"{disclaimer}"))

        ], className='report-container')

    app.run(debug=dev_mode, port=8050)


def main():
    '''This main runs on the example data for testing/building the report.'''
    today = date.today()
    parser = argparse.ArgumentParser(description='Generates a report',
                                     prog='BioTrack_app')
    parser.add_argument('-n',
                        '--patient_name',
                        type=str,
                        help='Enter Patient Name or ID.',
                        required=True)

    parser.add_argument('-t',
                        '--taxa_file',
                        type=str,
                        help='Enter otu.csv path.',
                        default='input_data/otu.csv',
                        required=False)

    parser.add_argument('-a',
                        '--alpha_file',
                        type=str,
                        help='Enter path to alpha diversity file.',
                        default='results/alpha_diversity.csv',
                        required=False)

    parser.add_argument('-b',
                        '--beta_file',
                        type=str,
                        help='Enter path to beta diversity/PCoA file.',
                        default='results/beta_diversity_coords.csv',
                        required=False)

    parser.add_argument('-d',
                        '--diff_file',
                        type=str,
                        help='Enter path to differential abundance file.',
                        default='results/differential_abundance_top_20.csv',
                        required=False)

    parser.add_argument('--date',
                        type=str,
                        help='Date of report generation, defaults to today.',
                        default=f'{today.strftime("%m/%d/%Y")}',
                        required=False)

    args = parser.parse_args()

    taxa, alpha, beta, diff = parse_csvs(args.taxa_file,
                                         args.alpha_file,
                                         args.beta_file,
                                         args.diff_file)
    id = get_patient(alpha)
    prediction = parse_rf_export('results/rf_report.txt')
    create_report(args.date, args.patient_name, id, prediction,
                  taxa, alpha, beta, diff)


if __name__ == "__main__":
    main()
