import asyncio
import time
import random
from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from mnemonic import Mnemonic
from eth_account import Account
import aiohttp

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

# Function to write to win.txt
def write_to_win(wallet_info):
    with open("win.txt", "a") as f:
        f.write(wallet_info + "\n")

# Main function
async def main():
    total_checked = 0
    total_wins = 0
    total_balance = 0.0  # To store the total balance found
    first_run = True  # Flag to indicate if it's the first run
    term = Console()

    words = load_words("words.txt")
    if len(words) < 24:
        raise ValueError("Insufficient words in words.txt. Expected at least 24 words.")

    async with aiohttp.ClientSession() as session:
        Account.enable_unaudited_hdwallet_features()  # Enable Mnemonic features
        while True:
            try:
                # Generate new 24-word mnemonic passphrase
                random.shuffle(words)
                words_split = ' '.join(words[:24])  # Take the first 24 shuffled words

                # Derive Ethereum address from mnemonic
                acct = Account.from_mnemonic(words_split)
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
                    total_balance_color = "blue"
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
                    f"Mnemonic: {words_split}\n"
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
                    # Write wallet info to win.txt
                    wallet_info = f"Address: {addr}, Mnemonic: {words_split}, Balance: {bal:.16f} ETH, Transactions: {txs}, Response Time: {response_time:.4f} seconds"
                    write_to_win(wallet_info)

                await asyncio.sleep(0.5)  # Adjust sleep time as needed for faster scanning

            except KeyboardInterrupt:
                print("\n\nScan interrupted. Exiting...")
                break
            except ValueError as ve:
                print(f"ValueError: {ve}")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    start_time = time.time()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nScan interrupted. Exiting...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print(f"Execution time: {time.time() - start_time} seconds")
