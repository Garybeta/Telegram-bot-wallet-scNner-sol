import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

import os

# Set up the Covalent API key and Telegram bot token
COVALENT_API_KEY = os.getenv('COVALENT_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Define the function that fetches wallet trades
def fetch_trades(wallet_address):
    url = f'https://api.covalenthq.com/v1/1/address/{wallet_address}/transactions_v2/?key={COVALENT_API_KEY}'
    
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and 'data' in data:
        transactions = data['data']['items']
        total_trades = len(transactions)
        wins = 0
        losses = 0
        pnl = 0

        # Example of calculating wins/losses
        for tx in transactions:
            # Add your own logic to determine if a trade was a win or loss
            value = tx.get('value_quote', 0)
            pnl += value

            if value > 0:
                wins += 1
            else:
                losses += 1

        return f"Total Trades: {total_trades}\nWins: {wins}\nLosses: {losses}\nPnL: {pnl}"
    else:
        return "Failed to fetch trades or no trades found."

# Command function for /trades
def trades_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide a wallet address!")
        return

    wallet_address = context.args[0]
    trades_info = fetch_trades(wallet_address)
    
    update.message.reply_text(trades_info)

# Main function to set up the bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Command handler for /trades
    dispatcher.add_handler(CommandHandler("trades", trades_command))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()