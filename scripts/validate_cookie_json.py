#!/usr/bin/env python3
"""Cookie 验证脚本 - 输出 JSON 格式结果供 GitHub Actions 使用"""
import json
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.weread_api import validate_cookie

result = validate_cookie()
print(json.dumps(result, ensure_ascii=False))
