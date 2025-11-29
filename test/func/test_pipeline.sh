test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_args python src/run_pipeline.py --location Netherlands --otu_file input_data/otu.csv --metadata_file input_data/combined_metadata.csv
assert_no_error

run test_bad_otu_file python src/run_pipeline.py --location Netherlands --otu_file input_data/bad_file.csv --metadata_file input_data/combined_metadata.csv
assert_exit_code 0
assert_in_stdout "Missing OTU File"

run test_bad_otu_file python src/run_pipeline.py --location Netherlands --otu_file input_data/otu.csv --metadata_file input_data/bad_file.csv
assert_exit_code 0
assert_in_stdout "Missing Metadata File"

