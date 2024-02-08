import csv

def load_hosts_csv(file_hosts_csv):
    """
    Load hosts.csv data from a file.

    Args:
        file_hosts_csv (str): The path to the hosts.csv file.

    Returns:
        dict: The loaded hosts.csv data.

    """
    dict_hosts = {}
    with open(file_hosts_csv, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=";", quotechar="|")
        for row in spamreader:
            host_name, list_ip, list_os_info = eval(", ".join(row))
            dict_hosts[host_name] = {"ip": list_ip, "os": list_os_info} 
    return dict_hosts 