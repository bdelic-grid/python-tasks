import argparse
import platform
import subprocess
import os
import psutil

def get_distro_info():
    try:
        res = subprocess.run(["sw_vers", "-productName"], capture_output=True, check=True)
        product_name = res.stdout.strip().decode("utf-8")

        res = subprocess.run(["sw_vers", "-productVersion"], capture_output=True, check=True)
        product_version = res.stdout.strip().decode("utf-8")
        
        res = subprocess.run(["sw_vers", "-buildVersion"], capture_output=True, check=True)
        build_version = res.stdout.strip().decode("utf-8")

        return f"Product name: {product_name}, product version: {product_version}, build version: {build_version}"
    except subprocess.CalledProcessError as e:
        print("Error retrieving distro info")
        print(e.returncode, e.output)
        raise e
    
def get_mem_info():
    memory_info = psutil.virtual_memory()

    return f"Total memory: {memory_info.total / 1024 / 1024} MB, available memory: {memory_info.available / 1024 / 1024}MB, used memory: {memory_info.used / 1024 / 1024} MB"
    
def get_cpu_info():
    cpu_info = platform.processor()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_freq = psutil.cpu_freq()[0]

    return f"Processor: {cpu_info}, CPU count: {cpu_count}, CPU frequency: {cpu_freq} Mhz"

def get_user_info():
    try:
        res = subprocess.run(["whoami"], capture_output=True, check=True)
        
    except subprocess.CalledProcessError as e:
        print("Error retrieving user info")
        print(e.returncode, e.output)
        raise e
    
    user = res.stdout.strip().decode("utf-8")

    return f"Current user: {user}"

def get_load_info():
    try:
        res = os.getloadavg()
    except OSError as e:
        raise OSError("Error retrieving load average info") from e

    return f"Load average for 1, 5 and 15 minutes: {res}"

def get_ip_info():
    try:
        res = subprocess.run(["ipconfig",  "getifaddr",  "en0"], capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error retrieving ip info")
        print(e.returncode, e.output)
        raise e
    
    ip_addr = res.stdout.strip().decode("utf-8")

    return f"IP address: {ip_addr}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get macOS system information.")
    parser.add_argument('-d', '--distro', action='store_true', help="Get macOS distribution information")
    parser.add_argument('-m', '--memory', action='store_true', help="Get memory usage (total, used, free)")
    parser.add_argument('-c', '--cpu', action='store_true', help="Get CPU information")
    parser.add_argument('-u', '--user', action='store_true', help="Get current user information")
    parser.add_argument('-l', '--load', action='store_true', help="Get system load average")
    parser.add_argument('-i', '--ip', action='store_true', help="Get IP address")

    args = parser.parse_args()

    try:
        if args.distro:
            print(get_distro_info())
        elif args.memory:
            print(get_mem_info())
        elif args.cpu:
            print(get_cpu_info())
        elif args.user:
            print(get_user_info())
        elif args.load:
            print(get_load_info())
        elif args.ip:
            print(get_ip_info())
        else:
            print("Invalid option!")
    except Exception as e:
        print(f"Error: {e}")
