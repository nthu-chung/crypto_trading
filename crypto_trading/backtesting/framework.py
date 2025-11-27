"""
回测框架主模块

提供统一的回测框架接口
"""

import pandas as pd
import json
from typing import Callable, Optional, Dict
from .factor_test import FactorTester
from .strategy_backtest import StrategyBacktester


class BacktestFramework:
    """
    回测框架主类
    
    提供统一的接口来使用因子测试和策略回测功能
    """
    
    def __init__(self, data_path: Optional[str] = None, data: Optional[pd.DataFrame] = None):
        """
        初始化回测框架
        
        Args:
            data_path: JSON数据文件路径（可选）
            data: 直接提供DataFrame数据（可选）
        
        注意: data_path 和 data 必须提供其中一个
        """
        if data_path:
            # 从JSON文件加载数据
            with open(data_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            if isinstance(json_data, dict) and 'data' in json_data:
                self.data = pd.DataFrame(json_data['data'])
            else:
                self.data = pd.DataFrame(json_data)
        
        elif data is not None:
            self.data = data.copy()
        else:
            raise ValueError("必须提供 data_path 或 data 参数")
        
        # 初始化测试器
        self.factor_tester = FactorTester(self.data)
        self.strategy_backtester = StrategyBacktester(self.data)
    
    def test_factor(
        self,
        factor_func: Callable[[pd.DataFrame, int], float],
        forward_periods: int = 7,
        min_periods: int = 0,
        factor_name: str = "factor"
    ) -> Dict:
        """
        测试单因子胜率
        
        Args:
            factor_func: 因子计算函数
            forward_periods: 向前看的周期数
            min_periods: 最小需要的周期数
            factor_name: 因子名称
        
        Returns:
            测试结果字典
        """
        return self.factor_tester.test_factor(
            factor_func=factor_func,
            forward_periods=forward_periods,
            min_periods=min_periods,
            factor_name=factor_name
        )
    
    def backtest_strategy(
        self,
        signal_func: Callable[[pd.DataFrame, int], str],
        min_periods: int = 0,
        position_size: float = 1.0,
        initial_capital: float = 10000.0,
        commission_rate: float = 0.001,
        take_profit: Optional[float] = None,
        stop_loss: Optional[float] = None,
        check_periods: int = 1
    ) -> Dict:
        """
        回测策略
        
        Args:
            signal_func: 信号生成函数
            min_periods: 最小需要的周期数
            position_size: 每次交易的仓位大小
            initial_capital: 初始资金
            commission_rate: 手续费率
            take_profit: 止盈比例（例如：0.1 表示 10%）
                        止盈检查未来周期内的 high_price，如果 high_price >= entry_price * (1 + take_profit) 则卖出
            stop_loss: 止损比例（例如：0.1 表示 10%）
                      止损检查未来周期内的 low_price，如果 low_price <= entry_price * (1 - stop_loss) 则卖出
                      如果某一天同时触发止盈和止损，则优先执行止损
            check_periods: 检查未来多少个周期（默认1，即只检查当前周期）
                          例如：check_periods=3 表示检查当前周期和未来2个周期
        
        Returns:
            回测结果字典
        """
        # 更新初始资金和手续费率
        self.strategy_backtester.initial_capital = initial_capital
        self.strategy_backtester.commission_rate = commission_rate
        
        return self.strategy_backtester.backtest(
            signal_func=signal_func,
            min_periods=min_periods,
            position_size=position_size,
            take_profit=take_profit,
            stop_loss=stop_loss,
            check_periods=check_periods
        )
    
    def plot_backtest_results(self, results: Dict, figsize: tuple = (14, 10)):
        """
        绘制回测结果
        
        Args:
            results: backtest_strategy返回的结果字典
            figsize: 图形大小
        """
        self.strategy_backtester.plot_results(results, figsize=figsize)
    
    def print_factor_results(self, results: Dict):
        """
        打印因子测试结果
        
        Args:
            results: test_factor返回的结果字典
        """
        self.factor_tester.print_results(results)
    
    def print_backtest_results(self, results: Dict):
        """
        打印回测结果
        
        Args:
            results: backtest_strategy返回的结果字典
        """
        self.strategy_backtester.print_results(results)

