import asyncio
import time
from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from mnemonic import Mnemonic
from eth_account import Account
import aiohttp
import eth_utils

# Initialize necessary objects
console = Console()

# Load BIP39 word list from a file
def load_words(filename):
    with open(filename, "r") as f:
        words = f.read().splitlines()
    return words

# Function to check balance using an Ethereum API asynchronously
async def balance(addr, session):
    url = f"https://ethereum.atomicwallet.io/api/v2/address/{addr}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            balance_eth = float(data["balance"])
            return balance_eth, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            return 0.0, None

# Function to check transaction count using the Ethereum API asynchronously
async def transaction(addr, session):
    url = f"https://ethereum.atomicwallet.io/api/v2/address/{addr}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            txs = int(data["txs"])
            return txs, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            return 0, None

# Function to save winning wallet information to win.txt
def save_to_win_file(wallet_info):
    with open("12same.txt", "a") as f:
        f.write(wallet_info + "\n")

# Main function
async def main():
    total_checked = 0
    total_wins = 0
    total_balance = 0.0  # To store the total balance found
    first_run = True  # Flag to indicate if it's the first run
    term = Console()

    words = load_words("words.txt")
    if len(words) < 2048:
        raise ValueError("Insufficient words in words1m.txt. Expected at least 2048 words.")

    used_words = set()  # Set to track used words

    async with aiohttp.ClientSession() as session:
        Account.enable_unaudited_hdwallet_features()  # Enable Mnemonic features

        for word in words:
            if word in used_words:
                continue  # Skip if word has been used before

            try:
                # Generate mnemonic with 15 repetitions of the current word
                mnemonic_words = ' '.join([word] * 12)


                used_words.add(word)  # Add the word to used set

                # Derive Ethereum address from mnemonic
                acct = Account.from_mnemonic(mnemonic_words)
                addr = acct.address

                # Perform balance and transaction checks asynchronously
                start_time = time.time()
                bal_task = balance(addr, session)
                txs_task = transaction(addr, session)

                # Await results
                bal, bal_time = await bal_task
                txs, txs_time = await txs_task
                response_time = time.time() - start_time  # Calculate response time

                # Add balance to total_balance only if API call is successful
                if bal_time is not None:
                    total_balance += bal

                # Determine color for Total Balance based on whether any balance is added
                if total_balance > 0:
                    total_balance_color = "red"
                else:
                    total_balance_color = "white"

                # Determine color for Total Wins based on whether balance is greater than 0
                total_wins_color = "red" if bal > 0 else "gray88"

                # Prepare panel content with alignment
                panel_content = (
                    f"[b magenta]  [/]\n"
                    f"[ad00ff]Total Checked: [fff]{'{: <4}'.format(total_checked)}[/] "
                    f"[ad00ff]Total Wins: [{total_wins_color}]{total_wins:^4}[/] "
                    f"[ad00ff]Total Balance: [{total_balance_color}]{total_balance:>20.16f} ETH[/]\n"
                    f"[b magenta]  [/]\n"
                    f"[ad00ff]Address: [fff]{addr}\n"
                    f"Mnemonic: {mnemonic_words}\n"
                    f"Balance: [green]{bal:.16f} ETH (Updated: {bal_time})[/]\n"
                    f"Transactions: [blue]{txs} (Updated: {txs_time})[/]\n"
                    f"[b magenta]  [/]\n"
                    f"[pink]Response Time: [fff]{response_time:.4f} seconds[/]\n"
                )

                if not first_run:
                    console.print("\x1b\x1b")  # Clear screen before printing new content

                console.print(Panel(panel_content, title="www.coinscan.cc", border_style="#ad00ff"))
                first_run = False

                total_checked += 1
                if bal > 0:
                    total_wins += 1
                    # Save winning wallet info to win.txt
                    wallet_info = f"Address: {addr}, Mnemonic: {mnemonic_words}, Balance: {bal:.16f} ETH, Transactions: {txs}"
                    save_to_win_file(wallet_info)

                await asyncio.sleep(2)  # Adjust sleep time as needed for rate limiting

            except eth_utils.exceptions.ValidationError as e:
                print(f"Error with mnemonic '{mnemonic_words}': {e}")
                continue  # Continue to the next word if mnemonic is invalid

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nScan interrupted. Exiting...")
