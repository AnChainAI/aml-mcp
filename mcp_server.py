#!/usr/bin/env python3
"""
AnChain.AI MCP Server for AML Compliance and Crypto Screening

Copyright (c) 2025 AnChain.AI
Authors: Shao Liang, Victor Fang. 
Contact: Info AT anchain.ai
All rights reserved.

This software provides MCP (Model Context Protocol) tools for AML (Anti Money Laundering):
- Cryptocurrency address screening and risk assessment
- Global sanctions list screening for individuals and entities  
- IP address geolocation and sanctions compliance checking
- More data sources coming. 

For more information, visit: https://anchain.ai
"""

import os
import sys
import requests
import argparse
from typing import Literal
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.exceptions import FastMCPError, ValidationError, NotFoundError

# Create an MCP server
mcp = FastMCP("anchain_aml")
url = "https://aml.anchainai.com/api"
anchain_apikey = None
remote = False

# Add an addition tool
@mcp.tool()
def crypto_screening(address: str, protocol: str) -> dict:
    """Basic risk assessment for cryptocurrency addresses.

    Args:
        address: crypto address (e.g. 0xf4548503dd51de15e8d0e6fb559f6062d38667e7, bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh)
        protocol: 3-letter blockchain code of the crypto address (e.g. btc, eth, sol)
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
    apikey = check_apikey()
    res = requests.get(url=url+'/crypto_screening', params={'protocol': protocol, 'address': address, 'action': 'score'}, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()


# Add an addition tool
@mcp.tool()
def crypto_activity_screening(address: str, protocol: str) -> dict:
    """Suspicious activity analysis for cryptocurrency addresses.

    Args:
        address: crypto address (e.g. 0xf4548503dd51de15e8d0e6fb559f6062d38667e7, bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh)
        proto: 3-letter blockchain code of the crypto address (e.g. btc, eth, sol)
    """
    apikey = check_apikey()
    res = requests.get(url=url+'/crypto_screening', params={'protocol': protocol, 'address': address, 'action': 'activity'}, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()


# Add an addition tool
@mcp.tool()
def crypto_attribution_screening(address: str, protocol: str) -> dict:
    """Transaction flow attribution for cryptocurrency addresses. (pro plans apikey only)

    Args:
        address: crypto address (e.g. 0xf4548503dd51de15e8d0e6fb559f6062d38667e7, bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh)
        proto: 3-letter blockchain code of the crypto address (e.g. btc, eth, sol)
    """
    apikey = check_apikey()
    res = requests.get(url=url+'/crypto_screening', params={'protocol': protocol, 'address': address, 'action': 'attribution'}, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()


# Add an addition tool
@mcp.tool()
def sanctions_screening(schema: str='person', scope: str='basic', name: list[str]=None, idNumber: list[str]=None, nationality: list[str]=None, birthYear: list[str]=None) -> dict:
    """Check individuals or entities against global sanctions lists.

    Args:
        schema:  Type of entity (person, company, vessel, aircraft, crypto)
        scope: Search scope (basic/full). Default: basic. Full scope requires enterprise plan.
        name: Full name(s) to screen (e.g. ["John Doe"])
        idNumber: Government ID or passport number(s) (e.g. ["A12345678"])
        nationality: 2-letter country code(s) (ISO 3166-1, e.g. ["us", "au"])
        birthYear: Birth year(s) in string (1000-9999, e.g. ["1980", "1975"])

    Note:
        - All query parameters are optional but at least one must be provided
        - Multiple conditions (shema, name, etc.) are combined with AND logic
        - Array elements within each condition are combined with OR logic
    """

    apikey = check_apikey()
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
    apikey = check_apikey()
    res = requests.get(url=url+'/ip_screening', params={'ip_address': ip_address}, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()


# Add an addition tool
@mcp.tool()
def auto_trace(protocol: str, time_from: int, time_to: int, address: str=None, txn_hash: str=None, 
    direction: str='in',time_window: int=365, min_amount: int=0, max_amount: int=None, token: str=None) -> dict:
    """Trace the asset flow originated from or ended at a blockchain address or from a transaction. 

    Args:
        protocol: Blockchain protocol. Supported: btc (Bitcoin), eth (Ethereum), xrp (Ripple), egld (MultiversX), trx (Tron).
        address: target address to trace from or to. (required if txn_hash is not provided).
        txn_hash: target transaction hash to trace from or to. (required if address is not provided).
        direction: direction of tracing. 'in' for incoming, 'out' for outgoing (default: 'in').
        time_from: starting unix epoch timestamp for tracing.
        time_to: ending unix epoch timestamp for tracing.
        time_window: number of past days to include around transaction time  (default: 365).
        min_amount: minimun transaction amount to be included.(default: 0).
        max_amaount: maximum amount to be included.
        token: token currency (address) to trace for EVM blockchains.

    Return:
        - token_mapping: use this mapping to map address in path_info for tokens (if any)
        - labels_mapping: use this mapping to map address in path_info for known entities (if any)
        - path_info: a list of result transactions by request conditions. each of the item is a node of a transaction diagram, they has following format:
            depth: the steps (transaction) away from target.
            hash: tramsaction hash.
            receiver: receiver.
            sender: sender.
            state: the condition of this node (whether it can be extended by starting another trace request from this node)
            timestamp: the time of this transaction.
            vol: the amount of this transaction 
    """

    payload = {
        'proto': protocol,
        'direct': direction,
        'time_from': time_from,
        'time_to': time_to,
        'time_window': time_window,
        'min_amount': min_amount,
    }
    if address:
        payload.update({'address': address})
    else:
        payload.update({'txnhash': txn_hash})
    
    if max_amount:
        payload.update({'max_amount': max_amount})
    if token:
        payload.update({'token': token})

    apikey = check_apikey()
    res = requests.post(url=url+'/crypto_auto_trace', json=payload, headers={
        "Authorization": f"Bearer {apikey}"
    })
    return res.json()


# Add an addition tool
@mcp.tool()
def get_source_code(address: str, protocol: Literal['eth', 'bnb']) -> dict:
    """Get smart contract source code (if any) by address.

    Args:
        address: smart contract address
        protocol: blockchain protocol of the smart contract address (only support 'eth' and 'bnb')
    """
    apikey = check_apikey()
    res = requests.get(url=url+'/smart_contract_agent', 
        params={'action': 'contract', 'protocol': protocol, 'contract_address': address}, 
        headers={"Authorization": f"Bearer {apikey}"}
    )
    return res.json()


# Add an addition tool
@mcp.tool()
def get_transaction(transaction_hash: str, protocol: Literal['eth', 'bnb'], scope: str='summary') -> dict:
    """Get transaction data by transaction hash. options: summarized analysis or detailed execution flow. use in caution: requesting full scope data can cost high token usage or hit the max token limit.

    Args:
        transaction_hash: transaction hash.
        protocol: blockchain protocol of the smart contract address (only support 'eth' and 'bnb').
        scope: optional, default to 'summary' returns summarized analysis. for 'full' scope, execution flow is return instead.
    Return:
        - overview: transaction overview.
        - token_index: token mapping that include all the tokens involved in this transaction.
        - addr_mapping: address mapping that include some of the addresses invloved in this transaction.
        - balance_table: the asset (token and ETH) transacted during this transaction. 
            each entry contains 3 fields
            {
                "currency": "",
                "id": ,
                "value": 
            }.
            currency is the transacted token which can be mapped in data["token_index"].
            id is NFT token id, for fungible token the id field will be 0.
            value is the amount of token transacted, for NFT the value will show -1 but always means 1.
        - transaction_graph: step by step function calls and events emitted. (there is no detail of function call such as parameters and returns. refer to "data" section for full exection flow") 
          transaction_graph.vertices include all the nodes (addresses) in this transaction.
          transaction_graph.edges include all the executions of this transaction, where "step" represent the exectuion order (multiple edge can happen in 1 step).
        - transaction_summary: summary of the highlited events in this transaction.
        - data: only available with "full" scope, full execution flow of this transaction, each node (referred as 'call') contains:
            {
                "error": error message (if not succeeded),
                "from": address who initiate this call,
                "gas": gass allocated by this call,
                "idx_root": the call index that this call return to when finished,
                "index": this call index,
                "input": raw input data, refer to "func_decode" for a decoded version (if any),
                "output": raw output data, refer to "func_decode" for a decoded version (if any),
                "succeeded": status of this call,
                "to": destination address of this call,
                "trace_depth": irrelevant,
                "type": type of this call,
                "value": eth value attached with this call, amount in WEI,
                "gas_used": gas used by this call,
                "func_decode": input and output decoded into function call and return as following:
                {
                    "name": function name,
                    "parameters": (aka input) [
                        {
                            "type": arg type,
                            "name": arg name,
                            "value": arg value
                        }
                    ],
                    "returnParams": (aka output) [
                        <same format as input params>
                    ],
                    "func_sig": function signature in bytes
                },
                "calls": [<internal call objects during execution of this call>]
            }
    """
    apikey = check_apikey()
    res = requests.get(url=url+'/smart_contract_agent', 
        params={'action': 'transaction', 'protocol': protocol, 'transaction_hash': transaction_hash}, 
        headers={"Authorization": f"Bearer {apikey}"}
    )
    # this is to cut down return size
    result = res.json()
    try:
        result = result['data']['transaction']
        if scope == 'summary':
            result.pop('data')
        elif scope == 'full':
            result = result.pop('data')
    except:
        pass
    return result


def check_apikey():
    if remote:
        apikey = get_http_headers().get("x-api-key", "")
    else:
        apikey = anchain_apikey
    
    if not apikey:
            raise ValidationError("no anchain apikey provided")
    return apikey

def main():
    parser = argparse.ArgumentParser()

    # Mode selection
    parser.add_argument('--rm', '--remote', action='store_true', 
                       help='Run in remote mode')

    # http server arguments
    remote_group = parser.add_argument_group('http server options')
    remote_group.add_argument('--port', type=int, default=8002,
                             help='Port for remote mcp server (default: 8002)')
    remote_group.add_argument('--host', default='127.0.0.1',
                             help='Host for remote mcp server (default: 127.0.0.1)')

    # stdio server arguments  
    local_group = parser.add_argument_group('stdio server options')
    local_group.add_argument('-k', '--ANCHAIN_APIKEY', dest='apikey',
                            help='API key for stdio server')

    args = parser.parse_args()

    if args.rm:
        global remote
        remote = True
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        global anchain_apikey
        if args.apikey:
            anchain_apikey = args.apikey
        else:
            anchain_apikey = os.environ.get("ANCHAIN_APIKEY")
    
        if not anchain_apikey:
            print('ANCHAIN_APIKEY environment variable is required', file=sys.stderr, flush=True)
            raise ValueError('ANCHAIN_APIKEY environment variable is required')
    
        mcp.run()

if __name__ == '__main__':
    main()


