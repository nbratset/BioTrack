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

    parser.add_argument('-r',
                        '--report',
                        type=str,
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
        metadata = metadata.loc[keep_samples]
        otu = otu.loc[keep_samples]

    # Create temporary filtered files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_otu_path = os.path.join(tmpdir, "otu_filtered.csv")
        tmp_meta_path = os.path.join(tmpdir, "metadata_filtered.csv")

        otu.to_csv(tmp_otu_path)
        metadata.to_csv(tmp_meta_path)

        # Call main.py and pass filtered files
        subprocess.run(
            [
                "python",
                "src/main.py",
                "--otu", tmp_otu_path,
                "--meta", tmp_meta_path
            ],
            check=True
        )


if __name__ == "__main__":
    main()

