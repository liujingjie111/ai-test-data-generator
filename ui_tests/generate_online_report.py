"""
生成 Allure 在线报告脚本
启动本地服务器实时查看测试报告
"""
import os
import sys
import argparse
import subprocess
import webbrowser
import time


def get_default_allure_path():
    """
    获取默认的 Allure 路径
    
    Returns:
        Allure 可执行文件路径
    """
    # 常见的 Allure 路径
    possible_paths = [
        r"D:\allure-2.39.0\bin\allure.bat",  # 用户之前提到的路径
        r"C:\allure\bin\allure.bat",
        r"C:\Program Files\Allure\bin\allure.bat",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return "allure"  # 假设在系统 PATH 中


def start_online_server(allure_path, host="127.0.0.1", port=0, open_browser=True):
    """
    启动在线报告服务器
    
    Args:
        allure_path: Allure 可执行文件路径
        host: 服务器监听地址
        port: 服务器端口，0 表示随机分配
        open_browser: 是否自动打开浏览器
    """
    # 切换到 ui_tests 目录
    ui_tests_dir = os.path.dirname(__file__)
    os.chdir(ui_tests_dir)
    
    # 检查是否有测试结果
    results_dir = "allure-results"
    if not os.path.exists(results_dir):
        print(f"错误：找不到测试结果目录: {results_dir}")
        print("请先运行测试！")
        return False
    
    # 检查是否有结果文件
    result_files = [f for f in os.listdir(results_dir) if f.endswith('.json') or f.endswith('.txt') or f.endswith('.png')]
    if not result_files:
        print(f"错误：测试结果目录为空: {results_dir}")
        print("请先运行测试！")
        return False
    
    # 构建 Allure 命令
    cmd = [
        allure_path,
        'serve',
        'allure-results',
        '--host',
        host
    ]
    
    if port > 0:
        cmd.extend(['--port', str(port)])
    
    print("正在启动在线报告服务器...")
    print(f"报告将在浏览器中打开（按 Ctrl+C 停止服务器）")
    
    try:
        # 启动服务器进程
        process = subprocess.Popen(cmd)
        
        # 等待服务器启动（给一些时间）
        time.sleep(3)
        
        # 自动打开浏览器
        if open_browser:
            url = f"http://{host}"
            if port > 0:
                url += f":{port}"
            else:
                url += ":5252"  # Allure 默认端口
            print(f"正在打开浏览器: {url}")
            webbrowser.open(url)
        
        # 等待用户按 Ctrl+C
        print("\n服务器正在运行，按 Ctrl+C 停止...")
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n正在停止服务器...")
            process.terminate()
            process.wait()
            print("服务器已停止。")
        
        return True
    except FileNotFoundError:
        print(f"\n错误：找不到 Allure 可执行文件: {allure_path}")
        print("请使用 --allure-path 参数指定正确的路径")
        return False
    except Exception as e:
        print(f"\n错误：启动服务器失败！{str(e)}")
        return False


def main():
    """
    主函数
    """
    default_allure = get_default_allure_path()
    
    parser = argparse.ArgumentParser(
        description="启动 Allure 在线报告服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
使用示例:
  python generate_online_report.py                        # 使用默认配置启动服务器
  python generate_online_report.py --allure-path "D:\\allure\\bin\\allure.bat"  # 指定 Allure 路径
  python generate_online_report.py -p 8080                # 指定端口为 8080
  python generate_online_report.py --no-open              # 不自动打开浏览器
        """
    )
    
    parser.add_argument(
        '--allure-path',
        default=default_allure,
        help=f'Allure 可执行文件路径（默认: {default_allure}）'
    )
    
    parser.add_argument(
        '-H', '--host',
        default='127.0.0.1',
        help='服务器监听地址（默认: 127.0.0.1）'
    )
    
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=0,
        help='服务器端口（0 表示随机分配，默认自动）'
    )
    
    parser.add_argument(
        '--no-open',
        action='store_false',
        dest='open_browser',
        help='不自动打开浏览器'
    )
    
    args = parser.parse_args()
    
    # 启动服务器
    success = start_online_server(
        args.allure_path,
        args.host,
        args.port,
        args.open_browser
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
