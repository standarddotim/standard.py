# Order Management Examples for Standard Protocol

This directory contains comprehensive examples for managing orders on the Standard Protocol exchange, including creating, updating, and cancelling orders both individually and in batches.

## Overview

The Standard Protocol provides three main order management functions:
- **`create_orders`** - Create new limit or market orders
- **`update_orders`** - Modify existing orders (price, amount, etc.)
- **`cancel_orders`** - Cancel existing orders

## Quick Start

### 1. Basic Order Creation

```python
from standardweb3 import StandardClient

# Initialize client
client = StandardClient(
    private_key="your_private_key",
    http_rpc_url="https://your-rpc-url.com",
    networkName="Somnia Testnet"
)

# Create order data
order_data = {
    "base": "0x...",              # Base token address
    "quote": "0x...",             # Quote token address
    "isBid": True,                # True=Buy, False=Sell
    "isLimit": True,              # True=Limit, False=Market
    "orderId": 0,                 # 0 for new orders
    "price": int(2000 * 10**18),  # Price in wei
    "amount": int(1 * 10**18),    # Amount in wei
    "n": 1,                       # Number parameter
    "recipient": client.account.address,
    "isETH": False,               # True for ETH orders
}

# Create the order
result = await client.create_orders([order_data])
```

### 2. Order Update

```python
# Update existing order
update_data = {
    "base": "0x...",
    "quote": "0x...",
    "isBid": True,
    "isLimit": True,
    "orderId": 12345,             # Existing order ID
    "price": int(1950 * 10**18),  # New price
    "amount": int(1.2 * 10**18),  # New amount
    "n": 1,
    "recipient": client.account.address,
    "isETH": False,
}

result = await client.update_orders([update_data])
```

### 3. Order Cancellation

```python
# Cancel order using formatted ID string
cancel_id = f"{base_token}_{quote_token}_{is_buy}_{order_id}"
tx_hash = await client.cancel_orders([cancel_id])
```

## Available Examples

### 1. `simple_order_example.py`
**Best for beginners** - Basic examples showing:
- Single order creation
- Order updates
- Order cancellation
- Batch order creation

**Run it:**
```bash
python src/standardweb3/examples/simple_order_example.py
```

### 2. `order_management_example.py`
**Advanced features** - Comprehensive examples with:
- Order management helper class
- Grid trading strategies
- Dollar-cost averaging (DCA)
- Batch operations
- Error handling
- Advanced trading patterns

**Run it:**
```bash
python src/standardweb3/examples/order_management_example.py
```

## Order Data Structure

### Required Fields

All order operations require these fields:

```python
{
    "base": "0x...",          # Base token contract address
    "quote": "0x...",         # Quote token contract address
    "isBid": bool,            # True for buy orders, False for sell
    "isLimit": bool,          # True for limit, False for market
    "orderId": int,           # Order ID (0 for new, existing ID for updates)
    "price": int,             # Price in wei (18 decimals)
    "amount": int,            # Amount in wei (18 decimals)
    "n": int,                 # Number parameter (usually 1)
    "recipient": "0x...",     # Recipient address
    "isETH": bool,            # True if using ETH directly
}
```

### Price and Amount Conversion

```python
# Convert from human-readable to wei
price_wei = int(price_usd * 10**18)
amount_wei = int(amount_tokens * 10**18)

# Example: $2000 per ETH, 1.5 ETH
order_data = {
    # ... other fields ...
    "price": int(2000 * 10**18),   # $2000 in wei
    "amount": int(1.5 * 10**18),   # 1.5 ETH in wei
}
```

## Order Types

### 1. Limit Orders
```python
{
    "isBid": True,      # Buy order
    "isLimit": True,    # Limit order
    "price": int(2000 * 10**18),  # Specific price
    "amount": int(1 * 10**18),    # Amount to buy
}
```

### 2. Market Orders
```python
{
    "isBid": True,      # Buy order
    "isLimit": False,   # Market order
    "price": 0,         # Price ignored for market orders
    "amount": int(1 * 10**18),    # Amount to buy
}
```

### 3. ETH Orders
```python
{
    "base": "0x0000000000000000000000000000000000000000",  # ETH address
    "quote": "0x...",   # Quote token
    "isETH": True,      # Using ETH directly
    # ... other fields ...
}
```

## Batch Operations

### Create Multiple Orders
```python
batch_orders = [
    {
        "base": eth_address,
        "quote": usdc_address,
        "isBid": True,
        "isLimit": True,
        "price": int(1900 * 10**18),
        "amount": int(0.5 * 10**18),
        # ... other fields ...
    },
    {
        "base": eth_address,
        "quote": usdc_address,
        "isBid": True,
        "isLimit": True,
        "price": int(1850 * 10**18),
        "amount": int(0.3 * 10**18),
        # ... other fields ...
    }
]

result = await client.create_orders(batch_orders)
```

### Update Multiple Orders
```python
update_orders = [
    {
        "orderId": 12345,
        "price": int(1950 * 10**18),  # New price
        # ... other fields same as original ...
    },
    {
        "orderId": 12346,
        "amount": int(2 * 10**18),    # New amount
        # ... other fields same as original ...
    }
]

result = await client.update_orders(update_orders)
```

### Cancel Multiple Orders
```python
cancel_ids = [
    "0x...eth_0x...usdc_True_12345",   # ETH/USDC buy order #12345
    "0x...eth_0x...usdc_False_12346",  # ETH/USDC sell order #12346
]

tx_hash = await client.cancel_orders(cancel_ids)
```

## Trading Strategies

### 1. Grid Trading
```python
base_price = 2000.0
grid_levels = 5
spacing = 50.0

for i in range(grid_levels):
    # Buy orders below market
    buy_price = base_price - (i + 1) * spacing
    buy_order = create_order_data(..., price=buy_price)

    # Sell orders above market
    sell_price = base_price + (i + 1) * spacing
    sell_order = create_order_data(..., price=sell_price)
```

### 2. Dollar Cost Averaging (DCA)
```python
investment_amount = 1000.0  # $1000 total
num_orders = 4
amount_per_order = investment_amount / num_orders

for i in range(num_orders):
    price = base_price * (0.95 + i * 0.02)  # Spread across price range
    eth_amount = amount_per_order / price
    order = create_order_data(..., price=price, amount=eth_amount)
```

### 3. Order Replacement Strategy
```python
# Cancel existing orders
await client.cancel_orders(existing_order_ids)

# Create new orders with updated prices
new_orders = create_updated_orders(new_market_conditions)
await client.create_orders(new_orders)
```

## Error Handling

### Common Validation Errors
```python
try:
    result = await client.create_orders(order_data)
except ValueError as e:
    if "missing required field" in str(e):
        print("Order data incomplete")
    elif "must be a list" in str(e):
        print("Order data must be in list format")
except Exception as e:
    print(f"Transaction failed: {e}")
```

### Transaction Result Checking
```python
result = await client.create_orders(order_data)

if result.get("status") == "success":
    print(f"✅ Success! TX: {result.get('tx_hash')}")
    order_info = result.get("order_info", {})
    order_id = order_info.get("orderId")
else:
    print(f"❌ Failed: {result}")
```

## Gas Management

### Automatic Gas Calculation
```python
# Gas is automatically calculated based on number of orders
# Minimum: 3,000,000 gas per order

# For batch operations, gas scales automatically:
batch_size = len(orders)
estimated_gas = 3_000_000 * batch_size
```

### Custom Gas Settings
```python
result = await client.create_orders(
    order_data,
    gas=5_000_000,        # Custom gas limit
    gas_price=8_000_000_000  # 8 gwei
)
```

## Best Practices

1. **Validate Data**: Always validate token addresses and amounts
2. **Handle Errors**: Implement proper error handling for all operations
3. **Batch Operations**: Use batch functions for multiple orders to save gas
4. **Track Order IDs**: Store order IDs for future updates/cancellations
5. **Price Precision**: Use wei for precise price calculations
6. **Gas Management**: Monitor gas costs for large batch operations

## Token Addresses

### Somnia Testnet
- **ETH**: `0x0000000000000000000000000000000000000000`
- **USDC**: `0xA0b86a33E6441c8C06DD2b7c47d2a82f0e7B3C2D` (example)
- **Other tokens**: Check the Standard Protocol documentation

## Common Issues

### 1. Invalid Address Format
```python
# ❌ Wrong
base_token = "invalid_address"

# ✅ Correct
base_token = "0x0000000000000000000000000000000000000000"
```

### 2. Incorrect Wei Conversion
```python
# ❌ Wrong - using float
price = 2000.5

# ✅ Correct - convert to wei integer
price = int(2000.5 * 10**18)
```

### 3. Missing Required Fields
```python
# ❌ Wrong - missing fields
order_data = {"base": "0x...", "quote": "0x..."}

# ✅ Correct - all required fields
order_data = {
    "base": "0x...",
    "quote": "0x...",
    "isBid": True,
    "isLimit": True,
    "orderId": 0,
    "price": int(2000 * 10**18),
    "amount": int(1 * 10**18),
    "n": 1,
    "recipient": "0x...",
    "isETH": False,
}
```

## Support

For issues or questions:
- Check the main Standard Protocol documentation
- Review the example code for implementation patterns
- Test with small amounts first
- Use the simple examples before advanced strategies
