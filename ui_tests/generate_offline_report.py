"""
生成 Allure 离线报告脚本
将 allure-results 转换为静态 HTML 报告
"""
import os
import sys
import argparse
import subprocess
import shutil


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


def generate_offline_report(allure_path, output_dir="allure-report", clean=True):
    """
    生成离线报告
    
    Args:
        allure_path: Allure 可执行文件路径
        output_dir: 报告输出目录
        clean: 是否清理旧的报告目录
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
    
    # 清理旧的报告目录
    if clean and os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"已清理旧报告目录: {output_dir}")
    
    # 构建 Allure 命令
    cmd = [
        allure_path,
        'generate',
        'allure-results',
        '-o',
        output_dir,
        '--clean'
    ]
    
    print("正在生成离线报告...")
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✓ 离线报告生成成功！")
        print(f"报告位置: {os.path.abspath(output_dir)}")
        print(f"您可以在浏览器中打开 index.html 查看报告")
        return True
    except FileNotFoundError:
        print(f"\n错误：找不到 Allure 可执行文件: {allure_path}")
        print("请使用 --allure-path 参数指定正确的路径")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n错误：生成报告失败！退出码: {e.returncode}")
        return False


def main():
    """
    主函数
    """
    default_allure = get_default_allure_path()
    
    parser = argparse.ArgumentParser(
        description="生成 Allure 离线报告脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
使用示例:
  python generate_offline_report.py                        # 使用默认路径生成报告
  python generate_offline_report.py --allure-path "D:\\allure\\bin\\allure.bat"  # 指定 Allure 路径
  python generate_offline_report.py -o my-report           # 输出到自定义目录
        """
    )
    
    parser.add_argument(
        '--allure-path',
        default=default_allure,
        help=f'Allure 可执行文件路径（默认: {default_allure}）'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        default='allure-report',
        help='报告输出目录（默认: allure-report）'
    )
    
    parser.add_argument(
        '--no-clean',
        action='store_false',
        dest='clean',
        help='不清理旧的报告目录'
    )
    
    args = parser.parse_args()
    
    # 生成报告
    success = generate_offline_report(
        args.allure_path,
        args.output_dir,
        args.clean
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
