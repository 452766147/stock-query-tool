"""
股票平均价格查询工具 - 图形界面版本 v2.3
适用于Windows系统,双击即可运行
性能优化: 延迟导入akshare库,启动速度更快
v2.2: 添加代理设置选项,修复代理导致的连接问题
v2.3: 添加多数据源支持(东方财富+腾讯),自动切换备用数据源
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
# import akshare as ak  # 延迟导入,提升启动速度
# import pandas as pd   # 延迟导入,提升启动速度
from datetime import datetime, timedelta
import threading
import os

class StockQueryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股票平均价格查询工具 v2.3")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        
        # 延迟导入标志
        self.akshare_loaded = False
        
        # 设置窗口图标(如果有的话)
        try:
            # self.root.iconbitmap('icon.ico')  # 如果有图标文件
            pass
        except:
            pass
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        
        # 标题
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame,
            text="📈 股票平均价格查询工具",
            font=("微软雅黑", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # 输入区域
        input_frame = tk.LabelFrame(
            self.root,
            text="  查询参数  ",
            font=("微软雅黑", 10, "bold"),
            padx=20,
            pady=15
        )
        input_frame.pack(padx=20, pady=20, fill=tk.X)
        
        # 股票代码
        code_frame = tk.Frame(input_frame)
        code_frame.pack(fill=tk.X, pady=5)
        tk.Label(
            code_frame,
            text="股票代码:",
            font=("微软雅黑", 10),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)
        self.code_entry = tk.Entry(
            code_frame,
            font=("微软雅黑", 10),
            width=20
        )
        self.code_entry.pack(side=tk.LEFT, padx=10)
        self.code_entry.insert(0, "300919")
        tk.Label(
            code_frame,
            text="(默认: 300919 中伟股份)",
            font=("微软雅黑", 9),
            fg="gray"
        ).pack(side=tk.LEFT)
        
        # 开始日期
        start_date_frame = tk.Frame(input_frame)
        start_date_frame.pack(fill=tk.X, pady=5)
        tk.Label(
            start_date_frame,
            text="开始日期:",
            font=("微软雅黑", 10),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)
        # 默认为6个月前
        default_start = datetime.now() - timedelta(days=180)
        self.start_date_picker = DateEntry(
            start_date_frame,
            font=("微软雅黑", 10),
            width=18,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            year=default_start.year,
            month=default_start.month,
            day=default_start.day
        )
        self.start_date_picker.pack(side=tk.LEFT, padx=10)
        tk.Label(
            start_date_frame,
            text="(选择查询起始日期)",
            font=("微软雅黑", 9),
            fg="gray"
        ).pack(side=tk.LEFT)
        
        # 结束日期
        end_date_frame = tk.Frame(input_frame)
        end_date_frame.pack(fill=tk.X, pady=5)
        tk.Label(
            end_date_frame,
            text="结束日期:",
            font=("微软雅黑", 10),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)
        self.end_date_picker = DateEntry(
            end_date_frame,
            font=("微软雅黑", 10),
            width=18,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.end_date_picker.pack(side=tk.LEFT, padx=10)
        tk.Label(
            end_date_frame,
            text="(选择查询结束日期)",
            font=("微软雅黑", 9),
            fg="gray"
        ).pack(side=tk.LEFT)
        
        # 代理设置区域
        proxy_frame = tk.Frame(input_frame)
        proxy_frame.pack(fill=tk.X, pady=5)
        tk.Label(
            proxy_frame,
            text="网络设置:",
            font=("微软雅黑", 10),
            width=10,
            anchor='w'
        ).pack(side=tk.LEFT)
        self.no_proxy_var = tk.BooleanVar(value=True)  # 默认禁用代理
        self.no_proxy_check = tk.Checkbutton(
            proxy_frame,
            text="禁用代理直连",
            font=("微软雅黑", 10),
            variable=self.no_proxy_var
        )
        self.no_proxy_check.pack(side=tk.LEFT, padx=10)
        tk.Label(
            proxy_frame,
            text="(如遇连接问题,请勾选此项)",
            font=("微软雅黑", 9),
            fg="gray"
        ).pack(side=tk.LEFT)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.query_button = tk.Button(
            button_frame,
            text="🔍 开始查询",
            font=("微软雅黑", 11, "bold"),
            bg="#3498db",
            fg="white",
            width=15,
            height=1,
            cursor="hand2",
            command=self.start_query
        )
        self.query_button.pack(side=tk.LEFT, padx=10)
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ 清空结果",
            font=("微软雅黑", 11),
            bg="#95a5a6",
            fg="white",
            width=15,
            height=1,
            cursor="hand2",
            command=self.clear_result
        )
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(
            self.root,
            text="  查询结果  ",
            font=("微软雅黑", 10, "bold"),
            padx=10,
            pady=10
        )
        result_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=("Consolas", 10),
            wrap=tk.WORD,
            height=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_bar = tk.Label(
            self.root,
            text="就绪",
            font=("微软雅黑", 9),
            bg="#ecf0f1",
            anchor='w',
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def clear_result(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.update_status("结果已清空")
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.config(text=message)
        self.root.update()
    
    def log_message(self, message):
        """在结果区域显示消息"""
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.see(tk.END)
        self.root.update()
    
    def start_query(self):
        """开始查询(在新线程中执行)"""
        # 禁用查询按钮
        self.query_button.config(state=tk.DISABLED)
        self.clear_result()
        
        # 在新线程中执行查询
        thread = threading.Thread(target=self.query_stock)
        thread.daemon = True
        thread.start()
    
    def fetch_stock_data(self, stock_code, start_date, end_date):
        """
        获取股票数据 - 多数据源策略
        按顺序尝试多个数据源，直到成功获取数据
        """
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        
        # 确定股票市场前缀
        if stock_code.startswith('6'):
            market_prefix = "sh"
            market_code = "1"  # 上海
        else:
            market_prefix = "sz"
            market_code = "0"  # 深圳
        
        # 数据源1: 东方财富 (stock_zh_a_hist)
        self.log_message("📡 尝试数据源1: 东方财富...")
        try:
            stock_df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date_str,
                end_date=end_date_str,
                adjust="qfq"
            )
            if stock_df is not None and not stock_df.empty:
                self.log_message("✅ 东方财富数据获取成功!")
                return stock_df
        except Exception as e:
            self.log_message(f"⚠️ 东方财富接口异常: {str(e)[:80]}")
        
        # 数据源2: 腾讯 (stock_zh_a_daily)
        self.log_message("📡 尝试数据源2: 腾讯...")
        try:
            symbol_tencent = f"{market_prefix}{stock_code}"
            stock_df = ak.stock_zh_a_daily(symbol=symbol_tencent, adjust="qfq")
            
            if stock_df is not None and not stock_df.empty:
                stock_df = stock_df.rename(columns={
                    'date': '日期', 'open': '开盘', 'high': '最高',
                    'low': '最低', 'close': '收盘', 'volume': '成交量', 'amount': '成交额'
                })
                stock_df['日期'] = pd.to_datetime(stock_df['日期'])
                start_dt = pd.to_datetime(start_date)
                end_dt = pd.to_datetime(end_date)
                stock_df = stock_df[(stock_df['日期'] >= start_dt) & (stock_df['日期'] <= end_dt)]
                stock_df['日期'] = stock_df['日期'].dt.strftime('%Y-%m-%d')
                stock_df = stock_df.reset_index(drop=True)
                self.log_message("✅ 腾讯数据获取成功!")
                return stock_df
        except Exception as e:
            self.log_message(f"⚠️ 腾讯接口异常: {str(e)[:80]}")
        
        # 数据源3: 新浪 (stock_zh_a_hist_163)
        self.log_message("📡 尝试数据源3: 网易财经...")
        try:
            stock_df = ak.stock_zh_a_hist_163(
                symbol=stock_code,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
            if stock_df is not None and not stock_df.empty:
                stock_df = stock_df.rename(columns={
                    '日期': '日期', '开盘价': '开盘', '最高价': '最高',
                    '最低价': '最低', '收盘价': '收盘', '成交量': '成交量', '成交金额': '成交额'
                })
                if '日期' in stock_df.columns:
                    stock_df['日期'] = pd.to_datetime(stock_df['日期']).dt.strftime('%Y-%m-%d')
                stock_df = stock_df.reset_index(drop=True)
                self.log_message("✅ 网易财经数据获取成功!")
                return stock_df
        except Exception as e:
            self.log_message(f"⚠️ 网易财经接口异常: {str(e)[:80]}")
        
        # 数据源4: 百度股市通
        self.log_message("📡 尝试数据源4: 百度股市通...")
        try:
            stock_df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period="daily",
                start_date=start_date.strftime("%Y-%m-%d %H:%M:%S"),
                end_date=end_date.strftime("%Y-%m-%d %H:%M:%S"),
                adjust="qfq"
            )
            if stock_df is not None and not stock_df.empty:
                stock_df = stock_df.rename(columns={
                    '时间': '日期', '开盘': '开盘', '最高': '最高',
                    '最低': '最低', '收盘': '收盘', '成交量': '成交量', '成交额': '成交额'
                })
                stock_df['日期'] = pd.to_datetime(stock_df['日期']).dt.strftime('%Y-%m-%d')
                stock_df = stock_df.drop_duplicates(subset=['日期'], keep='last')
                stock_df = stock_df.reset_index(drop=True)
                self.log_message("✅ 百度股市通数据获取成功!")
                return stock_df
        except Exception as e:
            self.log_message(f"⚠️ 百度股市通接口异常: {str(e)[:80]}")
        
        # 数据源5: 同花顺
        self.log_message("📡 尝试数据源5: 同花顺...")
        try:
            stock_df = ak.stock_zh_a_hist_pre_min_em(
                symbol=stock_code,
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d")
            )
            if stock_df is not None and not stock_df.empty:
                self.log_message("✅ 同花顺数据获取成功!")
                return stock_df
        except Exception as e:
            self.log_message(f"⚠️ 同花顺接口异常: {str(e)[:80]}")
        
        # 所有数据源都失败
        self.log_message("❌ 所有数据源均不可用，请检查网络或稍后重试")
        return pd.DataFrame()
    
    def query_stock(self):
        """查询股票数据"""
        try:
            # 处理代理设置
            if self.no_proxy_var.get():
                # 禁用代理，直连
                os.environ['NO_PROXY'] = '*'
                os.environ['no_proxy'] = '*'
                # 清除可能存在的代理设置
                for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
                    if proxy_var in os.environ:
                        del os.environ[proxy_var]
                self.log_message("🌐 已禁用代理,使用直连模式\n")
            
            # 首次查询时才导入akshare和pandas(延迟导入优化)
            if not self.akshare_loaded:
                self.update_status("正在加载数据模块...")
                self.log_message("⏳ 首次使用,正在加载数据模块,请稍候...\n")
                global ak, pd
                import akshare as ak
                import pandas as pd
                self.akshare_loaded = True
                self.log_message("✅ 数据模块加载完成!\n")
            
            # 获取输入参数
            stock_code = self.code_entry.get().strip()
            if not stock_code:
                messagebox.showwarning("输入错误", "请输入股票代码!")
                self.query_button.config(state=tk.NORMAL)
                return
            
            # 获取日期范围
            start_date = self.start_date_picker.get_date()
            end_date = self.end_date_picker.get_date()
            
            # 验证日期范围
            if start_date >= end_date:
                messagebox.showwarning("日期错误", "开始日期必须早于结束日期!")
                self.query_button.config(state=tk.NORMAL)
                return
            
            # 检查日期范围是否过大(最多5年)
            date_diff = (end_date - start_date).days
            if date_diff > 1825:  # 5年
                messagebox.showwarning("日期范围过大", "查询范围不能超过5年!")
                self.query_button.config(state=tk.NORMAL)
                return
            
            # 转换为字符串格式
            start_date_str = start_date.strftime("%Y%m%d")
            end_date_str = end_date.strftime("%Y%m%d")
            
            self.update_status("正在获取数据...")
            self.log_message("=" * 60)
            self.log_message(f"正在查询股票: {stock_code}")
            self.log_message(f"时间范围: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
            self.log_message("请稍候...")
            self.log_message("")
            
            # 获取数据 - 使用多数据源策略
            stock_df = self.fetch_stock_data(stock_code, start_date, end_date)
            
            if stock_df.empty:
                self.log_message("❌ 未获取到数据,请检查股票代码是否正确!")
                self.update_status("查询失败")
                self.query_button.config(state=tk.NORMAL)
                return
            
            # 计算统计数据
            trade_days = len(stock_df)
            avg_close = stock_df['收盘'].mean()
            vwap = (stock_df['收盘'] * stock_df['成交量']).sum() / stock_df['成交量'].sum()
            max_price = stock_df['收盘'].max()
            min_price = stock_df['收盘'].min()
            latest_price = stock_df['收盘'].iloc[-1]
            latest_date = stock_df['日期'].iloc[-1]
            
            # 显示结果
            self.log_message("=" * 60)
            self.log_message("📊 数据统计结果")
            self.log_message("=" * 60)
            self.log_message(f"\n股票代码: {stock_code}")
            self.log_message(f"交易天数: {trade_days} 天")
            self.log_message(f"最新价格: {latest_price:.2f} 元 ({latest_date})")
            self.log_message(f"\n" + "-" * 60)
            self.log_message(f"💰 平均价格:")
            self.log_message(f"   ├─ 算术平均价: {avg_close:.2f} 元")
            self.log_message(f"   │  计算方式: {stock_df['收盘'].sum():.2f} ÷ {trade_days} = {avg_close:.2f}")
            self.log_message(f"   │")
            self.log_message(f"   └─ 成交量加权均价: {vwap:.2f} 元")
            self.log_message(f"      计算方式: (收盘价×成交量)之和 ÷ 总成交量")
            self.log_message(f"\n" + "-" * 60)
            self.log_message(f"📈 价格区间:")
            self.log_message(f"   最高价: {max_price:.2f} 元")
            self.log_message(f"   最低价: {min_price:.2f} 元")
            self.log_message(f"   波动幅度: {((max_price - min_price) / min_price * 100):.2f}%")
            self.log_message("=" * 60)
            
            # 保存CSV文件
            filename = f"股票数据_{stock_code}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            stock_df.to_csv(filename, index=False, encoding='utf-8-sig')
            
            file_path = os.path.abspath(filename)
            self.log_message(f"\n✅ 数据已保存至:")
            self.log_message(f"   {file_path}")
            self.log_message("")
            
            self.update_status(f"查询完成! 数据已保存至 {filename}")
            
            # 弹出成功提示
            messagebox.showinfo(
                "查询成功",
                f"股票代码: {stock_code}\n"
                f"算术平均价: {avg_close:.2f} 元\n"
                f"成交量加权均价: {vwap:.2f} 元\n\n"
                f"数据已保存至:\n{filename}"
            )
            
        except Exception as e:
            error_msg = str(e)
            self.log_message(f"\n❌ 错误: {error_msg}")
            self.log_message("\n可能的原因及解决方案:")
            self.log_message("1. 股票代码不正确 - 请检查股票代码")
            self.log_message("2. 网络连接问题 - 请检查网络连接")
            self.log_message("3. 代理设置问题 - 请尝试勾选'禁用代理直连'选项")
            self.log_message("4. 数据源临时不可用 - 请稍后重试")
            self.log_message("5. akshare库未正确安装 - 请重新安装")
            
            # 针对代理错误的特殊提示
            if 'Proxy' in error_msg or 'proxy' in error_msg or 'RemoteDisconnected' in error_msg:
                self.log_message("\n💡 检测到可能是代理问题!")
                self.log_message("   建议: 勾选上方'禁用代理直连'选项后重试")
            
            self.update_status("查询失败")
            messagebox.showerror("查询失败", f"错误信息:\n{error_msg}")
        
        finally:
            # 重新启用查询按钮
            self.query_button.config(state=tk.NORMAL)

def main():
    """主程序"""
    root = tk.Tk()
    app = StockQueryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
