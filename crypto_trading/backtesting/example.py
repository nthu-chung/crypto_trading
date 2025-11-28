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


def example_signal_1(
    data: pd.DataFrame, 
    index: int, 
    position: float, 
    entry_price: float, 
    entry_index: int,
    take_profit: float,
    stop_loss: float,
    check_periods: int
) -> str:
    """
    示例策略: 基于移动平均线的策略，带止盈止损
    
    当价格上穿MA5时买入，下穿MA5时卖出
    同时检查止盈止损条件
    
    Args:
        data: 完整的DataFrame
        index: 当前数据点的索引
        position: 当前持仓数量（如果没有持仓则为0）
        entry_price: 入场价格（如果没有持仓则为0）
        entry_index: 入场索引（如果没有持仓则为-1）
        take_profit: 止盈比例（例如：0.1 表示 10%）
        stop_loss: 止损比例（例如：0.1 表示 10%）
        check_periods: 检查未来多少个周期
    
    Returns:
        'buy', 'sell' 或 'hold'
    """
    n = 2
    if index < n:
        return 'hold'
    
    current_price = data.iloc[index]['close_price']
    ma5 = data.iloc[index-n:index]['close_price'].mean()
    prev_price = data.iloc[index-1]['close_price']
    prev_ma5 = data.iloc[index-n-1:index-1]['close_price'].mean()
    
    # 如果有持仓，先检查止盈止损
    if position > 0 and entry_price > 0:
        # 计算止盈和止损价格
        take_profit_price = entry_price * (1 + take_profit) if take_profit is not None else None
        stop_loss_price = entry_price * (1 - stop_loss) if stop_loss is not None else None
        
        # 检查当前周期和未来 check_periods 个周期
        # 优先查找止损（因为止损优先），如果找到止损就立即返回卖出
        for check_idx in range(index, min(index + check_periods, len(data))):
            check_low = data.iloc[check_idx]['low_price']
            check_high = data.iloc[check_idx]['high_price']
            
            # 优先检查止损
            if stop_loss_price is not None and check_low <= stop_loss_price:
                return 'sell'  # 触发止损
            
            # 检查止盈
            if take_profit_price is not None and check_high >= take_profit_price:
                return 'sell'  # 触发止盈
        
        # 如果没有触发止盈止损，检查策略信号
        # 下穿：之前价格在MA5上方，现在在MA5下方
        if prev_price >= prev_ma5 and current_price < ma5:
            return 'sell'
        else:
            return 'hold'
    
    # 如果没有持仓，检查买入信号
    else:
        # 上穿：之前价格在MA5下方，现在在MA5上方
        if prev_price <= prev_ma5 and current_price > ma5:
            return 'buy'
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
    data_path = '/Users/user/Desktop/repo/crypto_trading/tmp/data/BTCUSDT_futures/BTCUSDT_1d_1095_20251127_113603.json'
    
    framework = BacktestFramework(data_path=data_path)
    
    # 测试因子
    factor_results = framework.test_factor(
        factor_func=example_factor_1,
        forward_periods=7,  # 未来7个周期
        min_periods=10,
        factor_name="MA5因子"
    )
    
    # 打印结果并自动保存（数据名称会自动从数据路径中提取）
    save_dir = '/Users/user/Desktop/repo/crypto_trading/result'  # 保存目录
    framework.print_factor_results(
        factor_results,
        save_dir=save_dir  # 如果提供了save_dir，会自动保存JSON
    )
    
    # 示例2: 使用BacktestFramework进行策略回测（止盈止损由策略函数决定）
    print("\n" + "=" * 60)
    print("示例2: 策略回测（止盈止损由策略函数决定）")
    print("=" * 60)
    
    # 回测策略（止盈止损参数会传递给策略函数，由策略函数决定是否使用）
    backtest_results = framework.backtest_strategy(
        signal_func=example_signal_1,  # 使用带止盈止损的策略函数
        min_periods=10,
        position_size=0.2,  # 每次使用20%的资金
        initial_capital=10000.0,
        commission_rate=0.00001,  # 0.001%手续费
        take_profit=0.1,  # 止盈8%（传递给策略函数）
        stop_loss=0.5,  # 止损30%（传递给策略函数）
        check_periods=7,  # 检查未来1个周期（传递给策略函数）
        strategy_name="MA5策略"  # 策略名称（用于文件命名）
    )
    
    # 打印结果
    framework.print_backtest_results(backtest_results)
    
    # 绘制结果并自动保存（根据策略名称和数据名称自动生成文件名）
    # 数据名称会自动从数据路径中提取（如 ETHUSDT）
    save_dir = '/Users/user/Desktop/repo/crypto_trading/result'  # 保存目录
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir  # 如果提供了save_dir，会自动保存图片和JSON
    )
    
    # # 示例4: 直接使用FactorTester
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

