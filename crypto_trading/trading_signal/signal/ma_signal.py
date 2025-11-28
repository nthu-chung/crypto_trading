"""
基于移动平均线的交易信号策略

包含基于移动平均线的各种交易策略
"""

import pandas as pd


def ma_signal(
    data: 'pd.DataFrame', 
    index: int, 
    position: float, 
    entry_price: float, 
    entry_index: int,
    take_profit: float,
    stop_loss: float,
    check_periods: int,
    period: int = 5
) -> str:
    """
    基于移动平均线的交易信号策略，带止盈止损
    
    当价格上穿MA时买入，下穿MA时卖出
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
        period: 移动平均周期（默认5）
    
    Returns:
        'buy', 'sell' 或 'hold'
    """
    if index < period:
        return 'hold'
    
    current_price = data.iloc[index]['close_price']
    ma = data.iloc[index-period:index]['close_price'].mean()
    prev_price = data.iloc[index-1]['close_price']
    prev_ma = data.iloc[index-period-1:index-1]['close_price'].mean()
    
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
        # 下穿：之前价格在MA上方，现在在MA下方
        if prev_price >= prev_ma and current_price < ma:
            return 'sell'
        else:
            return 'hold'
    
    # 如果没有持仓，检查买入信号
    else:
        # 上穿：之前价格在MA下方，现在在MA上方
        if prev_price <= prev_ma and current_price > ma:
            return 'buy'
        else:
            return 'hold'


def ma_cross_signal(
    data: 'pd.DataFrame', 
    index: int, 
    position: float, 
    entry_price: float, 
    entry_index: int,
    take_profit: float,
    stop_loss: float,
    check_periods: int,
    short_period: int = 5,
    long_period: int = 20
) -> str:
    """
    基于移动平均线交叉的交易信号策略，带止盈止损
    
    当短期均线上穿长期均线时买入，下穿时卖出
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
        short_period: 短期均线周期（默认5）
        long_period: 长期均线周期（默认20）
    
    Returns:
        'buy', 'sell' 或 'hold'
    """
    if index < long_period:
        return 'hold'
    
    # 计算当前周期的均线
    short_ma_current = data.iloc[index-short_period:index]['close_price'].mean()
    long_ma_current = data.iloc[index-long_period:index]['close_price'].mean()
    
    # 计算上一周期的均线
    short_ma_prev = data.iloc[index-short_period-1:index-1]['close_price'].mean()
    long_ma_prev = data.iloc[index-long_period-1:index-1]['close_price'].mean()
    
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
        # 下穿：之前短期均线在长期均线上方，现在在下方
        if short_ma_prev >= long_ma_prev and short_ma_current < long_ma_current:
            return 'sell'
        else:
            return 'hold'
    
    # 如果没有持仓，检查买入信号
    else:
        # 上穿：之前短期均线在长期均线下方，现在在上方
        if short_ma_prev <= long_ma_prev and short_ma_current > long_ma_current:
            return 'buy'
        else:
            return 'hold'

