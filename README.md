# get-ssl-data

Use free publically accessible sources to gather SSL information 💪 

`crtsh_query.py` - Python script that per domain extracts the most recent SSL certificate data - issuer_name, serial_number, not_before (expiry date) and not_after (begin date) - from crt.sh and outputs results to a csv file. Simply create a `domains.txt` file, populate it with the domains you want to query, and then run the script!

`ssl-labs-query.py` - This Python script is designed to check the SSL certificate expiry date for a list of domains by using the SSL Labs API. It processes an input file containing domain names, queries the API for each domain, and writes the expiry date to an output CSV file. 
