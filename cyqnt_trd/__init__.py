"""
Cyqnt Trading Package

一个用于加密货币交易的工具包，包含数据获取、交易信号生成和回测功能。

主要模块:
- get_data: 数据获取模块，支持从 Binance 获取期货和现货数据
- trading_signal: 交易信号模块，包含因子计算和信号策略
- backtesting: 回测框架，支持因子测试和策略回测
"""

__version__ = "0.1.9.dev"

_OPTIONAL_IMPORT_ERRORS = {}


def _safe_import(module_name: str):
    try:
        module = __import__(f"{__name__}.{module_name}", fromlist=[module_name])
        globals()[module_name] = module
    except Exception as exc:  # pragma: no cover - import environment dependent
        globals()[module_name] = None
        _OPTIONAL_IMPORT_ERRORS[module_name] = exc


# 导入主要模块
for _module_name in ("get_data", "trading_signal", "backtesting", "standard_bot"):
    _safe_import(_module_name)

__all__ = [
    'get_data',
    'trading_signal',
    'backtesting',
    'standard_bot',
    'utils',
    '__version__',
    '_OPTIONAL_IMPORT_ERRORS',
]
