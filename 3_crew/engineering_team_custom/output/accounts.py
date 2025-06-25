def get_share_price(symbol):
    """
    Returns the current price of a share for the given symbol.
    This is a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.
    """
    prices = {'AAPL': 150.0, 'TSLA': 600.0, 'GOOGL': 2800.0}
    return prices.get(symbol, 100.0)  # Default price is 100 if symbol not found


class Account:
    """
    A class representing a trading account with functionality for managing funds,
    buying/selling shares, and tracking transactions and portfolio value.
    """
    
    def __init__(self, username, initial_deposit):
        """
        Initialize a new account with the username and initial deposit.
        
        Args:
            username (str): The name of the account holder
            initial_deposit (float): The initial amount deposited
        """
        if initial_deposit <= 0:
            raise ValueError("Initial deposit must be greater than zero")
            
        self.username = username
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []
        
        # Record the initial deposit as a transaction
        self.transactions.append({
            'type': 'deposit',
            'amount': initial_deposit,
            'timestamp': 'initial deposit'
        })
    
    def deposit(self, amount):
        """
        Increase the balance by the specified amount.
        
        Args:
            amount (float): The amount to deposit
            
        Returns:
            None
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero")
            
        self.balance += amount
        
        # Record the transaction
        self.transactions.append({
            'type': 'deposit',
            'amount': amount,
            'timestamp': 'deposit'
        })
    
    def withdraw(self, amount):
        """
        Decrease the balance by the specified amount if sufficient balance is available.
        
        Args:
            amount (float): The amount to withdraw
            
        Returns:
            bool: True if the withdrawal is successful, otherwise False
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero")
            
        if amount > self.balance:
            return False
        
        self.balance -= amount
        
        # Record the transaction
        self.transactions.append({
            'type': 'withdrawal',
            'amount': amount,
            'timestamp': 'withdrawal'
        })
        
        return True
    
    def buy_shares(self, symbol, quantity):
        """
        Buy a specific quantity of shares of the given symbol if enough balance is available.
        
        Args:
            symbol (str): The stock symbol to buy
            quantity (int): The number of shares to buy
            
        Returns:
            bool: True if the purchase is successful, otherwise False
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
            
        price = get_share_price(symbol)
        total_cost = price * quantity
        
        if total_cost > self.balance:
            return False
        
        # Update balance
        self.balance -= total_cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        # Record the transaction
        self.transactions.append({
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_cost,
            'timestamp': 'buy'
        })
        
        return True
    
    def sell_shares(self, symbol, quantity):
        """
        Sell a specific quantity of shares of the given symbol if enough shares are available in holdings.
        
        Args:
            symbol (str): The stock symbol to sell
            quantity (int): The number of shares to sell
            
        Returns:
            bool: True if the sale is successful, otherwise False
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
            
        # Check if the user has enough shares
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        
        price = get_share_price(symbol)
        total_value = price * quantity
        
        # Update balance
        self.balance += total_value
        
        # Update holdings
        self.holdings[symbol] -= quantity
        
        # Remove the symbol from holdings if no shares left
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        # Record the transaction
        self.transactions.append({
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'total': total_value,
            'timestamp': 'sell'
        })
        
        return True
    
    def calculate_portfolio_value(self):
        """
        Calculate and return the total current value of all holdings.
        
        Returns:
            float: The total value of all holdings
        """
        total_value = 0.0
        
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            total_value += price * quantity
        
        return total_value
    
    def calculate_profit_loss(self):
        """
        Calculate and return the difference between current portfolio value and initial deposit.
        
        Returns:
            float: The profit or loss amount
        """
        portfolio_value = self.calculate_portfolio_value()
        total_assets = portfolio_value + self.balance
        return total_assets - self.initial_deposit
    
    def get_holdings(self):
        """
        Return a dictionary of current holdings.
        
        Returns:
            dict: A dictionary of current holdings
        """
        return self.holdings.copy()
    
    def get_profit_loss(self):
        """
        Calculate and return net profit or loss.
        
        Returns:
            float: The profit or loss amount
        """
        return self.calculate_profit_loss()
    
    def get_transactions(self):
        """
        Return a list of all transactions recorded.
        
        Returns:
            list: A list of all transactions
        """
        return self.transactions.copy()