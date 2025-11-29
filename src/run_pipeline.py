import argparse
import pandas as pd
import subprocess
import tempfile
import os
import sys


def main():
    parser = argparse.ArgumentParser(prog='BioTrack',
                                     description="Run microbiome analysis pipeline")  # noqa

    parser.add_argument("--location",
                        help="Location to limit the analysis to (optional)")

    parser.add_argument("--otu_file",
                        required=True,
                        help="Path to microbial abundance table")

    parser.add_argument("--metadata_file",
                        required=True,
                        help="Path to metadata file")
    
    parser.add_argument('--min_patients',
                        type=int,
                        help='Sets the threshold for minimum # patients when filtering by location (default=20)',  # noqa
                        default=20,
                        required=False)

    parser.add_argument('-r',
                        '--report',
                        type=bool,
                        help='Build a report document (optional).',
                        default=False,
                        required=False)

    parser.add_argument('-p',
                        '--patient_id',
                        type=str,
                        default='',
                        help='Patient name or ID for report (optional).',
                        required=False)

    args = parser.parse_args()

    # Load data
    try:
        otu = pd.read_csv(args.otu_file, index_col=0)
    except FileNotFoundError as e:
        print('Missing OTU File')
        sys.exit(0)
    try:
        metadata = pd.read_csv(args.metadata_file, index_col=0)
    except FileNotFoundError as e:
        print('Missing Metadata File')
        sys.exit(0)

    # Filter by location (if provided)
    if args.location:
        keep_samples = metadata[metadata["Location"] == args.location].index
        if len(keep_samples) >= args.min_patients:
            metadata = metadata.loc[keep_samples]
            otu = otu.loc[keep_samples]

    # Handle Patient ID (ignores if no report)
    if args.report:
        if args.patient_id == '':
            patient = otu[otu["Condition"] == 'Patient'].index.to_list()
            if len(patient) > 1:
                print('Check metadata file, multiple patients were found!')
                sys.exit(0)
            elif len(patient) == 0:
                print('Check metadata file, no patients found!')
                sys.exit(0)
            elif len(patient) == 1:
                patient_id = patient[0]
        else:
            patient_id = args.patient_id

    # Create temporary filtered files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_otu_path = os.path.join(tmpdir, "otu_filtered.csv")
        tmp_meta_path = os.path.join(tmpdir, "metadata_filtered.csv")

        otu.to_csv(tmp_otu_path)
        metadata.to_csv(tmp_meta_path)

        # Call main.py and pass filtered files
        if args.report:
            subprocess.run(["python",
                            "src/main.py",
                            "--otu", tmp_otu_path,
                            "--meta", tmp_meta_path,
                            "-r", True,
                            "-p", patient_id,
                            ],
                        check=True)
        else:
            subprocess.run(["python",
                            "src/main.py",
                            "--otu", tmp_otu_path,
                            "--meta", tmp_meta_path
                            ],
                        check=True)


if __name__ == "__main__":
    main()

