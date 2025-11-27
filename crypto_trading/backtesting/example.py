"""
回测框架使用示例

展示如何使用回测框架进行因子测试和策略回测

使用方法：
    python -m crypto_trading.backtesting.example
    或者
    from crypto_trading.backtesting import BacktestFramework, FactorTester, StrategyBacktester
"""

import sys
import os

# 添加项目根目录到路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（crypto_trading 的父目录）
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import json

# 导入回测框架 - 支持多种运行方式
try:
    # 方式1: 作为包导入（python -m crypto_trading.backtesting.example）
    from crypto_trading.backtesting import BacktestFramework, FactorTester, StrategyBacktester
except ImportError:
    # 方式2: 直接运行脚本时，直接导入当前目录的模块
    # 由于 framework.py 使用相对导入，我们需要先导入依赖模块
    import importlib.util
    
    # 创建一个临时包结构来支持相对导入
    import types
    backtesting_pkg = types.ModuleType('crypto_trading.backtesting')
    sys.modules['crypto_trading'] = types.ModuleType('crypto_trading')
    sys.modules['crypto_trading'].backtesting = backtesting_pkg
    sys.modules['crypto_trading.backtesting'] = backtesting_pkg
    
    # 导入 factor_test.py
    factor_test_path = os.path.join(current_dir, 'factor_test.py')
    spec_factor = importlib.util.spec_from_file_location("crypto_trading.backtesting.factor_test", factor_test_path)
    factor_test_module = importlib.util.module_from_spec(spec_factor)
    sys.modules['crypto_trading.backtesting.factor_test'] = factor_test_module
    spec_factor.loader.exec_module(factor_test_module)
    FactorTester = factor_test_module.FactorTester
    
    # 导入 strategy_backtest.py
    strategy_backtest_path = os.path.join(current_dir, 'strategy_backtest.py')
    spec_strategy = importlib.util.spec_from_file_location("crypto_trading.backtesting.strategy_backtest", strategy_backtest_path)
    strategy_backtest_module = importlib.util.module_from_spec(spec_strategy)
    sys.modules['crypto_trading.backtesting.strategy_backtest'] = strategy_backtest_module
    spec_strategy.loader.exec_module(strategy_backtest_module)
    StrategyBacktester = strategy_backtest_module.StrategyBacktester
    
    # 现在可以导入 framework.py 了（它的相对导入现在可以工作）
    framework_path = os.path.join(current_dir, 'framework.py')
    spec_framework = importlib.util.spec_from_file_location("crypto_trading.backtesting.framework", framework_path)
    framework_module = importlib.util.module_from_spec(spec_framework)
    sys.modules['crypto_trading.backtesting.framework'] = framework_module
    spec_framework.loader.exec_module(framework_module)
    BacktestFramework = framework_module.BacktestFramework


def example_factor_1(data: pd.DataFrame, index: int) -> float:
    """
    示例因子1: 简单移动平均线因子
    
    如果当前价格高于过去5期的平均价格，返回1（看多）
    否则返回-1（看空）
    """
    n=2
    if index < n:
        return 0
    
    current_price = data.iloc[index]['close_price']
    ma5 = data.iloc[index-n:index]['close_price'].mean()
    
    if current_price > ma5:
        return 1.0  # 看多
    else:
        return -1.0  # 看空


def example_signal_1(data: pd.DataFrame, index: int) -> str:
    """
    示例策略1: 基于移动平均线的简单策略
    
    当价格上穿MA5时买入，下穿MA5时卖出
    """
    n=3
    if index < n:
        return 'hold'
    
    current_price = data.iloc[index]['close_price']
    ma5 = data.iloc[index-n:index]['close_price'].mean()
    prev_price = data.iloc[index-1]['close_price']
    prev_ma5 = data.iloc[index-n-1:index-1]['close_price'].mean()
    
    # 上穿：之前价格在MA5下方，现在在MA5上方
    if prev_price <= prev_ma5 and current_price > ma5:
        return 'buy'
    # 下穿：之前价格在MA5上方，现在在MA5下方
    elif prev_price >= prev_ma5 and current_price < ma5:
        return 'sell'
    else:
        return 'hold'


def main():
    """
    主函数：演示回测框架的使用
    """
    # 示例1: 使用BacktestFramework进行因子测试
    print("=" * 60)
    print("示例1: 因子胜率测试")
    print("=" * 60)
    
    # 加载数据
    data_path = '/Users/user/Desktop/repo/crypto_trading/tmp/data/BTCUSDT_futures/BTCUSDT_1d_1095_20251126_200623.json'
    
    framework = BacktestFramework(data_path=data_path)
    
    # 测试因子
    factor_results = framework.test_factor(
        factor_func=example_factor_1,
        forward_periods=2,  # 未来7个周期
        min_periods=2,
        factor_name="MA5因子"
    )
    
    # 打印结果
    framework.print_factor_results(factor_results)
    
    # 示例2: 使用BacktestFramework进行策略回测
    print("\n" + "=" * 60)
    print("示例2: 策略回测")
    print("=" * 60)
    
    # 回测策略（带止盈止损）
    backtest_results = framework.backtest_strategy(
        signal_func=example_signal_1,
        min_periods=10,
        position_size=0.2,  # 每次使用20%的资金
        initial_capital=10000.0,
        commission_rate=0.00001,  # 0.001%手续费
        take_profit=0.08,  # 止盈10%
        stop_loss=0.3  # 止损10%
    )
    
    # 打印结果
    framework.print_backtest_results(backtest_results)
    
    # 绘制结果
    framework.plot_backtest_results(backtest_results)
    
    # # 示例3: 直接使用FactorTester
    # print("\n" + "=" * 60)
    # print("示例3: 直接使用FactorTester")
    # print("=" * 60)
    
    # with open(data_path, 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    
    # data = pd.DataFrame(json_data['data'])
    # factor_tester = FactorTester(data)
    
    # results = factor_tester.test_factor(
    #     factor_func=example_factor_1,
    #     forward_periods=2,
    #     min_periods=2,
    #     factor_name="直接测试MA5因子"
    # )
    
    # factor_tester.print_results(results)
    
    # # 示例4: 直接使用StrategyBacktester
    # print("\n" + "=" * 60)
    # print("示例4: 直接使用StrategyBacktester")
    # print("=" * 60)
    
    # strategy_backtester = StrategyBacktester(
    #     data=data,
    #     initial_capital=10000.0,
    #     commission_rate=0.00001
    # )
    
    # results = strategy_backtester.backtest(
    #     signal_func=example_signal_1,
    #     min_periods=5,
    #     position_size=0.2,
    #     take_profit=0.1,  # 止盈10%
    #     stop_loss=0.1  # 止损10%
    # )
    
    # strategy_backtester.print_results(results)
    # strategy_backtester.plot_results(results)


if __name__ == "__main__":
    main()

