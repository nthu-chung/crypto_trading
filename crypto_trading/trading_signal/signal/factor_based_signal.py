"""
基于因子的交易信号策略

展示如何在信号策略中使用factor中的因子
"""

from typing import Callable, Optional
import pandas as pd

# 导入因子
from ..factor.ma_factor import ma_factor, ma_cross_factor
from ..factor.rsi_factor import rsi_factor


def factor_based_signal(
    data: 'pd.DataFrame', 
    index: int, 
    position: float, 
    entry_price: float, 
    entry_index: int,
    take_profit: float,
    stop_loss: float,
    check_periods: int,
    factor_func: Optional[Callable] = None,
    factor_period: int = 3
) -> str:
    """
    基于因子的交易信号策略，带止盈止损
    
    使用指定的因子函数生成交易信号
    当因子值从负转正时买入，从正转负时卖出
    
    Args:
        data: 完整的DataFrame
        index: 当前数据点的索引
        position: 当前持仓数量（如果没有持仓则为0）
        entry_price: 入场价格（如果没有持仓则为0）
        entry_index: 入场索引（如果没有持仓则为-1）
        take_profit: 止盈比例（例如：0.1 表示 10%）
        stop_loss: 止损比例（例如：0.1 表示 10%）
        check_periods: 检查未来多少个周期
        factor_func: 因子函数（如果为None，默认使用ma_factor）
        factor_period: 因子计算周期（用于某些因子）
    
    Returns:
        'buy', 'sell' 或 'hold'
    """
    # 默认使用ma_factor
    if factor_func is None:
        factor_func = lambda d, i: ma_factor(d, i, period=factor_period)
    
    # 计算当前因子值
    try:
        current_factor = factor_func(data, index)
    except Exception:
        return 'hold'
    
    # 如果数据不足，返回hold
    if current_factor == 0 and index > 0:
        return 'hold'
    
    # 计算上一周期的因子值
    prev_factor = 0.0
    if index > 0:
        try:
            prev_factor = factor_func(data, index - 1)
        except Exception:
            prev_factor = 0.0
    
    # 如果有持仓，先检查止盈止损
    if position > 0 and entry_price > 0:
        # 计算止盈和止损价格
        take_profit_price = entry_price * (1 + take_profit) if take_profit is not None else None
        stop_loss_price = entry_price * (1 - stop_loss) if stop_loss is not None else None
        
        # 检查当前周期和未来 check_periods 个周期
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
        # 因子从正转负：卖出
        if prev_factor > 0 and current_factor < 0:
            return 'sell'
        else:
            return 'hold'
    
    # 如果没有持仓，检查买入信号
    else:
        # 因子从负转正：买入
        if prev_factor < 0 and current_factor > 0:
            return 'buy'
        else:
            return 'hold'


def multi_factor_signal(
    data: 'pd.DataFrame', 
    index: int, 
    position: float, 
    entry_price: float, 
    entry_index: int,
    take_profit: float,
    stop_loss: float,
    check_periods: int,
    factor_funcs: list = None,
    weights: list = None
) -> str:
    """
    多因子组合交易信号策略，带止盈止损
    
    组合多个因子，加权求和后生成交易信号
    
    Args:
        data: 完整的DataFrame
        index: 当前数据点的索引
        position: 当前持仓数量（如果没有持仓则为0）
        entry_price: 入场价格（如果没有持仓则为0）
        entry_index: 入场索引（如果没有持仓则为-1）
        take_profit: 止盈比例（例如：0.1 表示 10%）
        stop_loss: 止损比例（例如：0.1 表示 10%）
        check_periods: 检查未来多少个周期
        factor_funcs: 因子函数列表（如果为None，默认使用[ma_factor, rsi_factor]）
        weights: 因子权重列表（如果为None，默认等权重）
    
    Returns:
        'buy', 'sell' 或 'hold'
    """
    # 默认使用ma_factor和rsi_factor
    if factor_funcs is None:
        factor_funcs = [
            lambda d, i: ma_factor(d, i, period=5),
            lambda d, i: rsi_factor(d, i, period=14)
        ]
    
    # 默认等权重
    if weights is None:
        weights = [1.0 / len(factor_funcs)] * len(factor_funcs)
    
    # 确保权重和因子数量一致
    if len(weights) != len(factor_funcs):
        weights = [1.0 / len(factor_funcs)] * len(factor_funcs)
    
    # 计算加权因子值
    try:
        combined_factor = 0.0
        for factor_func, weight in zip(factor_funcs, weights):
            factor_value = factor_func(data, index)
            if factor_value is not None and not (isinstance(factor_value, float) and factor_value == 0 and index == 0):
                combined_factor += factor_value * weight
    except Exception:
        return 'hold'
    
    # 计算上一周期的组合因子值
    prev_combined_factor = 0.0
    if index > 0:
        try:
            for factor_func, weight in zip(factor_funcs, weights):
                factor_value = factor_func(data, index - 1)
                if factor_value is not None:
                    prev_combined_factor += factor_value * weight
        except Exception:
            prev_combined_factor = 0.0
    
    # 如果有持仓，先检查止盈止损
    if position > 0 and entry_price > 0:
        # 计算止盈和止损价格
        take_profit_price = entry_price * (1 + take_profit) if take_profit is not None else None
        stop_loss_price = entry_price * (1 - stop_loss) if stop_loss is not None else None
        
        # 检查当前周期和未来 check_periods 个周期
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
        # 组合因子从正转负：卖出
        if prev_combined_factor > 0 and combined_factor < 0:
            return 'sell'
        else:
            return 'hold'
    
    # 如果没有持仓，检查买入信号
    else:
        # 组合因子从负转正：买入
        if prev_combined_factor < 0 and combined_factor > 0:
            return 'buy'
        else:
            return 'hold'

