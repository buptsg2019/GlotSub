#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有单元测试
"""
import unittest
import sys


def run_tests():
    """运行所有测试"""
    # 发现并运行测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试模块
    suite.addTests(loader.discover('tests', pattern='test_*.py'))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回退出码
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())

