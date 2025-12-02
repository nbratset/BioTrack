test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_args python src/app.py -n 'John Doe'
assert_no_error

run test_bad_otu_file python src/app.py -n 'John Doe' --taxa_file input_data/bad_file.csv
assert_exit_code 0
assert_in_stdout "Missing Taxa/OTU File"

run test_bad_otu_file python src/run_pipeline.py -n 'John Doe' --alpha_file input_data/bad_file.csv
assert_exit_code 0
assert_in_stdout "Missing alpha diversity File"

run test_bad_otu_file python src/run_pipeline.py -n 'John Doe' --beta_file input_data/bad_file.csv
assert_exit_code 0
assert_in_stdout "Missing beta diversity File"

run test_bad_otu_file python src/run_pipeline.py -n 'John Doe' --diff_file input_data/bad_file.csv
assert_exit_code 0
assert_in_stdout "Missing Differential Abundance File"