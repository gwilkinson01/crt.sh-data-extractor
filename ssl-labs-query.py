import requests
import sys
import random
import time
import datetime
import csv

def convert_unix_timestamp_to_date(unix_timestamp):
    # Convert Unix timestamp to datetime object
    timestamp = datetime.datetime.fromtimestamp(unix_timestamp / 1000.0)
    # Format the datetime object to 'yyyy-MM-dd'
    return timestamp.strftime('%Y-%m-%d')

def get_certificate_expiry(host):
    url = "https://api.ssllabs.com/api/v3/analyze"
    params = {
        "host": host,
        "fromCache": "on",
        "all": "on"
    }

    while True:
        response = requests.get(url, params=params)
        if response.status_code == 429:
            # If rate limited, wait a random time between 10-20 seconds
            wait_time = random.randint(10, 20)
            time.sleep(wait_time)
        elif response.status_code == 529:
            # If server error, wait a random time between 15-30 minutes
            wait_time = random.randint(15 * 60, 30 * 60)
            time.sleep(wait_time)
        elif response.status_code == 200:
            data = response.json()
            if "status" in data:
                status = data["status"]
                if status == "READY":
                    if "certs" in data and len(data["certs"]) > 0:
                        cert_info = data["certs"][0]
                        if "notBefore" in cert_info:
                            not_before_unix_timestamp = cert_info["notBefore"]
                            not_before_date = convert_unix_timestamp_to_date(not_before_unix_timestamp)
                            return not_before_date  # Return the 'notBefore' date
                        else:
                            return "Error: Certificate dates not found"
                    else:
                        return "Error: No certificate information available"
                elif status == "IN_PROGRESS" or status == "DNS":
                    time.sleep(120)
                    continue
                elif status == "ERROR":
                    return "Error: status is error"
                else:
                    return "Error: unknown status"
            else:
                return "Error: status field not in response"
        else:
            return "Error: unexpected response code"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ssl_checker.py <input_file.txt> <output_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]  # Input text file containing domain names
    output_file = sys.argv[2]  # Output CSV file

    # Read domain names from the input file
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]

    # Open the CSV file to write results
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header row
        csvwriter.writerow(['Domain', 'Expiry Date'])

        # Process each domain and write to CSV
        for domain in domains:
            print(f"Checking {domain}...")
            not_before_date = get_certificate_expiry(domain)
            csvwriter.writerow([domain, not_before_date])
            time.sleep(random.randint(1, 3))  # To avoid hitting API rate limits
