test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_args python src/report.py -i 'file.csv' -p 'id_123' -r 'reference.csv'
assert_no_error
assert_in_stdout 'file.csv'
assert_in_stdout 'reference.csv'
assert_in_stdout 'id_123'
assert_in_stdout 'id_123.html'
