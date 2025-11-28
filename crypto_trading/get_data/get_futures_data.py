import os
import logging
import csv
import json
from datetime import datetime
from typing import Optional, Union

from binance_sdk_derivatives_trading_usds_futures.derivatives_trading_usds_futures import (
    DerivativesTradingUsdsFutures,
    ConfigurationRestAPI,
    DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL,
)
from binance_sdk_derivatives_trading_usds_futures.rest_api.models import (
    KlineCandlestickDataIntervalEnum,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def _convert_to_timestamp_ms(time_input: Union[datetime, str, int, None]) -> Optional[int]:
    """
    将各种时间格式转换为毫秒时间戳
    
    Args:
        time_input: 时间输入，可以是：
                   - datetime 对象
                   - 字符串格式的时间，例如 '2023-01-01 00:00:00' 或 '2023-01-01'
                   - 整数时间戳（秒或毫秒，自动判断）
                   - None
    
    Returns:
        毫秒时间戳，如果输入为 None 则返回 None
    """
    if time_input is None:
        return None
    
    if isinstance(time_input, datetime):
        return int(time_input.timestamp() * 1000)
    
    if isinstance(time_input, str):
        # 尝试解析字符串格式的时间
        try:
            # 尝试多种时间格式
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y/%m/%d %H:%M:%S', '%Y/%m/%d']:
                try:
                    dt = datetime.strptime(time_input, fmt)
                    return int(dt.timestamp() * 1000)
                except ValueError:
                    continue
            raise ValueError(f"无法解析时间字符串: {time_input}")
        except Exception as e:
            logging.error(f"时间字符串解析失败: {e}")
            raise
    
    if isinstance(time_input, int):
        # 判断是秒还是毫秒时间戳（通常毫秒时间戳 > 10^10）
        if time_input > 1e10:
            return time_input  # 已经是毫秒时间戳
        else:
            return time_input * 1000  # 秒时间戳，转换为毫秒
    
    raise TypeError(f"不支持的时间类型: {type(time_input)}")


def get_and_save_futures_klines(
    symbol: str,
    interval: str = "1m",
    limit: int = 30,
    start_time: Optional[Union[datetime, str, int]] = None,
    end_time: Optional[Union[datetime, str, int]] = None,
    output_dir: str = "data",
    save_csv: bool = False,
    save_json: bool = True
) -> Optional[list]:
    """
    查询并保存 Binance USDT保证金期货合约K线数据
    
    Args:
        symbol: 交易对符号，例如 'BTCUSDT', 'ETHUSDT'
        interval: 时间间隔，例如 '1d' (1天), '1h' (1小时), '1m' (1分钟)
                 可选值: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        limit: 返回的数据条数，默认30，最大1000
        start_time: 开始时间，可以是：
                   - datetime 对象
                   - 字符串格式，例如 '2023-01-01 00:00:00' 或 '2023-01-01'
                   - 整数时间戳（秒或毫秒，自动判断）
                   - None（不指定开始时间）
        end_time: 结束时间，格式同 start_time
                 - None（不指定结束时间）
        output_dir: 保存数据的目录，默认 'data'
        save_csv: 是否保存为 CSV 格式，默认 False
        save_json: 是否保存为 JSON 格式，默认 True
    
    Returns:
        返回查询到的K线数据列表，如果出错返回 None
    
    Note:
        - 如果 start_time 和 end_time 都不指定，返回最近的 limit 条数据
        - 如果只指定 start_time，返回从 start_time 开始的 limit 条数据
        - 如果只指定 end_time，返回 end_time 之前的 limit 条数据
        - 如果同时指定 start_time 和 end_time，返回该时间范围内的数据（最多 limit 条）
    """
    try:
        # 创建配置（公开API，不需要认证）
        configuration_rest_api = ConfigurationRestAPI(
            api_key=os.getenv("API_KEY", ""),
            api_secret=os.getenv("API_SECRET", ""),
            base_path=os.getenv(
                "BASE_PATH", DERIVATIVES_TRADING_USDS_FUTURES_REST_API_PROD_URL
            ),
        )
        
        # 初始化 USDS Futures 客户端
        client = DerivativesTradingUsdsFutures(config_rest_api=configuration_rest_api)
        
        # 将字符串间隔转换为枚举值
        interval_map = {
            "1m": KlineCandlestickDataIntervalEnum.INTERVAL_1m,
            "3m": KlineCandlestickDataIntervalEnum.INTERVAL_3m,
            "5m": KlineCandlestickDataIntervalEnum.INTERVAL_5m,
            "15m": KlineCandlestickDataIntervalEnum.INTERVAL_15m,
            "30m": KlineCandlestickDataIntervalEnum.INTERVAL_30m,
            "1h": KlineCandlestickDataIntervalEnum.INTERVAL_1h,
            "2h": KlineCandlestickDataIntervalEnum.INTERVAL_2h,
            "4h": KlineCandlestickDataIntervalEnum.INTERVAL_4h,
            "6h": KlineCandlestickDataIntervalEnum.INTERVAL_6h,
            "8h": KlineCandlestickDataIntervalEnum.INTERVAL_8h,
            "12h": KlineCandlestickDataIntervalEnum.INTERVAL_12h,
            "1d": KlineCandlestickDataIntervalEnum.INTERVAL_1d,
            "3d": KlineCandlestickDataIntervalEnum.INTERVAL_3d,
            "1w": KlineCandlestickDataIntervalEnum.INTERVAL_1w,
            "1M": KlineCandlestickDataIntervalEnum.INTERVAL_1M,
        }
        
        if interval not in interval_map:
            logging.error(f"不支持的间隔: {interval}")
            return None
        
        interval_enum = interval_map[interval]
        
        # 转换时间参数为毫秒时间戳
        start_time_ms = _convert_to_timestamp_ms(start_time) if start_time is not None else None
        end_time_ms = _convert_to_timestamp_ms(end_time) if end_time is not None else None
        
        # 构建查询日志信息
        time_info = []
        if start_time_ms:
            start_str = datetime.fromtimestamp(start_time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            time_info.append(f"开始时间: {start_str}")
        if end_time_ms:
            end_str = datetime.fromtimestamp(end_time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            time_info.append(f"结束时间: {end_str}")
        time_info_str = ", ".join(time_info) if time_info else "最近数据"
        
        # 查询数据
        logging.info(f"正在查询 {symbol} 的期货合约K线数据，间隔: {interval}, 数量: {limit}, {time_info_str}")
        response = client.rest_api.kline_candlestick_data(
            symbol=symbol,
            interval=interval_enum,
            start_time=start_time_ms,
            end_time=end_time_ms,
            limit=limit
        )
        
        # 获取数据
        klines_data = response.data()
        
        if not klines_data:
            logging.warning("未获取到数据")
            return None
        
        logging.info(f"成功获取 {len(klines_data)} 条数据")
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f"创建目录: {output_dir}")
        
        # 生成文件名（包含时间戳和时间范围）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        time_range_str = ""
        if start_time_ms or end_time_ms:
            if start_time_ms:
                start_str = datetime.fromtimestamp(start_time_ms / 1000).strftime("%Y%m%d_%H%M%S")
                time_range_str += f"_{start_str}"
            if end_time_ms:
                end_str = datetime.fromtimestamp(end_time_ms / 1000).strftime("%Y%m%d_%H%M%S")
                time_range_str += f"_{end_str}"
        base_filename = f"{symbol}_{interval}_{limit}{time_range_str}_{timestamp}"
        
        # 保存为 CSV
        if save_csv:
            csv_filename = os.path.join(output_dir, f"{base_filename}.csv")
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                writer.writerow([
                    '开盘时间', '开盘价', '最高价', '最低价', '收盘价', 
                    '成交量', '收盘时间', '成交额', '成交笔数', 
                    '主动买入成交量', '主动买入成交额', '忽略'
                ])
                
                # 写入数据
                for kline in klines_data:
                    # 转换时间戳为可读格式
                    row = list(kline)
                    # 处理时间戳（可能是int或str）
                    open_time = int(kline[0]) if isinstance(kline[0], str) else kline[0]
                    close_time = int(kline[6]) if isinstance(kline[6], str) else kline[6]
                    row[0] = datetime.fromtimestamp(open_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    row[6] = datetime.fromtimestamp(close_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow(row)
            
            logging.info(f"数据已保存为 CSV: {csv_filename}")
        
        # 保存为 JSON
        if save_json:
            json_filename = os.path.join(output_dir, f"{base_filename}.json")
            
            # 格式化数据以便阅读
            formatted_data = []
            for kline in klines_data:
                # 处理时间戳（可能是int或str）
                open_time = int(kline[0]) if isinstance(kline[0], str) else kline[0]
                close_time = int(kline[6]) if isinstance(kline[6], str) else kline[6]
                
                formatted_data.append({
                    'open_time': open_time,
                    'open_time_str': datetime.fromtimestamp(open_time / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    'open_price': float(kline[1]),
                    'high_price': float(kline[2]),
                    'low_price': float(kline[3]),
                    'close_price': float(kline[4]),
                    'volume': float(kline[5]),
                    'close_time': close_time,
                    'close_time_str': datetime.fromtimestamp(close_time / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    'quote_volume': float(kline[7]),
                    'trades': int(kline[8]),
                    'taker_buy_base_volume': float(kline[9]),
                    'taker_buy_quote_volume': float(kline[10]),
                    'ignore': kline[11]
                })
            
            # 构建元数据
            metadata = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit,
                'data_count': len(formatted_data),
                'timestamp': timestamp,
            }
            
            # 添加时间范围信息
            if start_time_ms:
                metadata['start_time'] = start_time_ms
                metadata['start_time_str'] = datetime.fromtimestamp(start_time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            if end_time_ms:
                metadata['end_time'] = end_time_ms
                metadata['end_time_str'] = datetime.fromtimestamp(end_time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            
            metadata['data'] = formatted_data
            
            with open(json_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(metadata, jsonfile, indent=2, ensure_ascii=False)
            
            logging.info(f"数据已保存为 JSON: {json_filename}")
        
        return klines_data
        
    except Exception as e:
        logging.error(f"查询或保存数据时出错: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None


if __name__ == "__main__":
    # 示例用法
    
    # 示例1: 查询最近的数据（不指定时间范围）
    symbol = "TRUMPUSDT"
    get_and_save_futures_klines(
        symbol=symbol,
        interval="1d",
        limit=365*3,
        output_dir=f"/Users/user/Desktop/repo/crypto_trading/tmp/data/{symbol}_futures"
    )
    
    # 示例2: 使用字符串格式指定时间范围
    # get_and_save_futures_klines(
    #     symbol="BTCUSDT",
    #     interval="1d",
    #     start_time="2023-01-01 00:00:00",
    #     end_time="2023-12-31 23:59:59",
    #     limit=1000,
    #     output_dir="data"
    # )
    
    # 示例3: 使用 datetime 对象指定时间范围
    # from datetime import datetime
    # start = datetime(2023, 1, 1)
    # end = datetime(2023, 12, 31)
    # get_and_save_futures_klines(
    #     symbol="ETHUSDT",
    #     interval="1h",
    #     start_time=start,
    #     end_time=end,
    #     limit=1000,
    #     output_dir="data"
    # )
    
    # 示例4: 使用时间戳（毫秒）
    # get_and_save_futures_klines(
    #     symbol="BTCUSDT",
    #     interval="1d",
    #     start_time=1672531200000,  # 2023-01-01 00:00:00 的毫秒时间戳
    #     end_time=1704067199000,    # 2023-12-31 23:59:59 的毫秒时间戳
    #     limit=1000,
    #     output_dir="data"
    # )
    
    # 示例5: 只指定开始时间
    # get_and_save_futures_klines(
    #     symbol="ETHUSDT",
    #     interval="1d",
    #     start_time="2023-01-01",
    #     limit=365,
    #     output_dir="data"
    # )

