import argparse
import subprocess
import re
import ipaddress

def is_valid_target(target):

    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass

    hostname_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    if re.match(hostname_pattern, target) and len(target) <= 253:
        return True
    
    return False

def ping_device(target):
    if not is_valid_target(target):
        print(f"Error: Invalid target '{target}'. Please provide a valid IP address or hostname.")
        return
    
    command = ["ping", "-c", "4", target]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(output.decode())
    except subprocess.CalledProcessError as e:
        print(f"Failed to ping {target}\n{e.output.decode()}")

def main():
    parser = argparse.ArgumentParser(description="Ping a device securely.")
    parser.add_argument("target", type=str, help="IP address or DNS name of the target device")
    args = parser.parse_args()
    ping_device(args.target)

if __name__ == "__main__":
    main()
