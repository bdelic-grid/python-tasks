import argparse
import re
from collections import defaultdict

def parse_log_file(filename):
    try:
        user_agents = defaultdict(int) 
        with open(filename, 'r', encoding="utf-8") as file:
            for line in file:
                match = re.search('"[^"]*"$', line)
                if match:
                    user_agent = match.group(0).strip('"')
                    if user_agent == '-':
                        user_agent = "No user agent provided"
                    user_agents[user_agent] += 1
        
        return user_agents
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: The file '{filename}' was not found") from e
    except IOError as e:
        raise IOError(f"Error while reading the file {filename}") from e

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The name of the log file to process")
    
    args = parser.parse_args()
    
    try:
        user_agents = parse_log_file(args.filename)
        
        print(f"Total unique user agents: {len(user_agents)}")

        print("User agent statistics:")
        for user_agent in sorted(user_agents.keys()):
            count = user_agents[user_agent]
            print(f"{user_agent}: {count} request(s)")
    
    except FileNotFoundError as e:
        print(e)
    except IOError as e:
        print(e)