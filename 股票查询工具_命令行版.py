"""
股票平均价格查询工具 - 命令行版本
适用于Windows/Mac/Linux系统
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印标题"""
    print("=" * 70)
    print(" " * 20 + "股票平均价格查询工具")
    print(" " * 25 + "v1.0")
    print("=" * 70)
    print()

def get_stock_data(stock_code, months):
    """
    获取股票数据并计算平均价格
    
    参数:
        stock_code: 股票代码 (如 "300919")
        months: 月份数
    """
    try:
        # 计算时间范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        
        print(f"\n⏳ 正在获取股票 {stock_code} 的数据...")
        print(f"   时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
        print(f"   请稍候...\n")
        
        # 获取数据
        stock_df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_date_str,
            end_date=end_date_str,
            adjust="qfq"  # 前复权
        )
        
        if stock_df.empty:
            print("❌ 未获取到数据,请检查股票代码是否正确!")
            return None
        
        # 计算统计数据
        trade_days = len(stock_df)
        avg_close = stock_df['收盘'].mean()
        vwap = (stock_df['收盘'] * stock_df['成交量']).sum() / stock_df['成交量'].sum()
        max_price = stock_df['收盘'].max()
        min_price = stock_df['收盘'].min()
        latest_price = stock_df['收盘'].iloc[-1]
        latest_date = stock_df['日期'].iloc[-1]
        
        # 显示结果
        print("=" * 70)
        print("📊 数据统计结果")
        print("=" * 70)
        print(f"\n股票代码: {stock_code}")
        print(f"交易天数: {trade_days} 天")
        print(f"最新价格: {latest_price:.2f} 元 ({latest_date})")
        print(f"\n" + "-" * 70)
        print(f"💰 平均价格:")
        print(f"   ├─ 算术平均价: {avg_close:.2f} 元")
        print(f"   │  计算方式: {stock_df['收盘'].sum():.2f} ÷ {trade_days} = {avg_close:.2f}")
        print(f"   │")
        print(f"   └─ 成交量加权均价: {vwap:.2f} 元")
        print(f"      计算方式: (收盘价×成交量)之和 ÷ 总成交量")
        print(f"\n" + "-" * 70)
        print(f"📈 价格区间:")
        print(f"   最高价: {max_price:.2f} 元")
        print(f"   最低价: {min_price:.2f} 元")
        print(f"   波动幅度: {((max_price - min_price) / min_price * 100):.2f}%")
        print("=" * 70)
        
        # 保存CSV文件
        filename = f"股票数据_{stock_code}_近{months}个月_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        stock_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 数据已保存至: {filename}")
        print(f"   文件位置: {os.path.abspath(filename)}\n")
        
        return {
            "股票代码": stock_code,
            "交易天数": trade_days,
            "算术平均价": round(avg_close, 2),
            "成交量加权均价": round(vwap, 2),
            "最新价格": round(latest_price, 2),
            "数据文件": filename
        }
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        print("   可能的原因:")
        print("   1. 股票代码不正确")
        print("   2. 网络连接问题")
        print("   3. akshare库未正确安装\n")
        return None

def main():
    """主程序"""
    while True:
        clear_screen()
        print_header()
        
        # 输入股票代码
        print("请输入股票代码 (直接回车使用默认值 300919):")
        stock_code = input("股票代码: ").strip()
        if not stock_code:
            stock_code = "300919"
            print(f"   → 使用默认值: {stock_code} (中伟股份)")
        
        # 输入时间区间
        print("\n请输入查询月数 (直接回车使用默认值 6个月):")
        months_input = input("月数: ").strip()
        if not months_input:
            months = 6
            print(f"   → 使用默认值: {months} 个月")
        else:
            try:
                months = int(months_input)
                if months <= 0 or months > 60:
                    print("   ⚠️  月数范围应在 1-60 之间,使用默认值 6")
                    months = 6
            except ValueError:
                print("   ⚠️  输入无效,使用默认值 6 个月")
                months = 6
        
        # 获取数据
        result = get_stock_data(stock_code, months)
        
        # 询问是否继续
        print("\n" + "=" * 70)
        choice = input("\n是否继续查询其他股票? (Y/N,直接回车继续): ").strip().upper()
        if choice == 'N':
            print("\n感谢使用!再见!\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已退出,再见!\n")
        sys.exit(0)
