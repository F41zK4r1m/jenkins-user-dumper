#!/usr/bin/env python3
import argparse
import requests
import re
import json
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_color(message, color=Fore.WHITE):
    """Print colored messages to console"""
    print(f"{color}{message}{Style.RESET_ALL}")

def parse_arguments():
    """Handle command-line arguments"""
    parser = argparse.ArgumentParser(description='Jenkins User Extractor', add_help=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--ip', help='Target IP address')
    group.add_argument('-d', '--domain', help='Target domain name')
    parser.add_argument('-p', '--port', help='Target port number (required with IP)')
    parser.add_argument('-o', '--output', help='Output file name')
    parser.add_argument('-t', '--timeout', type=int, default=10, 
                      help='Request timeout in seconds (default: 10)')
    parser.add_argument('--debug', action='store_true', help='Show raw JSON response')
    parser.add_argument('-h', '--help', action='store_true', help='Show help menu')

    args = parser.parse_args()

    if args.help:
        show_help()
    if args.ip and not args.port:
        print_color("Error: Port required when using IP address", Fore.RED)
        show_help()
    if args.timeout <= 0:
        print_color("Error: Timeout must be greater than 0", Fore.RED)
        sys.exit(1)
    
    return args

def show_help():
    """Display help menu"""
    print(f"\n{Fore.CYAN}Usage:{Style.RESET_ALL}")
    print("python jenkins_users.py [-i IP -p PORT] | [-d DOMAIN] [-o OUTPUT]")
    print(f"\n{Fore.CYAN}Options:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}-i, --ip{Style.RESET_ALL}      Target IP address")
    print(f"{Fore.GREEN}-p, --port{Style.RESET_ALL}    Target port number")
    print(f"{Fore.GREEN}-d, --domain{Style.RESET_ALL}  Target domain name")
    print(f"{Fore.GREEN}-o, --output{Style.RESET_ALL}  Output file name")
    print(f"{Fore.GREEN}-t, --timeout{Style.RESET_ALL} Request timeout in seconds (default: 10)")
    print(f"{Fore.GREEN}--debug{Style.RESET_ALL}       Show raw JSON response")
    print(f"{Fore.GREEN}-h, --help{Style.RESET_ALL}    Show this help message")
    sys.exit(0)

def construct_target_url(args):
    """Build the target URL from provided arguments"""
    endpoint = "/asynchPeople/api/json"
    
    if args.ip and args.port:
        return f"http://{args.ip}:{args.port}{endpoint}"
    elif args.domain:
        if args.domain.startswith(('http://', 'https://')):
            return f"{args.domain.rstrip('/')}{endpoint}"
        else:
            return f"http://{args.domain}{endpoint}"

def fetch_json_data(url, timeout):
    """Retrieve JSON data from target URL"""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print_color(f"Connection error: {e}", Fore.RED)
        sys.exit(1)
    except json.JSONDecodeError:
        print_color("Invalid JSON response received", Fore.RED)
        sys.exit(1)

def extract_usernames(json_data, debug=False):
    """Extract usernames from JSON structure"""
    if debug:
        print_color("\n[DEBUG] Raw JSON response:", Fore.CYAN)
        print(json.dumps(json_data, indent=2))
    
    username_pattern = re.compile(r"/user/([^/]+)")
    users = []

    for entry in json_data.get('users', []):
        user_data = entry.get('user', {})
        profile_url = user_data.get('absoluteUrl', '')
        
        if match := username_pattern.search(profile_url):
            users.append(match.group(1))
        else:
            print_color(f"Skipped invalid entry: {profile_url}", Fore.YELLOW)
    
    return users

def save_results(usernames, filename):
    """Save results to output file"""
    if not filename:
        filename = "target.txt"
    
    with open(filename, 'w') as f:
        f.write('\n'.join(usernames))
    
    print_color(f"\nSuccessfully saved {len(usernames)} users to {filename}", Fore.GREEN)

def main():
    args = parse_arguments()
    target_url = construct_target_url(args)
    
    print_color(f"\n[*] Targeting: {target_url}", Fore.YELLOW)
    print_color(f"[*] Timeout set to: {args.timeout}s", Fore.YELLOW)
    
    json_response = fetch_json_data(target_url, args.timeout)
    discovered_users = extract_usernames(json_response, args.debug)
    
    if not discovered_users:
        print_color("\nNo valid users found in response", Fore.YELLOW)
        sys.exit(0)
    
    output_file = args.output if args.output else 'target.txt'
    save_results(discovered_users, output_file)

if __name__ == '__main__':
    main()
