import os
import logging
import csv
import json
from datetime import datetime
from typing import Optional

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


def get_and_save_futures_klines(
    symbol: str,
    interval: str = "1m",
    limit: int = 30,
    output_dir: str = "data",
    save_csv: bool = True,
    save_json: bool = True
) -> Optional[list]:
    """
    查询并保存 Binance USDT保证金期货合约K线数据
    
    Args:
        symbol: 交易对符号，例如 'BTCUSDT', 'ETHUSDT'
        interval: 时间间隔，例如 '1d' (1天), '1h' (1小时), '1m' (1分钟)
                 可选值: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
        limit: 返回的数据条数，默认30，最大1000
        output_dir: 保存数据的目录，默认 'data'
        save_csv: 是否保存为 CSV 格式，默认 True
        save_json: 是否保存为 JSON 格式，默认 True
    
    Returns:
        返回查询到的K线数据列表，如果出错返回 None
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
        
        # 查询数据
        logging.info(f"正在查询 {symbol} 的期货合约K线数据，间隔: {interval}, 数量: {limit}")
        response = client.rest_api.kline_candlestick_data(
            symbol=symbol,
            interval=interval_enum,
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
        
        # 生成文件名（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{symbol}_{interval}_{limit}_{timestamp}"
        
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
            
            with open(json_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump({
                    'symbol': symbol,
                    'interval': interval,
                    'limit': limit,
                    'data_count': len(formatted_data),
                    'timestamp': timestamp,
                    'data': formatted_data
                }, jsonfile, indent=2, ensure_ascii=False)
            
            logging.info(f"数据已保存为 JSON: {json_filename}")
        
        return klines_data
        
    except Exception as e:
        logging.error(f"查询或保存数据时出错: {e}")
        import traceback
        logging.error(traceback.format_exc())
        return None


if __name__ == "__main__":
    # 示例用法
    # 查询 BTCUSDT 期货合约最近30条1分钟K线数据
    symbol = "BTCUSDT"
    get_and_save_futures_klines(
        symbol=symbol,
        interval="1m",
        limit=30,
        output_dir=f"/Users/user/Desktop/repo/crypto_trading/tmp/data/{symbol}_futures"
    )
    
    # 查询 ETHUSDT 期货合约最近100条日线数据
    # get_and_save_futures_klines(
    #     symbol="ETHUSDT",
    #     interval="1d",
    #     limit=100,
    #     output_dir="data"
    # )

