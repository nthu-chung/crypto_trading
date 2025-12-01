"""
因子和信号使用示例

展示如何使用factor中的因子和signal中的信号策略

使用方法：
    # 方式1: 作为模块运行（推荐）
    python -m crypto_trading.trading_signal.example_usage
    
    # 方式2: 直接运行脚本
    python example_usage.py
"""

import sys
import os

# 添加项目根目录到路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（crypto_trading 的父目录）
# example_usage.py 位于: crypto_trading/crypto_trading/trading_signal/example_usage.py
# 需要向上2级到达: crypto_trading/
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入回测框架和因子、信号模块
try:
    from crypto_trading.backtesting import BacktestFramework
    from crypto_trading.trading_signal.factor import ma_factor, ma_cross_factor, rsi_factor
    from crypto_trading.trading_signal.signal import (
        ma_signal, 
        ma_cross_signal, 
        factor_based_signal,
        multi_factor_signal
    )
except ImportError as e:
    print(f"导入错误: {e}")
    print("\n提示：请使用以下方式运行：")
    print("  python -m crypto_trading.trading_signal.example_usage")
    print("\n或者确保在项目根目录下运行：")
    print("  cd /Users/user/Desktop/repo/crypto_trading")
    print("  python -m crypto_trading.trading_signal.example_usage")
    sys.exit(1)


def example_1_use_factor():
    """
    示例1: 使用factor中的因子进行因子测试
    """
    print("=" * 60)
    print("示例1: 使用factor中的因子进行因子测试")
    print("=" * 60)
    
    # 加载数据
    data_path = '/Users/user/Desktop/repo/crypto_trading/tmp/data/BTCUSDT_futures/BTCUSDT_3m_158879_20250101_000000_20251127_235959_20251128_145101.json'
    
    framework = BacktestFramework(data_path=data_path)
    
    # 使用factor中的ma_factor进行测试
    # 注意：ma_factor现在接收数据切片，不需要包装函数
    def ma_factor_wrapper(data_slice):
        return ma_factor(data_slice, period=3)
    
    factor_results = framework.test_factor(
        factor_func=ma_factor_wrapper,
        forward_periods=5,
        min_periods=10,
        factor_name="MA5因子（来自factor模块）"
    )
    
    save_dir = '/Users/user/Desktop/repo/crypto_trading/result'
    framework.print_factor_results(
        factor_results,
        save_dir=save_dir
    )


def example_2_use_signal():
    """
    示例2: 使用signal中的信号策略进行回测
    """
    print("\n" + "=" * 60)
    print("示例2: 使用signal中的信号策略进行回测")
    print("=" * 60)
    
    # 加载数据
    data_path = '/Users/user/Desktop/repo/crypto_trading/tmp/data/BTCUSDT_futures/BTCUSDT_3m_158879_20250101_000000_20251127_235959_20251128_145101.json'
    
    framework = BacktestFramework(data_path=data_path)
    
    # 使用signal中的ma_signal进行回测
    # 注意：需要创建一个包装函数，因为ma_signal需要period参数
    # 使用闭包来捕获period值
    period = 3
    def ma_signal_wrapper(data_slice, position, entry_price, entry_index, take_profit, stop_loss, check_periods):
        return ma_signal(
            data_slice, position, entry_price, entry_index, 
            take_profit, stop_loss, period=period
        )
    
    backtest_results = framework.backtest_strategy(
        signal_func=ma_signal_wrapper,
        min_periods=10,
        position_size=0.2,
        initial_capital=10000.0,
        commission_rate=0.00001,
        take_profit=0.03,
        stop_loss=0.1,
        strategy_name="MA3策略（来自signal模块）"
    )
    
    framework.print_backtest_results(backtest_results)
    
    save_dir = '/Users/user/Desktop/repo/crypto_trading/result'
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir
    )


def example_3_factor_in_signal():
    """
    示例3: 在signal中使用factor中的因子
    """
    print("\n" + "=" * 60)
    print("示例3: 在signal中使用factor中的因子")
    print("=" * 60)
    
    # 加载数据
    data_path = '/Users/user/Desktop/repo/crypto_trading/tmp/data/TRUMPUSDT_futures/TRUMPUSDT_1d_1095_20251127_174403.json'
    
    framework = BacktestFramework(data_path=data_path)
    
    # 使用factor_based_signal，它内部会使用factor中的因子
    # 创建一个包装函数，传入ma_factor作为因子函数
    def factor_signal_wrapper(data_slice, position, entry_price, entry_index, take_profit, stop_loss, check_periods):
        # 使用factor中的ma_factor
        factor_func = lambda d: ma_factor(d, period=5)
        return factor_based_signal(
            data_slice, position, entry_price, entry_index,
            take_profit, stop_loss, check_periods,
            factor_func=factor_func
        )
    
    backtest_results = framework.backtest_strategy(
        signal_func=factor_signal_wrapper,
        min_periods=10,
        position_size=0.2,
        initial_capital=10000.0,
        commission_rate=0.00001,
        take_profit=0.1,
        stop_loss=0.5,
        check_periods=7,
        strategy_name="基于MA因子的策略"
    )
    
    framework.print_backtest_results(backtest_results)
    
    save_dir = '/Users/user/Desktop/repo/crypto_trading/result'
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir
    )


def example_4_multi_factor():
    """
    示例4: 使用多因子组合策略
    """
    print("\n" + "=" * 60)
    print("示例4: 使用多因子组合策略")
    print("=" * 60)
    
    # 加载数据
    data_path = '/Users/user/Desktop/repo/crypto_trading/tmp/data/TRUMPUSDT_futures/TRUMPUSDT_1d_1095_20251127_174403.json'
    
    framework = BacktestFramework(data_path=data_path)
    
    # 使用multi_factor_signal，组合多个因子
    def multi_factor_signal_wrapper(data_slice, position, entry_price, entry_index, take_profit, stop_loss, check_periods):
        # 组合ma_factor和rsi_factor
        factor_funcs = [
            lambda d: ma_factor(d, period=5),
            lambda d: rsi_factor(d, period=14)
        ]
        weights = [0.6, 0.4]  # MA因子权重0.6，RSI因子权重0.4
        
        return multi_factor_signal(
            data_slice, position, entry_price, entry_index,
            take_profit, stop_loss, check_periods,
            factor_funcs=factor_funcs,
            weights=weights
        )
    
    backtest_results = framework.backtest_strategy(
        signal_func=multi_factor_signal_wrapper,
        min_periods=20,  # 需要更多周期因为RSI需要14个周期
        position_size=0.2,
        initial_capital=10000.0,
        commission_rate=0.00001,
        take_profit=0.1,
        stop_loss=0.5,
        check_periods=7,
        strategy_name="多因子组合策略（MA+RSI）"
    )
    
    framework.print_backtest_results(backtest_results)
    
    save_dir = '/Users/user/Desktop/repo/crypto_trading/result'
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir
    )


def main():
    """
    主函数：运行所有示例
    """
    # 取消注释想要运行的示例
    example_1_use_factor()
    example_2_use_signal()
    # example_3_factor_in_signal()
    # example_4_multi_factor()
    
    # print("\n提示：")
    # print("  - 取消注释example_usage.py中的示例函数来运行测试")
    # print("  - 推荐使用模块方式运行: python3 -m crypto_trading.trading_signal.example_usage")


if __name__ == "__main__":
    main()

