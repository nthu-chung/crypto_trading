"""
移动平均线因子

包含基于移动平均线的各种因子
"""

import pandas as pd
import numpy as np


def ma_factor(data: 'pd.DataFrame', index: int, period: int = 5) -> float:
    """
    简单移动平均线因子
    
    如果当前价格高于过去period期的平均价格，返回1（看多）
    否则返回-1（看空）
    
    Args:
        data: 完整的DataFrame
        index: 当前数据点的索引
        period: 移动平均周期（默认5）
    
    Returns:
        因子值：1.0（看多）、-1.0（看空）或 0（数据不足）
    """
    if index < period:
        return 0.0
    
    current_price = data.iloc[index]['close_price']
    ma = data.iloc[index-period:index]['close_price'].mean()
    
    if current_price > ma:
        return 1.0  # 看多
    else:
        return -1.0  # 看空


def ma_cross_factor(data: 'pd.DataFrame', index: int, short_period: int = 5, long_period: int = 20) -> float:
    """
    移动平均线交叉因子
    
    当短期均线上穿长期均线时看多，下穿时看空
    
    Args:
        data: 完整的DataFrame
        index: 当前数据点的索引
        short_period: 短期均线周期（默认5）
        long_period: 长期均线周期（默认20）
    
    Returns:
        因子值：1.0（看多）、-1.0（看空）或 0（数据不足）
    """
    if index < long_period:
        return 0.0
    
    # 计算当前周期的均线
    short_ma_current = data.iloc[index-short_period:index]['close_price'].mean()
    long_ma_current = data.iloc[index-long_period:index]['close_price'].mean()
    
    # 计算上一周期的均线
    short_ma_prev = data.iloc[index-short_period-1:index-1]['close_price'].mean()
    long_ma_prev = data.iloc[index-long_period-1:index-1]['close_price'].mean()
    
    # 上穿：之前短期均线在长期均线下方，现在在上方
    if short_ma_prev <= long_ma_prev and short_ma_current > long_ma_current:
        return 1.0  # 看多
    # 下穿：之前短期均线在长期均线上方，现在在下方
    elif short_ma_prev >= long_ma_prev and short_ma_current < long_ma_current:
        return -1.0  # 看空
    else:
        return 0.0  # 中性

