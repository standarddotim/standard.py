# CSV Limit Orders Examples

This directory contains examples demonstrating how to submit limit orders by reading data from CSV files using pandas and numpy.

## Files

### 1. `csv_limit_orders_example.py` - Advanced CSV Orders
**Full-featured example with comprehensive data processing and batch operations.**

**Features:**
- ✅ **Pandas Data Loading**: Load and validate CSV data with error handling
- ✅ **NumPy Statistics**: Calculate price statistics and token distributions
- ✅ **Data Filtering**: Filter orders by price range and limit quantities
- ✅ **Batch Processing**: Submit orders in batches to manage gas limits
- ✅ **Buy/Sell Orders**: Create both buy and sell order strategies
- ✅ **Error Handling**: Robust error handling for failed transactions

**Usage:**
```bash
uv run src/standardweb3/examples/csv_limit_orders_example.py
```

### 2. `csv_simple_orders_example.py` - Simple CSV Orders
**Simplified example focusing on basic CSV reading and order submission.**

**Features:**
- ✅ **Simple CSV Reading**: Basic pandas CSV loading
- ✅ **NumPy Calculations**: Vectorized price and amount calculations
- ✅ **Small Orders**: Realistic order sizes for testing
- ✅ **Data Analysis**: Basic pandas and numpy statistical analysis
- ✅ **Clear Output**: Human-readable order confirmation

**Usage:**
```bash
uv run src/standardweb3/examples/csv_simple_orders_example.py
```

## CSV Data Format

The examples expect CSV files with the following structure:

```csv
Step,Price,Tokens,Value(USD),Cumulative Tokens,Cumulative Value(USD)
1,0.000032,5421686.7470,173.493976,5421686.7470,173.493976
2,0.000034,5421686.7470,184.337349,10843373.4940,357.831325
3,0.000035,5421686.7470,189.759036,16265060.2410,547.590361
...
```

**Required Columns:**
- `Price`: Price per token in USD
- `Tokens`: Number of tokens at this price level

**Optional Columns:**
- `Step`: Step number in the price ladder
- `Value(USD)`: USD value at this step
- `Cumulative Tokens`: Running total of tokens
- `Cumulative Value(USD)`: Running total of USD value

## Dependencies

The CSV examples require additional Python packages:

```bash
uv add pandas numpy
```

## Key Features Demonstrated

### 1. **Pandas Data Processing**
```python
# Load CSV data
df = pd.read_csv("price_data.csv")

# Filter data
filtered_df = df[df['Price'] <= 0.0001]

# Statistical analysis
print(f"Average price: ${df['Price'].mean():.6f}")
print(f"Price range: ${df['Price'].min():.6f} - ${df['Price'].max():.6f}")
```

### 2. **NumPy Vectorized Calculations**
```python
# Vectorized price calculations
prices = df['Price'].values * 0.95  # 5% below CSV prices
amounts = np.full(len(prices), 10.0)  # $10 orders

# Statistical calculations
price_std = np.std(df['Price'].values)
price_increases = np.diff(df['Price'].values)
```

### 3. **Order Creation from CSV Data**
```python
orders = []
for i, (price, amount) in enumerate(zip(prices, amounts)):
    order = {
        "base": base_token,
        "quote": quote_token,
        "isBid": True,
        "isLimit": True,
        "orderId": i + 1,
        "price": parse_units(price, 6),  # USDC decimals
        "amount": parse_units(amount, 6),
        "n": 1,
        "recipient": client.address,
        "isETH": False,
    }
    orders.append(order)
```

### 4. **Batch Order Submission**
```python
# Submit in batches to manage gas limits
for i in range(0, len(orders), batch_size):
    batch = orders[i:i + batch_size]
    result = await client.create_orders(batch)

    if result and result.get('status') == 1:
        print(f"✅ Batch {batch_num} successful!")
```

## Configuration

### Environment Variables
```bash
# .env file
RPC_URL=https://rpc.testnet.mode.network
PRIVATE_KEY=your_private_key_here
NETWORK=Somnia Testnet
```

### Token Addresses (Testnet)
```python
base_token = "0x4A3BC48C156384f9564Fd65A53a2f3D534D8f2b7"  # STT
quote_token = "0x0ED782B8079529f7385c3eDA9fAf1EaA0DbC6a17"  # USDC
```

## Example Output

### Simple CSV Orders
```
🚀 Simple CSV Limit Orders Example
Account: 0xF8FB4672170607C95663f4Cc674dDb1386b7CfE0
Network: Somnia Testnet

📂 Loading CSV data...
Loaded 166 price points
Using 3 price points for demo

📊 Price Data:
  Step 1: $0.000032 per token
  Step 2: $0.000034 per token
  Step 3: $0.000035 per token

🛒 Creating Buy Orders...
  Order 1: Buy at $0.000030 with $10.0 USDC
  Order 2: Buy at $0.000032 with $10.0 USDC
  Order 3: Buy at $0.000033 with $10.0 USDC

✅ Orders submitted successfully!
  TX Hash: 38735bb4b244ce05cf64594c77df1dc95b423ca8675af0a593ff65108d036686
  Gas Used: 3,111,773
  📊 Orders Placed: 3
```

### Advanced CSV Orders
```
📊 Loaded CSV with 166 rows and 6 columns
Columns: ['Step', 'Price', 'Tokens', 'Value(USD)', 'Cumulative Tokens', 'Cumulative Value(USD)']

📈 Price Statistics:
  Min Price: $0.000032
  Max Price: $0.100000
  Mean Price: $0.012652
  Median Price: $0.001789

🛒 Prepared 5 buy orders
📦 Submitting 5 orders in 2 batches of 3

✅ Batch 1 successful!
  TX Hash: 169f3768d37b527bb0d9e553c6841d78694eef0bb7d6f122d46a307e31382c19
  Gas Used: 3,773,318
  📊 Orders Placed: 3
```

## Trading Strategies

### 1. **Price Ladder Strategy**
- Read price levels from CSV
- Create buy orders below market price
- Create sell orders above market price
- Profit from bid-ask spread

### 2. **Volume-Based Strategy**
- Use token volume data from CSV
- Scale order sizes based on volume
- Larger orders at high-volume price levels

### 3. **Statistical Strategy**
- Use numpy to calculate price statistics
- Place orders at statistical levels (mean, median, percentiles)
- Dynamic pricing based on historical data

## Best Practices

1. **Data Validation**: Always validate CSV data before processing
2. **Batch Processing**: Submit orders in small batches to manage gas costs
3. **Error Handling**: Handle failed transactions gracefully
4. **Decimal Precision**: Use `parse_units` for proper decimal handling
5. **Gas Management**: Monitor and adjust gas limits for batch operations
6. **Rate Limiting**: Add delays between batch submissions

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Install pandas and numpy
   ```bash
   uv add pandas numpy
   ```

2. **"Transaction failed" errors**: Usually due to insufficient balance or gas limits
   - Check account balance
   - Reduce order sizes
   - Increase gas limits

3. **CSV format errors**: Ensure CSV has required columns (`Price`, `Tokens`)

4. **Decimal precision errors**: Use `parse_units()` for consistent decimal handling

### Gas Optimization

- **Batch Size**: Use 3-5 orders per batch for optimal gas usage
- **Gas Limits**: Start with 3M gas per batch, adjust based on results
- **Order Complexity**: Simple limit orders use less gas than complex orders

## Advanced Usage

### Custom CSV Processing
```python
# Custom filtering with pandas
high_volume_orders = df[df['Tokens'] > df['Tokens'].quantile(0.8)]
low_price_orders = df[df['Price'] < df['Price'].median()]

# Combine conditions
filtered_orders = df[
    (df['Price'] >= min_price) &
    (df['Price'] <= max_price) &
    (df['Tokens'] >= min_volume)
]
```

### Advanced NumPy Calculations
```python
# Price percentiles
price_25th = np.percentile(df['Price'].values, 25)
price_75th = np.percentile(df['Price'].values, 75)

# Moving averages
window_size = 5
moving_avg = np.convolve(df['Price'].values,
                        np.ones(window_size)/window_size,
                        mode='valid')
```

This comprehensive CSV integration allows for sophisticated trading strategies based on external data sources! 🚀📊
