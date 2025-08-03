# Trading Examples

This directory contains examples demonstrating how to use the StandardWeb3 contract functions for trading operations.

## Files

- `trading.py` - Comprehensive trading example with detailed error handling and multiple trading scenarios
- `simple_trading.py` - Minimal example showing basic contract function usage
- `bot.py` - Trading bot example (existing file)

## Setup

### 1. Install Dependencies

Make sure you have the required dependencies installed:

```bash
pip install web3 eth-account
```

### 2. Set Environment Variables

#### Option A: Using .env file (Recommended)

1. Copy the example environment file:
```bash
cp env.example .env
```

2. Edit `.env` and add your actual values:
```bash
# Your Ethereum private key (without 0x prefix)
PRIVATE_KEY=your_actual_private_key_here

# RPC URL for your network
RPC_URL=https://rpc.testnet.mode.network

# Network name
NETWORK=Somnia Testnet
```

#### Option B: Using environment variables

```bash
export PRIVATE_KEY="your_private_key_here"
export RPC_URL="https://rpc.testnet.mode.network"
export NETWORK="Somnia Testnet"
```

**⚠️ Security Warning**: Never commit your private key to version control. The `.env` file is gitignored for your security.

### 3. Configure Network Settings

The examples use the following default settings:
- **Network**: Somnia Testnet
- **RPC URL**: https://rpc.testnet.mode.network
- **Matching Engine**: Automatically selected based on network

You can modify these in the example files or set them as environment variables.

## Usage

### Running the Simple Example

```bash
# Using uv (recommended)
uv run src/standardweb3/examples/simple_trading.py

# Or using python directly
python src/standardweb3/examples/simple_trading.py
```

### Running the Comprehensive Example

```bash
# Using uv (recommended)
uv run src/standardweb3/examples/trading.py

# Or using python directly
python trading.py
```

## Example Output

```
🚀 Simple Trading Example
==============================
Account: 0x1234...5678
Network: Somnia Testnet
Matching Engine: 0x8c1f7817657aae22e22ce84d552fe0c01bd8a254
----------------------------------------

📈 Market Buy Example
✅ Market buy successful! TX: 0xabcd...1234

💰 Limit Buy Example
✅ Limit buy successful! TX: 0xefgh...5678

📉 Market Sell Example
✅ Market sell successful! TX: 0xijkl...9012

💸 Limit Sell Example
✅ Limit sell successful! TX: 0xmnop...3456

✅ Example completed!
```

## Trading Functions

The examples demonstrate the following trading operations:

### Market Orders
- **Market Buy**: Buy tokens at the current market price
- **Market Sell**: Sell tokens at the current market price

### Limit Orders
- **Limit Buy**: Place a buy order at a specific price
- **Limit Sell**: Place a sell order at a specific price

## Parameters

### Common Parameters
- `base`: Address of the base token (token to buy/sell)
- `quote`: Address of the quote token (token to spend/receive)
- `is_maker`: Whether this is a maker order (affects fees)
- `n`: Number of matches (usually 1)
- `uid`: User ID (usually 0)
- `recipient`: Recipient address (defaults to sender)

### Market Orders
- `quote_amount`: Amount of quote token to spend (for market buy)
- `base_amount`: Amount of base token to sell (for market sell)

### Limit Orders
- `price`: Price per unit (in wei)
- `quote_amount`: Amount of quote token to spend (for limit buy)
- `base_amount`: Amount of base token to sell (for limit sell)

## Error Handling

The examples include comprehensive error handling for:
- Invalid private keys
- Network connectivity issues
- Insufficient funds
- Invalid token addresses
- Transaction failures

## Customization

### Using Different Networks

To use a different network, modify the network parameter:

```python
# For Mode Mainnet
NETWORK = "Mode Mainnet"

# For Somnia Testnet
NETWORK = "Somnia Testnet"
```

### Using Real Token Addresses

Replace the example token addresses with actual token addresses:

```python
# Example: USDC/ETH pair
base_token = "0xA0b86a33E6441b8c4C8C8C8C8C8C8C8C8C8C8C8"  # USDC
quote_token = "0x4200000000000000000000000000000000000006"  # WETH
```

### Adjusting Order Amounts

Modify the order amounts based on your needs:

```python
# For larger orders
quote_amount = w3.to_wei(1.0, 'ether')  # 1 ETH

# For smaller orders
quote_amount = w3.to_wei(0.0001, 'ether')  # 0.0001 ETH
```

## Troubleshooting

### Common Issues

1. **"Network not found"**: Check that the network name matches the keys in `matching_engine_addresses`
2. **"Invalid private key"**: Ensure your private key is correctly formatted (64 hex characters)
3. **"Insufficient funds"**: Make sure your account has enough tokens for the trade
4. **"Transaction failed"**: Check gas settings and ensure the contract supports the operation

### Debug Mode

To enable more detailed logging, you can modify the Web3 provider:

```python
w3 = Web3(Web3.HTTPProvider(RPC_URL))
w3.provider.request_counter = 0  # Enable request logging
```

## Security Notes

1. **Private Key Security**: Never hardcode private keys in your code
2. **Test Networks**: Always test on testnets before using mainnet
3. **Small Amounts**: Start with small amounts when testing
4. **Gas Limits**: Monitor gas usage and adjust limits as needed

## Support

For issues or questions:
1. Check the error messages for specific details
2. Verify your network and token addresses
3. Ensure you have sufficient funds for the transaction
4. Check the contract documentation for parameter requirements
