"""
策略回测模块

根据买卖信号进行回测，计算收益率和收益曲线
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Optional, Dict, List, Tuple
from datetime import datetime
import json


class StrategyBacktester:
    """
    策略回测器
    
    根据买卖信号进行回测，计算收益率和收益曲线
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        initial_capital: float = 10000.0,
        commission_rate: float = 0.001
    ):
        """
        初始化策略回测器
        
        Args:
            data: 包含K线数据的DataFrame，必须包含以下列：
                  - datetime 或 open_time_str: 时间
                  - close_price: 收盘价
            initial_capital: 初始资金
            commission_rate: 手续费率（默认0.1%）
        """
        self.data = data.copy()
        
        # 确保有datetime列
        if 'datetime' not in self.data.columns:
            if 'open_time_str' in self.data.columns:
                self.data['datetime'] = pd.to_datetime(self.data['open_time_str'])
            elif 'open_time' in self.data.columns:
                self.data['datetime'] = pd.to_datetime(self.data['open_time'], unit='ms')
            else:
                raise ValueError("数据必须包含 'datetime', 'open_time_str' 或 'open_time' 列")
        
        # 确保有close_price列
        if 'close_price' not in self.data.columns:
            raise ValueError("数据必须包含 'close_price' 列")
        
        # 确保有high_price和low_price列（用于止盈止损）
        if 'high_price' not in self.data.columns:
            raise ValueError("数据必须包含 'high_price' 列（用于止盈止损）")
        if 'low_price' not in self.data.columns:
            raise ValueError("数据必须包含 'low_price' 列（用于止盈止损）")
        
        # 按时间排序
        self.data = self.data.sort_values('datetime').reset_index(drop=True)
        
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
    
    def backtest(
        self,
        signal_func: Callable[[pd.DataFrame, int], str],
        min_periods: int = 0,
        position_size: float = 1.0,
        take_profit: Optional[float] = None,
        stop_loss: Optional[float] = None,
        check_periods: int = 1
    ) -> Dict:
        """
        执行回测
        
        Args:
            signal_func: 信号生成函数，接受 (data, index) 作为参数，返回信号
                        - data: 完整的DataFrame
                        - index: 当前数据点的索引
                        - 返回: 'buy'（买入）, 'sell'（卖出）, 'hold'（持有）或 None
            min_periods: 最小需要的周期数（用于计算信号时）
            position_size: 每次交易的仓位大小（相对于可用资金的比例，0-1之间）
            take_profit: 止盈比例（例如：0.1 表示 10%）
                        止盈检查未来周期内的 high_price，如果 high_price >= entry_price * (1 + take_profit) 则卖出
            stop_loss: 止损比例（例如：0.1 表示 10%）
                      止损检查未来周期内的 low_price，如果 low_price <= entry_price * (1 - stop_loss) 则卖出
                      如果某一天同时触发止盈和止损，则优先执行止损
            check_periods: 检查未来多少个周期（默认1，即只检查当前周期）
                          例如：check_periods=3 表示检查当前周期和未来2个周期
        
        Returns:
            包含回测结果的字典：
            - initial_capital: 初始资金
            - final_capital: 最终资金
            - total_return: 总收益率
            - total_trades: 总交易次数
            - win_trades: 盈利交易次数
            - loss_trades: 亏损交易次数
            - win_rate: 胜率
            - max_drawdown: 最大回撤
            - sharpe_ratio: 夏普比率
            - equity_curve: 资金曲线（DataFrame）
            - trades: 交易记录列表
        """
        # 初始化
        capital = self.initial_capital
        position = 0  # 持仓数量
        entry_price = 0  # 入场价格
        entry_index = -1  # 入场索引
        
        equity_curve = []
        trades = []
        
        # 遍历每个时间点
        for i in range(min_periods, len(self.data)):
            try:
                # 获取当前价格
                current_price = self.data.iloc[i]['close_price']
                current_time = self.data.iloc[i]['datetime']
                
                # 如果有持仓，先检查止盈止损
                stop_triggered = False
                if position > 0 and entry_price > 0:
                    # 计算止盈和止损价格
                    take_profit_price = entry_price * (1 + take_profit) if take_profit is not None else None
                    stop_loss_price = entry_price * (1 - stop_loss) if stop_loss is not None else None
                    
                    # 检查当前周期和未来 check_periods 个周期
                    # 优先查找止损（因为止损优先），如果找到止损就立即退出
                    # 如果没有找到止损，再查找止盈
                    trigger_reason = None
                    trigger_index = None
                    trigger_price = None
                    
                    # 先查找所有周期中的止损（优先）
                    for check_idx in range(i, min(i + check_periods, len(self.data))):
                        check_low = self.data.iloc[check_idx]['low_price']
                        check_high = self.data.iloc[check_idx]['high_price']

                        if stop_loss_price is not None and check_low <= stop_loss_price:
                            trigger_reason = 'stop_loss'
                            trigger_index = check_idx
                            trigger_price = stop_loss_price  # 使用止损价格卖出
                            break  # 找到止损就立即退出
                        
                        if take_profit_price is not None and check_high >= take_profit_price:
                            trigger_reason = 'take_profit'
                            trigger_index = check_idx
                            trigger_price = take_profit_price  # 使用止盈价格卖出
                            break  # 找到第一个止盈就退出



                    
                    # 如果触发了止盈或止损，执行卖出
                    if trigger_reason is not None:
                        # 使用触发价格卖出
                        trade_amount = position * trigger_price
                        commission = trade_amount * self.commission_rate
                        capital = capital + trade_amount - commission
                        
                        # 计算盈亏
                        pnl = (trigger_price - entry_price) / entry_price
                        pnl_amount = trade_amount - (position * entry_price) - commission
                        
                        # 记录交易：使用当前周期的日期（因为我们在当前周期执行卖出）
                        # 但价格使用触发价格
                        trades.append({
                            'type': 'sell',
                            'reason': trigger_reason,
                            'datetime': current_time,
                            'index': i,
                            'trigger_index': trigger_index,  # 记录实际触发的周期
                            'price': float(trigger_price),
                            'entry_price': float(entry_price),
                            'pnl': float(pnl),
                            'pnl_amount': float(pnl_amount),
                            'capital': float(capital)
                        })
                        
                        position = 0
                        entry_price = 0
                        entry_index = -1
                        stop_triggered = True
                
                # 如果没有触发止盈止损，才处理信号
                if not stop_triggered:
                    # 生成信号
                    signal = signal_func(self.data, i)
                    
                    # 处理信号
                    if signal == 'buy' and position == 0:
                        # 买入
                        trade_amount = capital * position_size
                        position = trade_amount / current_price
                        commission = trade_amount * self.commission_rate
                        capital = capital - trade_amount - commission
                        entry_price = current_price
                        entry_index = i
                        
                        trades.append({
                            'type': 'buy',
                            'datetime': current_time,
                            'index': i,
                            'price': float(current_price),
                            'position': float(position),
                            'capital': float(capital)
                        })
                    
                    elif signal == 'sell' and position > 0:
                        # 卖出（信号触发）
                        trade_amount = position * current_price
                        commission = trade_amount * self.commission_rate
                        capital = capital + trade_amount - commission
                        
                        # 计算盈亏
                        pnl = (current_price - entry_price) / entry_price
                        pnl_amount = trade_amount - (position * entry_price) - commission
                        
                        trades.append({
                            'type': 'sell',
                            'reason': 'signal',
                            'datetime': current_time,
                            'index': i,
                            'price': float(current_price),
                            'entry_price': float(entry_price),
                            'pnl': float(pnl),
                            'pnl_amount': float(pnl_amount),
                            'capital': float(capital)
                        })
                        
                        position = 0
                        entry_price = 0
                        entry_index = -1
                
                # 计算当前总资产（现金 + 持仓市值）
                current_equity = capital + (position * current_price if position > 0 else 0)
                equity_curve.append({
                    'datetime': current_time,
                    'index': i,
                    'equity': float(current_equity),
                    'capital': float(capital),
                    'position': float(position),
                    'price': float(current_price)
                })
                
            except Exception as e:
                # 如果信号生成出错，继续
                continue
        
        # 如果最后还有持仓，按最后价格平仓
        if position > 0:
            last_price = self.data.iloc[-1]['close_price']
            last_time = self.data.iloc[-1]['datetime']
            trade_amount = position * last_price
            commission = trade_amount * self.commission_rate
            capital = capital + trade_amount - commission
            
            pnl = (last_price - entry_price) / entry_price
            pnl_amount = trade_amount - (position * entry_price) - commission
            
            trades.append({
                'type': 'sell',
                'reason': 'close_position',
                'datetime': last_time,
                'index': len(self.data) - 1,
                'price': float(last_price),
                'entry_price': float(entry_price),
                'pnl': float(pnl),
                'pnl_amount': float(pnl_amount),
                'capital': float(capital)
            })
            
            # 更新最后一条资金曲线
            if equity_curve:
                equity_curve[-1]['equity'] = float(capital)
                equity_curve[-1]['capital'] = float(capital)
                equity_curve[-1]['position'] = 0.0
        
        # 构建资金曲线DataFrame
        equity_df = pd.DataFrame(equity_curve)
        
        # 计算统计指标
        final_capital = capital
        total_return = (final_capital - self.initial_capital) / self.initial_capital
        
        # 计算交易统计
        sell_trades = [t for t in trades if t['type'] == 'sell']
        total_trades = len(sell_trades)
        win_trades = len([t for t in sell_trades if t.get('pnl', 0) > 0])
        loss_trades = len([t for t in sell_trades if t.get('pnl', 0) < 0])
        win_rate = win_trades / total_trades if total_trades > 0 else 0.0
        
        # 计算最大回撤
        equity_values = equity_df['equity'].values
        peak = np.maximum.accumulate(equity_values)
        drawdown = (equity_values - peak) / peak
        max_drawdown = abs(np.min(drawdown)) if len(drawdown) > 0 else 0.0
        
        # 计算夏普比率（简化版，假设无风险利率为0）
        returns = equity_df['equity'].pct_change().dropna()
        if len(returns) > 0 and returns.std() > 0:
            sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # 年化
        else:
            sharpe_ratio = 0.0
        
        results = {
            'initial_capital': self.initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'total_trades': total_trades,
            'win_trades': win_trades,
            'loss_trades': loss_trades,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'equity_curve': equity_df,
            'trades': trades
        }
        
        return results
    
    def plot_results(self, results: Dict, figsize: Tuple[int, int] = (14, 10)):
        """
        绘制回测结果
        
        Args:
            results: backtest返回的结果字典
            figsize: 图形大小
        """
        equity_df = results['equity_curve']
        
        # Set default font (no need for Chinese fonts)
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, axes = plt.subplots(3, 1, figsize=figsize, gridspec_kw={'height_ratios': [2, 1, 1]})
        
        # 1. Equity Curve
        ax1 = axes[0]
        ax1.plot(equity_df['datetime'], equity_df['equity'], label='Equity Curve', linewidth=2, color='blue')
        ax1.axhline(y=results['initial_capital'], color='gray', linestyle='--', label='Initial Capital')
        ax1.set_title('Backtest Equity Curve', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Equity (USDT)', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Price Curve and Trading Signals
        ax2 = axes[1]
        ax2.plot(equity_df['datetime'], equity_df['price'], label='Price', linewidth=1.5, color='black', alpha=0.7)
        
        # Mark buy/sell points
        buy_trades = [t for t in results['trades'] if t['type'] == 'buy']
        sell_trades = [t for t in results['trades'] if t['type'] == 'sell']
        
        if buy_trades:
            buy_times = [t['datetime'] for t in buy_trades]
            buy_prices = [t['price'] for t in buy_trades]
            ax2.scatter(buy_times, buy_prices, color='green', marker='^', s=100, label='Buy', zorder=5)
        
        if sell_trades:
            sell_times = [t['datetime'] for t in sell_trades]
            sell_prices = [t['price'] for t in sell_trades]
            ax2.scatter(sell_times, sell_prices, color='red', marker='v', s=100, label='Sell', zorder=5)
        
        ax2.set_title('Price Curve and Trading Signals', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Price (USDT)', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Drawdown Curve
        ax3 = axes[2]
        equity_values = equity_df['equity'].values
        peak = np.maximum.accumulate(equity_values)
        drawdown = (equity_values - peak) / peak * 100
        ax3.fill_between(equity_df['datetime'], drawdown, 0, color='red', alpha=0.3, label='Drawdown')
        ax3.plot(equity_df['datetime'], drawdown, color='red', linewidth=1)
        ax3.set_title('Drawdown Curve', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Drawdown (%)', fontsize=12)
        ax3.set_xlabel('Time', fontsize=12)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # 打印统计信息
        self.print_results(results)
    
    def print_results(self, results: Dict):
        """
        打印回测结果
        
        Args:
            results: backtest返回的结果字典
        """
        print(f"\n{'='*60}")
        print("回测结果统计")
        print(f"{'='*60}")
        print(f"初始资金: {results['initial_capital']:.2f} USDT")
        print(f"最终资金: {results['final_capital']:.2f} USDT")
        print(f"总收益率: {results['total_return']:.2%}")
        print(f"\n交易统计:")
        print(f"  总交易次数: {results['total_trades']}")
        print(f"  盈利交易: {results['win_trades']}")
        print(f"  亏损交易: {results['loss_trades']}")
        print(f"  胜率: {results['win_rate']:.2%}")
        print(f"\n风险指标:")
        print(f"  最大回撤: {results['max_drawdown']:.2%}")
        print(f"  夏普比率: {results['sharpe_ratio']:.2f}")
        print(f"{'='*60}\n")
    
    def save_results(self, results: Dict, filepath: str):
        """
        保存回测结果到JSON文件
        
        Args:
            results: backtest返回的结果字典
            filepath: 保存路径
        """
        output = results.copy()
        
        # 转换DataFrame为字典
        output['equity_curve'] = output['equity_curve'].to_dict('records')
        
        # 转换datetime为字符串
        for record in output['equity_curve']:
            if isinstance(record['datetime'], (pd.Timestamp, datetime)):
                record['datetime'] = record['datetime'].isoformat()
        
        for trade in output['trades']:
            if isinstance(trade['datetime'], (pd.Timestamp, datetime)):
                trade['datetime'] = trade['datetime'].isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"结果已保存到: {filepath}")

