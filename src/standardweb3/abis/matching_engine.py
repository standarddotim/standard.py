matching_engine_abi = matching_engine_abi = [
    {"type": "constructor", "inputs": [], "stateMutability": "nonpayable"},
    {"type": "receive", "stateMutability": "payable"},
    {
        "type": "function",
        "name": "DEFAULT_ADMIN_ROLE",
        "inputs": [],
        "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "DENOM",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint32", "internalType": "uint32"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "WETH",
        "inputs": [],
        "outputs": [{"name": "", "type": "address", "internalType": "address"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "addPair",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "listingPrice", "type": "uint256", "internalType": "uint256"},
            {"name": "listingDate", "type": "uint256", "internalType": "uint256"},
            {"name": "payment", "type": "address", "internalType": "address"},
        ],
        "outputs": [{"name": "pair", "type": "address", "internalType": "address"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "addPairETH",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "listingPrice", "type": "uint256", "internalType": "uint256"},
            {"name": "listingDate", "type": "uint256", "internalType": "uint256"},
        ],
        "outputs": [{"name": "book", "type": "address", "internalType": "address"}],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "cancelOrder",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "isBid", "type": "bool", "internalType": "bool"},
            {"name": "orderId", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "cancelOrders",
        "inputs": [
            {
                "name": "cancelOrderData",
                "type": "tuple[]",
                "internalType": "struct IMatchingEngine.CancelOrderInput[]",
                "components": [
                    {"name": "base", "type": "address", "internalType": "address"},
                    {"name": "quote", "type": "address", "internalType": "address"},
                    {"name": "isBid", "type": "bool", "internalType": "bool"},
                    {"name": "orderId", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "outputs": [
            {"name": "refunded", "type": "uint256[]", "internalType": "uint256[]"}
        ],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "convert",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "amount", "type": "uint256", "internalType": "uint256"},
            {"name": "isBid", "type": "bool", "internalType": "bool"},
        ],
        "outputs": [
            {"name": "converted", "type": "uint256", "internalType": "uint256"}
        ],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "createOrder",
        "inputs": [
            {
                "name": "createOrderData",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.CreateOrderInput",
                "components": [
                    {"name": "base", "type": "address", "internalType": "address"},
                    {"name": "quote", "type": "address", "internalType": "address"},
                    {"name": "isBid", "type": "bool", "internalType": "bool"},
                    {"name": "isLimit", "type": "bool", "internalType": "bool"},
                    {"name": "orderId", "type": "uint32", "internalType": "uint32"},
                    {"name": "price", "type": "uint256", "internalType": "uint256"},
                    {"name": "amount", "type": "uint256", "internalType": "uint256"},
                    {"name": "n", "type": "uint32", "internalType": "uint32"},
                    {"name": "recipient", "type": "address", "internalType": "address"},
                ],
            }
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "createOrders",
        "inputs": [
            {
                "name": "createOrderData",
                "type": "tuple[]",
                "internalType": "struct IMatchingEngine.CreateOrderInput[]",
                "components": [
                    {"name": "base", "type": "address", "internalType": "address"},
                    {"name": "quote", "type": "address", "internalType": "address"},
                    {"name": "isBid", "type": "bool", "internalType": "bool"},
                    {"name": "isLimit", "type": "bool", "internalType": "bool"},
                    {"name": "orderId", "type": "uint32", "internalType": "uint32"},
                    {"name": "price", "type": "uint256", "internalType": "uint256"},
                    {"name": "amount", "type": "uint256", "internalType": "uint256"},
                    {"name": "n", "type": "uint32", "internalType": "uint32"},
                    {"name": "recipient", "type": "address", "internalType": "address"},
                ],
            }
        ],
        "outputs": [
            {
                "name": "results",
                "type": "tuple[]",
                "internalType": "struct IMatchingEngine.OrderResult[]",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "feeOf",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "account", "type": "address", "internalType": "address"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
        ],
        "outputs": [{"name": "feeNum", "type": "uint32", "internalType": "uint32"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "feeTo",
        "inputs": [],
        "outputs": [{"name": "", "type": "address", "internalType": "address"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "getOrder",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "isBid", "type": "bool", "internalType": "bool"},
            {"name": "orderId", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [
            {
                "name": "",
                "type": "tuple",
                "internalType": "struct ExchangeOrderbook.Order",
                "components": [
                    {"name": "owner", "type": "address", "internalType": "address"},
                    {"name": "price", "type": "uint256", "internalType": "uint256"},
                    {
                        "name": "depositAmount",
                        "type": "uint256",
                        "internalType": "uint256",
                    },
                ],
            }
        ],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "getPair",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
        ],
        "outputs": [{"name": "book", "type": "address", "internalType": "address"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "getRoleAdmin",
        "inputs": [{"name": "role", "type": "bytes32", "internalType": "bytes32"}],
        "outputs": [{"name": "", "type": "bytes32", "internalType": "bytes32"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "getSpread",
        "inputs": [
            {"name": "pair", "type": "address", "internalType": "address"},
            {"name": "isBuy", "type": "bool", "internalType": "bool"},
            {"name": "isMkt", "type": "bool", "internalType": "bool"},
        ],
        "outputs": [
            {"name": "spreadLimit", "type": "uint32", "internalType": "uint32"}
        ],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "grantRole",
        "inputs": [
            {"name": "role", "type": "bytes32", "internalType": "bytes32"},
            {"name": "account", "type": "address", "internalType": "address"},
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "hasRole",
        "inputs": [
            {"name": "role", "type": "bytes32", "internalType": "bytes32"},
            {"name": "account", "type": "address", "internalType": "address"},
        ],
        "outputs": [{"name": "", "type": "bool", "internalType": "bool"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "heads",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
        ],
        "outputs": [
            {"name": "bidHead", "type": "uint256", "internalType": "uint256"},
            {"name": "askHead", "type": "uint256", "internalType": "uint256"},
        ],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "incentive",
        "inputs": [],
        "outputs": [{"name": "", "type": "address", "internalType": "address"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "initialize",
        "inputs": [
            {"name": "orderbookFactory_", "type": "address", "internalType": "address"},
            {"name": "feeTo_", "type": "address", "internalType": "address"},
            {"name": "WETH_", "type": "address", "internalType": "address"},
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "limitBuy",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "price", "type": "uint256", "internalType": "uint256"},
            {"name": "quoteAmount", "type": "uint256", "internalType": "uint256"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "limitBuyETH",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "price", "type": "uint256", "internalType": "uint256"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "limitSell",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "price", "type": "uint256", "internalType": "uint256"},
            {"name": "baseAmount", "type": "uint256", "internalType": "uint256"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "limitSellETH",
        "inputs": [
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "price", "type": "uint256", "internalType": "uint256"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "listingDates",
        "inputs": [{"name": "", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "lmtSpreadLimits",
        "inputs": [{"name": "", "type": "address", "internalType": "address"}],
        "outputs": [
            {"name": "buy", "type": "uint32", "internalType": "uint32"},
            {"name": "sell", "type": "uint32", "internalType": "uint32"},
        ],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "marketBuy",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "quoteAmount", "type": "uint256", "internalType": "uint256"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
            {"name": "slippageLimit", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "marketBuyETH",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
            {"name": "slippageLimit", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "marketSell",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "baseAmount", "type": "uint256", "internalType": "uint256"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
            {"name": "slippageLimit", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "marketSellETH",
        "inputs": [
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "n", "type": "uint32", "internalType": "uint32"},
            {"name": "recipient", "type": "address", "internalType": "address"},
            {"name": "slippageLimit", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "mktPrice",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
        ],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "mktSpreadLimits",
        "inputs": [{"name": "", "type": "address", "internalType": "address"}],
        "outputs": [
            {"name": "buy", "type": "uint32", "internalType": "uint32"},
            {"name": "sell", "type": "uint32", "internalType": "uint32"},
        ],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "orderbookFactory",
        "inputs": [],
        "outputs": [{"name": "", "type": "address", "internalType": "address"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "renounceRole",
        "inputs": [
            {"name": "role", "type": "bytes32", "internalType": "bytes32"},
            {
                "name": "callerConfirmation",
                "type": "address",
                "internalType": "address",
            },
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "revokeRole",
        "inputs": [
            {"name": "role", "type": "bytes32", "internalType": "bytes32"},
            {"name": "account", "type": "address", "internalType": "address"},
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setDefaultFee",
        "inputs": [
            {"name": "isMaker", "type": "bool", "internalType": "bool"},
            {"name": "fee_", "type": "uint32", "internalType": "uint32"},
        ],
        "outputs": [{"name": "success", "type": "bool", "internalType": "bool"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setDefaultSpread",
        "inputs": [
            {"name": "buy", "type": "uint32", "internalType": "uint32"},
            {"name": "sell", "type": "uint32", "internalType": "uint32"},
            {"name": "isMkt", "type": "bool", "internalType": "bool"},
        ],
        "outputs": [{"name": "success", "type": "bool", "internalType": "bool"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setFeeTo",
        "inputs": [{"name": "feeTo_", "type": "address", "internalType": "address"}],
        "outputs": [{"name": "success", "type": "bool", "internalType": "bool"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setIncentive",
        "inputs": [
            {"name": "incentive_", "type": "address", "internalType": "address"}
        ],
        "outputs": [{"name": "success", "type": "bool", "internalType": "bool"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setListingCost",
        "inputs": [
            {"name": "terminal", "type": "string", "internalType": "string"},
            {"name": "payment", "type": "address", "internalType": "address"},
            {"name": "amount", "type": "uint256", "internalType": "uint256"},
        ],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setMaxMatches",
        "inputs": [{"name": "n", "type": "uint32", "internalType": "uint32"}],
        "outputs": [{"name": "success", "type": "bool", "internalType": "bool"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "setSpread",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "buy", "type": "uint32", "internalType": "uint32"},
            {"name": "sell", "type": "uint32", "internalType": "uint32"},
            {"name": "isMkt", "type": "bool", "internalType": "bool"},
        ],
        "outputs": [{"name": "success", "type": "bool", "internalType": "bool"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "supportsInterface",
        "inputs": [{"name": "interfaceId", "type": "bytes4", "internalType": "bytes4"}],
        "outputs": [{"name": "", "type": "bool", "internalType": "bool"}],
        "stateMutability": "view",
    },
    {
        "type": "function",
        "name": "updateOrder",
        "inputs": [
            {
                "name": "updateOrderData",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.CreateOrderInput",
                "components": [
                    {"name": "base", "type": "address", "internalType": "address"},
                    {"name": "quote", "type": "address", "internalType": "address"},
                    {"name": "isBid", "type": "bool", "internalType": "bool"},
                    {"name": "isLimit", "type": "bool", "internalType": "bool"},
                    {"name": "orderId", "type": "uint32", "internalType": "uint32"},
                    {"name": "price", "type": "uint256", "internalType": "uint256"},
                    {"name": "amount", "type": "uint256", "internalType": "uint256"},
                    {"name": "n", "type": "uint32", "internalType": "uint32"},
                    {"name": "recipient", "type": "address", "internalType": "address"},
                ],
            }
        ],
        "outputs": [
            {
                "name": "result",
                "type": "tuple",
                "internalType": "struct IMatchingEngine.OrderResult",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "nonpayable",
    },
    {
        "type": "function",
        "name": "updateOrders",
        "inputs": [
            {
                "name": "updateOrderData",
                "type": "tuple[]",
                "internalType": "struct IMatchingEngine.CreateOrderInput[]",
                "components": [
                    {"name": "base", "type": "address", "internalType": "address"},
                    {"name": "quote", "type": "address", "internalType": "address"},
                    {"name": "isBid", "type": "bool", "internalType": "bool"},
                    {"name": "isLimit", "type": "bool", "internalType": "bool"},
                    {"name": "orderId", "type": "uint32", "internalType": "uint32"},
                    {"name": "price", "type": "uint256", "internalType": "uint256"},
                    {"name": "amount", "type": "uint256", "internalType": "uint256"},
                    {"name": "n", "type": "uint32", "internalType": "uint32"},
                    {"name": "recipient", "type": "address", "internalType": "address"},
                ],
            }
        ],
        "outputs": [
            {
                "name": "results",
                "type": "tuple[]",
                "internalType": "struct IMatchingEngine.OrderResult[]",
                "components": [
                    {"name": "makePrice", "type": "uint256", "internalType": "uint256"},
                    {"name": "placed", "type": "uint256", "internalType": "uint256"},
                    {"name": "id", "type": "uint32", "internalType": "uint32"},
                ],
            }
        ],
        "stateMutability": "payable",
    },
    {
        "type": "function",
        "name": "updatePair",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "listingPrice", "type": "uint256", "internalType": "uint256"},
            {"name": "listingDate", "type": "uint256", "internalType": "uint256"},
        ],
        "outputs": [{"name": "pair", "type": "address", "internalType": "address"}],
        "stateMutability": "nonpayable",
    },
    {
        "type": "event",
        "name": "ListingCostSet",
        "inputs": [
            {
                "name": "payment",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "amount",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "NewMarketPrice",
        "inputs": [
            {
                "name": "pair",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "price",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {"name": "isBid", "type": "bool", "indexed": False, "internalType": "bool"},
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "OrderCanceled",
        "inputs": [
            {
                "name": "pair",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "id",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {"name": "isBid", "type": "bool", "indexed": False, "internalType": "bool"},
            {
                "name": "owner",
                "type": "address",
                "indexed": True,
                "internalType": "address",
            },
            {
                "name": "amount",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "OrderMatched",
        "inputs": [
            {
                "name": "pair",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "orderHistoryId",
                "type": "uint16",
                "indexed": False,
                "internalType": "uint16",
            },
            {
                "name": "id",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {"name": "isBid", "type": "bool", "indexed": False, "internalType": "bool"},
            {
                "name": "price",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "total",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {"name": "clear", "type": "bool", "indexed": False, "internalType": "bool"},
            {
                "name": "orderMatch",
                "type": "tuple",
                "indexed": False,
                "internalType": "struct IMatchingEngine.OrderMatch",
                "components": [
                    {"name": "sender", "type": "address", "internalType": "address"},
                    {"name": "owner", "type": "address", "internalType": "address"},
                    {
                        "name": "baseAmount",
                        "type": "uint256",
                        "internalType": "uint256",
                    },
                    {
                        "name": "quoteAmount",
                        "type": "uint256",
                        "internalType": "uint256",
                    },
                    {"name": "baseFee", "type": "uint256", "internalType": "uint256"},
                    {"name": "quoteFee", "type": "uint256", "internalType": "uint256"},
                    {"name": "tradeId", "type": "uint64", "internalType": "uint64"},
                ],
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "OrderPlaced",
        "inputs": [
            {
                "name": "pair",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "orderHistoryId",
                "type": "uint16",
                "indexed": False,
                "internalType": "uint16",
            },
            {
                "name": "id",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "owner",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {"name": "isBid", "type": "bool", "indexed": False, "internalType": "bool"},
            {
                "name": "price",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "withoutFee",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "placed",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "PairAdded",
        "inputs": [
            {
                "name": "pair",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "base",
                "type": "tuple",
                "indexed": False,
                "internalType": "struct TransferHelper.TokenInfo",
                "components": [
                    {"name": "token", "type": "address", "internalType": "address"},
                    {"name": "decimals", "type": "uint8", "internalType": "uint8"},
                    {"name": "name", "type": "string", "internalType": "string"},
                    {"name": "symbol", "type": "string", "internalType": "string"},
                    {
                        "name": "totalSupply",
                        "type": "uint256",
                        "internalType": "uint256",
                    },
                ],
            },
            {
                "name": "quote",
                "type": "tuple",
                "indexed": False,
                "internalType": "struct TransferHelper.TokenInfo",
                "components": [
                    {"name": "token", "type": "address", "internalType": "address"},
                    {"name": "decimals", "type": "uint8", "internalType": "uint8"},
                    {"name": "name", "type": "string", "internalType": "string"},
                    {"name": "symbol", "type": "string", "internalType": "string"},
                    {
                        "name": "totalSupply",
                        "type": "uint256",
                        "internalType": "uint256",
                    },
                ],
            },
            {
                "name": "listingPrice",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "listingDate",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "supportedTerminals",
                "type": "string",
                "indexed": False,
                "internalType": "string",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "PairCreate2",
        "inputs": [
            {
                "name": "deployer",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "bytecode",
                "type": "bytes",
                "indexed": False,
                "internalType": "bytes",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "PairUpdated",
        "inputs": [
            {
                "name": "pair",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "base",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "quote",
                "type": "address",
                "indexed": False,
                "internalType": "address",
            },
            {
                "name": "listingPrice",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
            {
                "name": "listingDate",
                "type": "uint256",
                "indexed": False,
                "internalType": "uint256",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "RoleAdminChanged",
        "inputs": [
            {
                "name": "role",
                "type": "bytes32",
                "indexed": True,
                "internalType": "bytes32",
            },
            {
                "name": "previousAdminRole",
                "type": "bytes32",
                "indexed": True,
                "internalType": "bytes32",
            },
            {
                "name": "newAdminRole",
                "type": "bytes32",
                "indexed": True,
                "internalType": "bytes32",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "RoleGranted",
        "inputs": [
            {
                "name": "role",
                "type": "bytes32",
                "indexed": True,
                "internalType": "bytes32",
            },
            {
                "name": "account",
                "type": "address",
                "indexed": True,
                "internalType": "address",
            },
            {
                "name": "sender",
                "type": "address",
                "indexed": True,
                "internalType": "address",
            },
        ],
        "anonymous": False,
    },
    {
        "type": "event",
        "name": "RoleRevoked",
        "inputs": [
            {
                "name": "role",
                "type": "bytes32",
                "indexed": True,
                "internalType": "bytes32",
            },
            {
                "name": "account",
                "type": "address",
                "indexed": True,
                "internalType": "address",
            },
            {
                "name": "sender",
                "type": "address",
                "indexed": True,
                "internalType": "address",
            },
        ],
        "anonymous": False,
    },
    {"type": "error", "name": "AccessControlBadConfirmation", "inputs": []},
    {
        "type": "error",
        "name": "AccessControlUnauthorizedAccount",
        "inputs": [
            {"name": "account", "type": "address", "internalType": "address"},
            {"name": "neededRole", "type": "bytes32", "internalType": "bytes32"},
        ],
    },
    {
        "type": "error",
        "name": "AlreadyInitialized",
        "inputs": [{"name": "init", "type": "bool", "internalType": "bool"}],
    },
    {"type": "error", "name": "AmountIsZero", "inputs": []},
    {
        "type": "error",
        "name": "FactoryNotInitialized",
        "inputs": [{"name": "factory", "type": "address", "internalType": "address"}],
    },
    {
        "type": "error",
        "name": "InvalidPair",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "pair", "type": "address", "internalType": "address"},
        ],
    },
    {
        "type": "error",
        "name": "InvalidRole",
        "inputs": [
            {"name": "role", "type": "bytes32", "internalType": "bytes32"},
            {"name": "sender", "type": "address", "internalType": "address"},
        ],
    },
    {
        "type": "error",
        "name": "InvalidTerminal",
        "inputs": [{"name": "terminal", "type": "address", "internalType": "address"}],
    },
    {
        "type": "error",
        "name": "OrderSizeTooSmall",
        "inputs": [
            {"name": "amount", "type": "uint256", "internalType": "uint256"},
            {"name": "minRequired", "type": "uint256", "internalType": "uint256"},
        ],
    },
    {
        "type": "error",
        "name": "PairDoesNotExist",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "pair", "type": "address", "internalType": "address"},
        ],
    },
    {
        "type": "error",
        "name": "PairNotListedYet",
        "inputs": [
            {"name": "base", "type": "address", "internalType": "address"},
            {"name": "quote", "type": "address", "internalType": "address"},
            {"name": "listingDate", "type": "uint256", "internalType": "uint256"},
            {"name": "timeNow", "type": "uint256", "internalType": "uint256"},
        ],
    },
    {"type": "error", "name": "ReentrancyGuardReentrantCall", "inputs": []},
    {
        "type": "error",
        "name": "TooManyMatches",
        "inputs": [{"name": "n", "type": "uint256", "internalType": "uint256"}],
    },
]
