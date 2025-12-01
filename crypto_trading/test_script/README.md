# Test Script 使用说明

## get_symbols_by_volume.py

获取 Binance 所有合约和现货交易对列表，并按24小时交易量排序。

### 功能

- 获取所有现货交易对列表，按24小时交易量降序排序
- 获取所有合约交易对列表，按24小时交易量降序排序
- 在控制台显示前50个交易量最大的交易对
- 将结果保存为 JSON 文件到 `tmp/` 目录

### 使用方法

```bash
# 方式1: 作为模块运行（推荐）
cd /Users/user/Desktop/repo/crypto_trading
python -m crypto_trading.test_script.get_symbols_by_volume

# 方式2: 直接运行脚本
cd /Users/user/Desktop/repo/crypto_trading
python crypto_trading/test_script/get_symbols_by_volume.py
```

### 输出

脚本会在控制台显示：
- 现货交易对列表（前50个，按交易量排序）
- 合约交易对列表（前50个，按交易量排序）

同时会将完整列表保存为 JSON 文件：
- `tmp/spot_symbols_by_volume_YYYYMMDD_HHMMSS.json` - 现货交易对列表
- `tmp/futures_symbols_by_volume_YYYYMMDD_HHMMSS.json` - 合约交易对列表

### JSON 文件格式

每个 JSON 文件包含一个数组，每个元素包含：
```json
{
  "symbol": "BTCUSDT",
  "volume": 1234567890.12,
  "volume_str": "1,234,567,890.12"
}
```

### 注意事项

- 脚本使用公开 API，不需要 API Key 和 Secret（可以设置为空字符串）
- 交易量数据基于24小时滚动窗口
- 交易量以 USDT 计价（quoteVolume）

---

## test_order.py

测试 Binance 下单接口，包含现货和合约的买卖功能。

### 功能

- **现货交易测试**：
  - 市价买入/卖出
  - 限价买入/卖出
  
- **合约交易测试**：
  - 市价买入/卖出
  - 限价买入/卖出

- **撤单功能**：
  - 撤销现货订单（单个/批量）
  - 撤销合约订单
  - 查询当前挂单

### 使用方法

```bash
# 方式1: 作为模块运行（推荐）
cd /Users/user/Desktop/repo/crypto_trading
python -m crypto_trading.test_script.test_order

# 方式2: 直接运行脚本
cd /Users/user/Desktop/repo/crypto_trading
python crypto_trading/test_script/test_order.py
```

### 函数说明

#### 现货交易函数

- `test_spot_buy_market(symbol, quantity)` - 现货市价买入
- `test_spot_sell_market(symbol, quantity)` - 现货市价卖出
- `test_spot_buy_limit(symbol, quantity, price)` - 现货限价买入
- `test_spot_sell_limit(symbol, quantity, price)` - 现货限价卖出

#### 合约交易函数

- `test_futures_buy_market(symbol, quantity)` - 合约市价买入
- `test_futures_sell_market(symbol, quantity)` - 合约市价卖出
- `test_futures_buy_limit(symbol, quantity, price)` - 合约限价买入
- `test_futures_sell_limit(symbol, quantity, price)` - 合约限价卖出

#### 撤单函数

- `cancel_spot_order(symbol, order_id, orig_client_order_id)` - 撤销现货订单
- `cancel_futures_order(symbol, order_id, orig_client_order_id)` - 撤销合约订单
- `cancel_all_spot_orders(symbol)` - 撤销现货某个交易对的所有挂单
- `get_spot_open_orders(symbol)` - 获取现货当前挂单
- `get_futures_open_orders(symbol)` - 获取合约当前挂单
- `show_spot_open_orders(symbol)` - 显示现货当前挂单（格式化输出）
- `show_futures_open_orders(symbol)` - 显示合约当前挂单（格式化输出）

#### 通用函数

- `test_spot_order(symbol, side, order_type, quantity, price, time_in_force)` - 现货下单通用函数
- `test_futures_order(symbol, side, order_type, quantity, price, time_in_force, position_side, reduce_only)` - 合约下单通用函数

### 参数说明

- `symbol`: 交易对，如 "BTCUSDT"
- `side`: 买卖方向，"BUY" 或 "SELL"
- `order_type`: 订单类型，"MARKET" 或 "LIMIT"
- `quantity`: 数量（必需）
- `price`: 价格（LIMIT 订单必需）
- `time_in_force`: 有效期，"GTC", "IOC", "FOK"（默认 "GTC"）
- `position_side`: 持仓方向（仅合约），"LONG", "SHORT", "BOTH"
- `reduce_only`: 是否只减仓（仅合约），"true" 或 "false"

### 使用示例

```python
from crypto_trading.test_script.test_order import (
    test_spot_buy_market,
    test_spot_sell_market,
    test_futures_buy_market,
    test_futures_sell_market
)

# 现货市价买入 0.001 BTC
result = test_spot_buy_market("BTCUSDT", 0.001)

# 现货市价卖出 0.001 BTC
result = test_spot_sell_market("BTCUSDT", 0.001)

# 合约市价买入 0.001 BTC
result = test_futures_buy_market("BTCUSDT", 0.001)

# 合约市价卖出 0.001 BTC
result = test_futures_sell_market("BTCUSDT", 0.001)

# 查看当前挂单
from crypto_trading.test_script.test_order import (
    show_spot_open_orders,
    show_futures_open_orders
)

show_spot_open_orders("BTCUSDT")  # 查看现货 BTCUSDT 的挂单
show_futures_open_orders()  # 查看合约所有交易对的挂单

# 撤销订单
from crypto_trading.test_script.test_order import (
    cancel_spot_order,
    cancel_futures_order,
    cancel_all_spot_orders
)

# 通过订单ID撤销现货订单
cancel_spot_order("BTCUSDT", order_id=12345678)

# 通过客户端订单ID撤销合约订单
cancel_futures_order("BTCUSDT", orig_client_order_id="my_order_123")

# 撤销现货某个交易对的所有挂单
cancel_all_spot_orders("BTCUSDT")
```

### 环境变量

脚本支持通过环境变量配置 API 密钥：

```bash
export API_KEY="your_api_key"
export API_SECRET="your_api_secret"
export BASE_PATH="https://api.binance.com"  # 可选，默认使用生产环境
```

### 注意事项

⚠️ **重要警告**：

1. **实际下单风险**：此脚本会进行真实交易，请谨慎使用！
2. **测试环境**：建议先在测试网络或使用小额资金测试
3. **API 密钥安全**：不要将 API 密钥提交到版本控制系统
4. **默认参数**：脚本中的测试函数默认已注释，避免意外下单
5. **余额检查**：下单前请确保账户有足够的余额
6. **交易对验证**：确保交易对符号正确且可交易
7. **价格精度**：注意交易对的价格和数量精度要求

### 返回格式

函数返回字典，包含：

```python
{
    "success": True,  # 是否成功
    "rate_limits": {...},  # API 限流信息
    "order": {...}  # 订单详情
}
```

如果失败：

```python
{
    "success": False,
    "error": "错误信息",
    "traceback": "错误堆栈"
}
```


