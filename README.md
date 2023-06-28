# Solidity-function-level-tokenizer-for-SourcererCC
A test version of the tokenizing parser of identifying function-level Solidity smart contracts using SourcereCC

This is a test version of the SourcererCC tokenizer to parse Solidity function-level code fragments into token results.
The process is to use Universal Ctags to generate JSON result and parse it to ctags_json_parser.py to generate sample.csv.
ctags --fields=+ne --sort=no --output-format=json --options=../ctags_conf.ini -R > tags.json

Then you need to create a directory for Solidity contracts in zip format and store each of them in single zip files.
Use collect_list.py to generate a list of the files.
Put sample.csv and projects-lists.txt under SourcererCC block-level tokenizer directory(./SourcererCC/tokenizers/block-level)
Use sol_tokenizer to generate tokens for the Solidity contract dataset.

extract_scc_info.py is to generate a piece of general clone information for analysis.
