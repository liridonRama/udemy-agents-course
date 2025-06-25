import gradio as gr
from accounts import Account, get_share_price

# Global account variable
account = None

def create_account(username, initial_deposit):
    """Create a new account for the user"""
    global account
    try:
        initial_deposit = float(initial_deposit)
        account = Account(username, initial_deposit)
        return f"Account created for {username} with initial deposit of ${initial_deposit:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def deposit_funds(amount):
    """Deposit funds into the account"""
    global account
    if account is None:
        return "Please create an account first"
    
    try:
        amount = float(amount)
        account.deposit(amount)
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    """Withdraw funds from the account"""
    global account
    if account is None:
        return "Please create an account first"
    
    try:
        amount = float(amount)
        if account.withdraw(amount):
            return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Error: Insufficient funds. Current balance: ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    """Buy shares of a specified stock"""
    global account
    if account is None:
        return "Please create an account first"
    
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        price = get_share_price(symbol)
        
        if account.buy_shares(symbol, quantity):
            return f"Successfully bought {quantity} shares of {symbol} at ${price:.2f} each. " \
                   f"Total cost: ${price * quantity:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Error: Insufficient funds to buy {quantity} shares of {symbol} at ${price:.2f} each. " \
                   f"Total cost would be ${price * quantity:.2f}, but your balance is ${account.balance:.2f}"
    except ValueError as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    """Sell shares of a specified stock"""
    global account
    if account is None:
        return "Please create an account first"
    
    try:
        quantity = int(quantity)
        symbol = symbol.upper()
        price = get_share_price(symbol)
        
        if account.sell_shares(symbol, quantity):
            return f"Successfully sold {quantity} shares of {symbol} at ${price:.2f} each. " \
                   f"Total received: ${price * quantity:.2f}. New balance: ${account.balance:.2f}"
        else:
            holdings = account.get_holdings()
            current_quantity = holdings.get(symbol, 0)
            return f"Error: Insufficient shares to sell. You have {current_quantity} shares of {symbol}, " \
                   f"but tried to sell {quantity}"
    except ValueError as e:
        return f"Error: {str(e)}"

def get_account_status():
    """Get the current status of the account"""
    global account
    if account is None:
        return "Please create an account first"
    
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.calculate_profit_loss()
    
    status = f"Account: {account.username}\n"
    status += f"Cash Balance: ${account.balance:.2f}\n"
    status += f"Portfolio Value: ${portfolio_value:.2f}\n"
    status += f"Total Assets: ${(account.balance + portfolio_value):.2f}\n"
    status += f"Initial Deposit: ${account.initial_deposit:.2f}\n"
    status += f"Profit/Loss: ${profit_loss:.2f} "
    
    if profit_loss > 0:
        status += "(Profit)"
    elif profit_loss < 0:
        status += "(Loss)"
    else:
        status += "(Break-even)"
        
    return status

def get_holdings():
    """Get the current holdings of the account"""
    global account
    if account is None:
        return "Please create an account first"
    
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings found"
    
    result = "Current Holdings:\n\n"
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        result += f"{symbol}: {quantity} shares at ${price:.2f} each = ${value:.2f}\n"
    
    return result

def get_transactions():
    """Get the transaction history of the account"""
    global account
    if account is None:
        return "Please create an account first"
    
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions found"
    
    result = "Transaction History:\n\n"
    for i, tx in enumerate(transactions, 1):
        result += f"Transaction #{i}: "
        
        if tx['type'] == 'deposit':
            result += f"Deposited ${tx['amount']:.2f}"
        elif tx['type'] == 'withdrawal':
            result += f"Withdrew ${tx['amount']:.2f}"
        elif tx['type'] == 'buy':
            result += f"Bought {tx['quantity']} shares of {tx['symbol']} at ${tx['price']:.2f} each (Total: ${tx['total']:.2f})"
        elif tx['type'] == 'sell':
            result += f"Sold {tx['quantity']} shares of {tx['symbol']} at ${tx['price']:.2f} each (Total: ${tx['total']:.2f})"
        
        result += f" - {tx['timestamp']}\n"
    
    return result

def get_stock_price(symbol):
    """Get the current price of a stock"""
    try:
        symbol = symbol.upper()
        price = get_share_price(symbol)
        return f"Current price of {symbol}: ${price:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(title="Trading Account Simulator") as demo:
    gr.Markdown("# Trading Account Simulator")
    gr.Markdown("Create an account, deposit funds, and start trading!")
    
    with gr.Tab("Account Management"):
        with gr.Box():
            gr.Markdown("### Create Account")
            with gr.Row():
                username_input = gr.Textbox(label="Username")
                initial_deposit_input = gr.Textbox(label="Initial Deposit ($)")
            create_btn = gr.Button("Create Account")
            create_output = gr.Textbox(label="Result")
            create_btn.click(create_account, inputs=[username_input, initial_deposit_input], outputs=create_output)
        
        with gr.Box():
            gr.Markdown("### Deposit Funds")
            deposit_input = gr.Textbox(label="Amount ($)")
            deposit_btn = gr.Button("Deposit")
            deposit_output = gr.Textbox(label="Result")
            deposit_btn.click(deposit_funds, inputs=deposit_input, outputs=deposit_output)
        
        with gr.Box():
            gr.Markdown("### Withdraw Funds")
            withdraw_input = gr.Textbox(label="Amount ($)")
            withdraw_btn = gr.Button("Withdraw")
            withdraw_output = gr.Textbox(label="Result")
            withdraw_btn.click(withdraw_funds, inputs=withdraw_input, outputs=withdraw_output)
    
    with gr.Tab("Trading"):
        with gr.Box():
            gr.Markdown("### Stock Price Lookup")
            price_symbol_input = gr.Textbox(label="Stock Symbol (e.g., AAPL, TSLA, GOOGL)")
            price_btn = gr.Button("Get Price")
            price_output = gr.Textbox(label="Current Price")
            price_btn.click(get_stock_price, inputs=price_symbol_input, outputs=price_output)
        
        with gr.Box():
            gr.Markdown("### Buy Shares")
            with gr.Row():
                buy_symbol_input = gr.Textbox(label="Stock Symbol")
                buy_quantity_input = gr.Textbox(label="Quantity")
            buy_btn = gr.Button("Buy Shares")
            buy_output = gr.Textbox(label="Result")
            buy_btn.click(buy_shares, inputs=[buy_symbol_input, buy_quantity_input], outputs=buy_output)
        
        with gr.Box():
            gr.Markdown("### Sell Shares")
            with gr.Row():
                sell_symbol_input = gr.Textbox(label="Stock Symbol")
                sell_quantity_input = gr.Textbox(label="Quantity")
            sell_btn = gr.Button("Sell Shares")
            sell_output = gr.Textbox(label="Result")
            sell_btn.click(sell_shares, inputs=[sell_symbol_input, sell_quantity_input], outputs=sell_output)
    
    with gr.Tab("Account Status"):
        with gr.Box():
            gr.Markdown("### Account Overview")
            status_btn = gr.Button("Refresh Account Status")
            status_output = gr.Textbox(label="Account Status", lines=8)
            status_btn.click(get_account_status, inputs=None, outputs=status_output)
        
        with gr.Box():
            gr.Markdown("### Current Holdings")
            holdings_btn = gr.Button("View Holdings")
            holdings_output = gr.Textbox(label="Holdings", lines=10)
            holdings_btn.click(get_holdings, inputs=None, outputs=holdings_output)
        
        with gr.Box():
            gr.Markdown("### Transaction History")
            transactions_btn = gr.Button("View Transactions")
            transactions_output = gr.Textbox(label="Transactions", lines=15)
            transactions_btn.click(get_transactions, inputs=None, outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()