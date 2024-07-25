import requests
import json
import csv

def query_crtsh(domain):
    url = f'https://crt.sh/?q={domain}&output=json'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for {domain}: {response.status_code}")
        return None

def main():
    try:
        with open('domains.txt', 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("The file domains.txt was not found.")
        return

    results = []
    for domain in domains:
        print(f"Querying crt.sh for {domain}...")
        data = query_crtsh(domain)
        if data:
            if len(data) > 0:
                # Extract required fields from the first element of the JSON response
                first_entry = data[0]
                result = {
                    "domain": domain,
                    "issuer_name": first_entry.get("issuer_name"),
                    "serial_number": first_entry.get("serial_number"),
                    "not_before": first_entry.get("not_before"),
                    "not_after": first_entry.get("not_after")
                }
            else:
                result = {
                    "domain": domain,
                    "issuer_name": "error",
                    "serial_number": "error",
                    "not_before": "error",
                    "not_after": "error"
                }
        else:
            result = {
                "domain": domain,
                "issuer_name": "error",
                "serial_number": "error",
                "not_before": "error",
                "not_after": "error"
            }
        results.append(result)

    # Define CSV file column headers
    fieldnames = ["domain", "issuer_name", "serial_number", "not_before", "not_after"]

    # Write results to a CSV file
    with open('crtsh_results.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Results have been written to crtsh_results.csv")

if __name__ == "__main__":
    main()
