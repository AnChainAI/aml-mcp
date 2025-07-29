# server.py
from fastmcp import FastMCP
import requests
import argparse
import os
import sys

# Create an MCP server
mcp = FastMCP("anchain_aml")
url = "https://aml.anchainai.com/api"
apikey = None

# Add an addition tool
@mcp.tool()
def crypto_screening(address: str, proto: str) -> dict:
    """Screen cryptocurrency addresses for risk factors and sanctions compliance.

    Args:
        address: crypto address (e.g. 0xf4548503dd51de15e8d0e6fb559f6062d38667e7, bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh)
        proto: 3-letter blockchain code of the crypto address (e.g. btc, eth, sol)

    Note:
        Supported Protocols
        The address risk score endpoint currently supports the following protocols:

        Protocol    Name
        btc     Bitcoin
        eth     Ethereum
        sol     Solana
        xlm     Stellar
        trx     Tron
        egld    Elrond
        xrp     Ripple
        bch     Bitcoin Cash
        ltc     Litecoin
        algo    Algorand
        bsv     Bitcoin SV
        dash    Dash
        xvg     Verge Currency
        zec     Zcash

    """
    res = requests.get(url=url+'/crypto_screening', params={'protocol': proto, 'address': address}, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()


# Add an addition tool
@mcp.tool()
def sanctions_screening(schema: str='person', scope: str='basic', name: list[str]=None, idNumber: list[str]=None, nationality: list[str]=None, birthYear: list[int]=None) -> dict:
    """Check individuals or entities against global sanctions lists.

    Args:
        schema:  Type of entity (person, company, vessel, aircraft, crypto)
        scope: Search scope (basic/full). Default: basic. Full scope requires enterprise plan.
        name: Full name(s) to screen (e.g. ["John Doe"])
        idNumber: Government ID or passport number(s) (e.g. ["A12345678"])
        nationality: 2-letter country code(s) (ISO 3166-1, e.g. ["us", "au"])
        birthYear: Birth year(s) (1000-9999, e.g. [1980, 1975])

    Note:
        - All query parameters are optional but at least one must be provided
        - Multiple conditions (shema, name, etc.) are combined with AND logic
        - Array elements within each condition are combined with OR logic
    """

    payload = {
        "schema": schema,
        "scope": scope,
        "properties": {}
    }
    if name:
        payload['properties'].update({'name': name})
    if idNumber:
        payload['properties'].update({'idNumber': idNumber})
    if nationality:
        payload['properties'].update({'nationality': nationality})
    if birthYear:
        payload['properties'].update({'birthYear': birthYear})

    data = requests.post(url=url+"/sanctions_screening", json=payload, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return data.json()


# Add an addition tool
@mcp.tool()
def ip_screening(ip_address: str) -> dict:
    """Check if an IP address originates from a sanctioned country.

    Args:
        ip_address: The IP address to check (IPv4 or IPv6)
    """
    res = requests.get(url=url+'/ip_screening', params={'ip_address': ip_address}, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()



def main():
    global apikey

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--ANCHAIN_APIKEY', help="Specify apikey", type=str)
    args = parser.parse_args()

    if args.ANCHAIN_APIKEY:
        apikey = args.ANCHAIN_APIKEY
    else:
        apikey = os.environ.get("ANCHAIN_APIKEY")

    
    if not apikey:
        print('ANCHAIN_APIKEY environment variable is required', file=sys.stderr, flush=True)
        raise ValueError('ANCHAIN_APIKEY environment variable is required')
    
    mcp.run()

if __name__ == '__main__':
    main()


