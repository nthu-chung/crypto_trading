"""
因子和信号使用示例

展示如何使用factor中的因子和signal中的信号策略

使用方法：
    # 方式1: 作为模块运行（推荐）
    python -m cyqnt_trd.trading_signal.example_usage
    
    # 方式2: 直接运行脚本
    python example_usage.py
"""

import sys
import os

# 尝试直接导入（当作为 package 安装时）
try:
    from cyqnt_trd.backtesting import BacktestFramework
    from cyqnt_trd.trading_signal.factor import ma_factor, ma_cross_factor, rsi_factor
    from cyqnt_trd.trading_signal.signal import (
        ma_signal, 
        ma_cross_signal, 
        factor_based_signal,
        multi_factor_signal
    )
    from cyqnt_trd.trading_signal.selected_alpha import alpha1_factor
except ImportError:
    # 如果直接导入失败，尝试添加项目根目录到路径（用于开发模式）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目根目录（cyqnt_trd 的父目录）
    # example_usage.py 位于: cyqnt_trd/cyqnt_trd/trading_signal/example_usage.py
    # 需要向上2级到达: cyqnt_trd/
    project_root = os.path.dirname(os.path.dirname(current_dir))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # 再次尝试导入
    try:
        from cyqnt_trd.backtesting import BacktestFramework
        from cyqnt_trd.trading_signal.factor import ma_factor, ma_cross_factor, rsi_factor
        from cyqnt_trd.trading_signal.signal import (
            ma_signal, 
            ma_cross_signal, 
            factor_based_signal,
            multi_factor_signal
        )
        from cyqnt_trd.trading_signal.selected_alpha import alpha1_factor
    except ImportError as e:
        print(f"导入错误: {e}")
        print("\n提示：请使用以下方式之一：")
        print("  1. 安装 package: pip install -e .")
        print("  2. 作为模块运行: python -m cyqnt_trd.trading_signal.example_usage")
        print("  3. 在项目根目录下运行: cd /path/to/cyqnt_trd && python -m cyqnt_trd.trading_signal.example_usage")
        sys.exit(1)


def example_1_use_factor(data_path):
    """
    示例1: 使用factor中的因子进行因子测试
    """
    print("=" * 60)
    print("示例1: 使用factor中的因子进行因子测试")
    print("=" * 60)
    
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
    
    save_dir = '/Users/user/Desktop/repo/cyqnt_trd/result'
    framework.print_factor_results(
        factor_results,
        save_dir=save_dir
    )


def example_2_use_signal(data_path):
    """
    示例2: 使用signal中的信号策略进行回测
    """
    print("\n" + "=" * 60)
    print("示例2: 使用signal中的信号策略进行回测")
    print("=" * 60)

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
    
    save_dir = '/Users/user/Desktop/repo/cyqnt_trd/result'
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir
    )


def example_3_factor_in_signal(data_path):
    """
    示例3: 在signal中使用factor中的因子
    """
    print("\n" + "=" * 60)
    print("示例3: 在signal中使用factor中的因子")
    print("=" * 60)

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
        min_periods=35,  # 至少需要35个周期，确保factor_based_signal有足够的数据（30+2+缓冲）
        position_size=0.2,
        initial_capital=10000.0,
        commission_rate=0.00001,
        take_profit=0.1,
        stop_loss=0.5,
        check_periods=1,  # 只能为1，因为实际使用时无法看到未来数据
        strategy_name="基于MA因子的策略"
    )
    
    framework.print_backtest_results(backtest_results)
    
    save_dir = '/Users/user/Desktop/repo/cyqnt_trd/result'
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir
    )


def example_4_multi_factor(data_path):
    """
    示例4: 使用多因子组合策略
    """
    print("\n" + "=" * 60)
    print("示例4: 使用多因子组合策略")
    print("=" * 60)
    
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
        check_periods=1,  # 只能为1，因为实际使用时无法看到未来数据
        strategy_name="多因子组合策略（MA+RSI）"
    )
    
    framework.print_backtest_results(backtest_results)
    
    save_dir = '/Users/user/Desktop/repo/cyqnt_trd/result'
    framework.plot_backtest_results(
        backtest_results, 
        save_dir=save_dir
    )


def example_5_alpha1_factor(data_path):
    """
    示例5: 使用Alpha#1因子进行因子测试
    """
    print("\n" + "=" * 60)
    print("示例5: 使用Alpha#1因子进行因子测试")
    print("=" * 60)
    print("\n因子说明：")
    print("  - 公式: rank(Ts_ArgMax(SignedPower(((returns<0)?stddev(returns,20):close),2.),5))-0.5)")
    print("  - 策略逻辑：对过去5天按照收盘价最高或下行波动率最高进行排名")
    print("  - 下行波动率最高的一天离计算时间越近，越可以投资")
    print("  - 收盘价最高离计算时间越近，越可以投资")
    print("  - 标签：mean-reversion+momentum")
    print()
    
    framework = BacktestFramework(data_path=data_path)
    
    # 使用Alpha#1因子进行测试
    def alpha1_wrapper(data_slice):
        """
        Alpha#1 因子包装函数
        
        使用默认参数：lookback_days=5, stddev_period=20, power=2.0
        """
        return alpha1_factor(
            data_slice,
            lookback_days=5,
            stddev_period=20,
            power=2.0
        )
    
    # 测试因子
    print("开始测试 Alpha#1 因子...")
    print(f"  回看天数: 5")
    print(f"  标准差周期: 20")
    print(f"  幂次: 2.0")
    print(f"  向前看周期: 7")
    print()
    
    factor_results = framework.test_factor(
        factor_func=alpha1_wrapper,
        forward_periods=7,  # 未来7个周期
        min_periods=30,  # 至少需要30个周期（5+20+一些缓冲）
        factor_name="Alpha#1因子"
    )
    
    # 打印结果并保存
    save_dir = '/Users/user/Desktop/repo/cyqnt_trd/result'
    framework.print_factor_results(
        factor_results,
        save_dir=save_dir
    )


def example_6_alpha1_signal(data_path):
    """
    示例6: 使用基于Alpha#1因子的信号策略进行回测
    """
    print("\n" + "=" * 60)
    print("示例6: 使用基于Alpha#1因子的信号策略进行回测")
    print("=" * 60)

    framework = BacktestFramework(data_path=data_path)
    
    # 创建使用 Alpha#1 因子的信号策略
    def alpha1_signal_wrapper(data_slice, position, entry_price, entry_index, take_profit, stop_loss, check_periods):
        """
        使用 Alpha#1 因子的信号策略
        """
        # 使用 Alpha#1 因子
        factor_func = lambda d: alpha1_factor(d, lookback_days=5, stddev_period=20, power=2.0)
        return factor_based_signal(
            data_slice, position, entry_price, entry_index,
            take_profit, stop_loss, check_periods,
            factor_func=factor_func
        )
    
    # 回测策略
    print("开始回测基于 Alpha#1 因子的策略...")
    backtest_results = framework.backtest_strategy(
        signal_func=alpha1_signal_wrapper,
        min_periods=30,  # 至少需要30个周期
        position_size=0.2,  # 每次使用20%的资金
        initial_capital=10000.0,
        commission_rate=0.00001,  # 0.001%手续费
        take_profit=0.1,  # 止盈10%
        stop_loss=0.5,  # 止损50%
        check_periods=1,  # 只能为1，因为实际使用时无法看到未来数据
        strategy_name="基于Alpha#1因子的策略"
    )
    
    # 打印结果
    framework.print_backtest_results(backtest_results)
    
    # 绘制结果并保存
    save_dir = '/Users/user/Desktop/repo/cyqnt_trd/result'
    framework.plot_backtest_results(
        backtest_results,
        save_dir=save_dir
    )


def main():
    """
    主函数：运行所有示例
    """
    # 取消注释想要运行的示例
    data_path = "/Users/user/Desktop/repo/cyqnt_trd/tmp/data/BTCUSDT_current/BTCUSDT_3m_32160_20251002_000000_20251208_000000_20251211_111242.json"
    # example_1_use_factor()
    example_2_use_signal(data_path)
    # example_4_multi_factor()
    example_3_factor_in_signal(data_path)
    # example_5_alpha1_factor()  # Alpha#1因子测试
    example_6_alpha1_signal(data_path)  # 基于Alpha#1因子的策略回测
    
    
    # print("\n提示：")
    # print("  - 取消注释example_usage.py中的示例函数来运行测试")
    # print("  - 推荐使用模块方式运行: python3 -m cyqnt_trd.trading_signal.example_usage")


if __name__ == "__main__":
    main()

