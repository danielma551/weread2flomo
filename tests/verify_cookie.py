"""
Cookie 验证和刷新工具
"""
import os
import sys
from dotenv import load_dotenv

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weread_api import try_get_cloud_cookie, get_cookie

load_dotenv()


def verify_cookie():
    """验证 Cookie 配置"""
    print("=" * 70)
    print("🔐 Cookie 验证工具")
    print("=" * 70)
    print()

    # 检查环境变量
    print("【检查环境变量】")
    cc_url = os.getenv("CC_URL")
    cc_id = os.getenv("CC_ID")
    cc_password = os.getenv("CC_PASSWORD")
    weread_cookie = os.getenv("WEREAD_COOKIE")

    if cc_url and cc_id and cc_password:
        print(f"   ✓ Cookie Cloud 已配置")
        print(f"     URL: {cc_url}")
        print(f"     ID: {cc_id}")
    else:
        print(f"   ✗ Cookie Cloud 未配置")

    if weread_cookie:
        print(f"   ✓ WEREAD_COOKIE 已配置")
        print(f"     长度: {len(weread_cookie)} 字符")
        if 'wr_skey' in weread_cookie:
            print(f"     ✓ 包含 wr_skey")
        else:
            print(f"     ⚠️  缺少 wr_skey")
    else:
        print(f"   ✗ WEREAD_COOKIE 未配置")
    print()

    # 测试 Cookie Cloud
    if cc_url and cc_id and cc_password:
        print("【测试 Cookie Cloud】")
        cloud_cookie = try_get_cloud_cookie(cc_url, cc_id, cc_password)

        if cloud_cookie:
            print(f"   ✅ Cookie Cloud 返回成功")
            print(f"      长度: {len(cloud_cookie)} 字符")

            if 'wr_skey' in cloud_cookie:
                print(f"      ✓ 包含 wr_skey")

                # 提取 wr_skey 的值(用于对比)
                parts = cloud_cookie.split('; ')
                for part in parts:
                    if part.startswith('wr_skey='):
                        skey = part.split('=', 1)[1]
                        print(f"      wr_skey: {skey[:20]}...")
                        break
            else:
                print(f"      ⚠️  缺少 wr_skey")

            print()
            print("   📋 完整 Cookie 内容:")
            print(f"   {cloud_cookie}")
            print()

            # 建议
            print("   💡 建议:")
            print("   1. 如果这个 Cookie 看起来是最新的，请更新 .env 中的 WEREAD_COOKIE")
            print("   2. 复制上面的完整 Cookie 内容")
            print("   3. 在 .env 文件中设置: WEREAD_COOKIE=\"<复制的内容>\"")
        else:
            print(f"   ❌ Cookie Cloud 获取失败")
            print()
            print("   💡 请检查:")
            print("   1. Cookie Cloud 服务是否可访问")
            print("   2. UUID 和密码是否正确")
            print("   3. Cookie Cloud 中是否已同步微信读书 cookie")
            print()
            print("   🔄 刷新步骤:")
            print("   1. 访问 https://weread.qq.com/")
            print("   2. 微信扫码登录")
            print("   3. 在 Cookie Cloud 插件中点击'立即同步'")
            print("   4. 等待几秒后重新运行此脚本")
    print()

    # 获取最终使用的 Cookie
    print("【获取最终 Cookie】")
    try:
        final_cookie = get_cookie()
        print(f"   ✅ 成功获取 Cookie")
        print(f"      长度: {len(final_cookie)} 字符")

        if 'wr_skey' in final_cookie:
            print(f"      ✓ 包含 wr_skey")
        else:
            print(f"      ⚠️  缺少 wr_skey")
    except Exception as e:
        print(f"   ❌ 获取失败: {e}")

    print()
    print("=" * 70)


if __name__ == "__main__":
    verify_cookie()
