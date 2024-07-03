ETH-wallet-mine is a Python application that asynchronously scans Ethereum addresses, retrieves balance and transaction information using external APIs, and displays results in a styled console panel.
Features

    Generates Ethereum addresses from mnemonic phrases.
    Retrieves and displays real-time balance and transaction count.
    Stylish console output using the rich library.
    Tracks total checked addresses, total wins (addresses with non-zero balances), and cumulative balances found.

Installation

    Clone the repository:

    bash

git clone <repository-url>
cd ETH-wallet-mine



Install dependencies using pip:

bash

pip install -r requirements.txt

Run the application:

bash

    python coinscan.py

Usage

    Upon execution, the program starts generating Ethereum addresses and querying their balances and transaction counts asynchronously.
    Console output includes detailed information about each address checked, including mnemonic phrases, balances, transaction counts, and response times.
    Total checked addresses, total wins (addresses with non-zero balances), and cumulative balances found are displayed and updated in real-time.

Dependencies

    eth-account: For Ethereum account management.
    mnemonic: For generating mnemonic phrases.
    aiohttp: For asynchronous HTTP requests.
    rich: For stylish console output.

Contributing

Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.
