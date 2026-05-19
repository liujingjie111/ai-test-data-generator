"""
运行测试用例脚本
支持选择不同模块运行测试
"""
import os
import sys
import argparse
import subprocess


def get_test_modules():
    """
    获取所有可用的测试模块
    
    Returns:
        模块名称列表
    """
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    modules = []
    
    if os.path.exists(tests_dir):
        for filename in os.listdir(tests_dir):
            if filename.startswith('test_') and filename.endswith('.py'):
                module_name = filename[:-3]  # 去掉 .py 后缀
                modules.append(module_name)
    
    return sorted(modules)


def run_tests(module=None):
    """
    运行测试用例
    
    Args:
        module: 模块名称，如果为 None 则运行所有测试
    """
    # 切换到 ui_tests 目录
    ui_tests_dir = os.path.dirname(__file__)
    os.chdir(ui_tests_dir)
    
    # 构建 pytest 命令
    cmd = ['pytest', '-v', '--tb=short']
    
    if module:
        # 运行特定模块
        cmd.append(f'tests/{module}.py')
        print(f"正在运行测试模块: {module}")
    else:
        # 运行所有测试
        print("正在运行所有测试...")
    
    # 执行命令
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("\n测试运行完成，但有失败的用例。")
    else:
        print("\n所有测试运行成功！")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(
        description="运行测试用例脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_tests.py              # 运行所有测试
  python run_tests.py -m generator  # 仅运行 generator 模块的测试
  python run_tests.py -l           # 列出所有可用的测试模块
        """
    )
    
    parser.add_argument(
        '-m', '--module',
        help='指定要运行的测试模块名称'
    )
    
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='列出所有可用的测试模块'
    )
    
    args = parser.parse_args()
    
    if args.list:
        # 列出可用模块
        modules = get_test_modules()
        print("可用的测试模块:")
        for module in modules:
            print(f"  - {module}")
        return
    
    # 运行测试
    run_tests(args.module)


if __name__ == '__main__':
    main()
