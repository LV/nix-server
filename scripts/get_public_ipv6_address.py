"""
Prints the public IPv6 address of the machine
"""

import os
import requests
import sys


def send_req(service_url: str) -> str:
    """
    Sends a request to a webpage that tells you what IP you're coming from
    """
    try:
        response = requests.get(service_url, timeout=5)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text.strip()
    except requests.RequestException as e:
        return f"Error: {e}"


def get_ipv6_address() -> str:
    """
    Get the definitive public IPv6 address of the machine
    """
    # Domains of the services from where to CURL to get server's IPv6 address
    ipv6_services: list[str] = [
        "https://ifconfig.me",
        "https://ipecho.net/plain",
        "https://icanhazip.com",
    ]

    """
    ipv4_servcies: list[str] = [
        "https://ipinfo.io/ip",
        "https://api.ipify.org"
    ]
    """

    # put ipv6 address into a single set, if that set has only one element then the IP is consistent and correct
    ipv6_address: set = set()
    errors: list[
        str
    ] = (
        []
    )  # currently doing nothing with this, perhaps log this into server in the future

    for serv in ipv6_services:
        try:
            ip: str = send_req(serv)
            ipv6_address.add(send_req(serv))
        except requests.RequestException as e:
            errors.append(str(e))

    if len(ipv6_address) == 0:
        raise ValueError("Could not obtain an IP address!")

    if len(ipv6_address) > 1:
        raise ValueError("Coult not obtain a consistent IP address!")

    return ipv6_address.pop()


def main() -> None:
    ip: str = get_ipv6_address()
    sys.stdout.write(get_ipv6_address())
    sys.stdout.flush()


if __name__ == "__main__":
    main()
