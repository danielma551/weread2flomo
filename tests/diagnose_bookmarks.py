"""
划线获取诊断工具
用于检查划线数量不匹配的问题
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from weread_api import initialize_api, get_notebooklist, get_bookmark_list, get_review_list


def diagnose():
    """诊断所有书籍的划线获取情况"""
    
    print("=" * 80)
    print("📊 微信读书划线获取诊断")
    print("=" * 80)
    print()
    
    # 初始化
    print("初始化 API...")
    if not initialize_api():
        print("❌ 初始化失败")
        return
    print("✅ 初始化成功\n")
    
    # 获取书籍列表
    books = get_notebooklist()
    print(f"📚 共找到 {len(books)} 本书\n")
    
    # 统计
    total_with_notes = 0
    match_count = 0
    mismatch_count = 0
    zero_count = 0
    
    mismatches = []
    
    print("检查每本书的划线情况...\n")
    print("-" * 80)
    
    for i, book in enumerate(books):
        book_info = book.get('book', {})
        note_count = book.get('noteCount', 0)
        
        if note_count == 0:
            continue
        
        total_with_notes += 1
        
        book_id = book.get('bookId')
        title = book_info.get('title', '未知')
        author = book_info.get('author', '未知')
        
        # 获取实际划线和评论
        try:
            bookmarks = get_bookmark_list(book_id)
            reviews = get_review_list(book_id)
            
            actual_count = len(bookmarks)
            review_count = len(reviews)
            total_notes = actual_count + review_count
            
            # 判断状态
            if actual_count == 0:
                zero_count += 1
                status = "❌ 零划线"
                print(f"\n{status} [{i+1}] 《{title}》")
                print(f"   作者: {author}")
                print(f"   BookID: {book_id}")
                print(f"   noteCount: {note_count}")
                print(f"   实际划线: {actual_count}")
                print(f"   实际评论: {review_count}")
                print(f"   合计: {total_notes}")
            elif actual_count != note_count:
                mismatch_count += 1
                diff = note_count - actual_count
                status = "⚠️ 不匹配"
                
                mismatches.append({
                    'title': title,
                    'expected': note_count,
                    'actual': actual_count,
                    'reviews': review_count,
                    'diff': diff
                })
                
                if mismatch_count <= 5:  # 只显示前5个不匹配的
                    print(f"\n{status} [{i+1}] 《{title}》")
                    print(f"   noteCount: {note_count}")
                    print(f"   实际划线: {actual_count}")
                    print(f"   实际评论: {review_count}")
                    print(f"   差异: {diff}")
            else:
                match_count += 1
                
        except Exception as e:
            print(f"\n❌ 错误 [{i+1}] 《{title}》: {e}")
    
    # 输出统计
    print("\n" + "=" * 80)
    print("📊 统计结果")
    print("=" * 80)
    print(f"\n总书籍数: {len(books)}")
    print(f"有笔记的书: {total_with_notes}")
    print(f"  ✅ 数量匹配: {match_count}")
    print(f"  ⚠️  数量不匹配: {mismatch_count}")
    print(f"  ❌ 获取为零: {zero_count}")
    
    if mismatches:
        print(f"\n📋 不匹配详情 (前10个):")
        for item in mismatches[:10]:
            print(f"\n  《{item['title']}》")
            print(f"    期望: {item['expected']}, 实际: {item['actual']}, 评论: {item['reviews']}, 差异: {item['diff']}")
    
    # 分析
    print("\n" + "=" * 80)
    print("💡 分析")
    print("=" * 80)
    
    if zero_count > 0:
        print(f"\n⚠️ 发现 {zero_count} 本书显示有笔记但获取为 0")
        print("   可能原因:")
        print("   1. noteCount 包含了评论但不包含划线")
        print("   2. 会话刷新失败")
        print("   3. API 返回了错误但未正确处理")
    
    if mismatch_count > 0:
        print(f"\n⚠️ 发现 {mismatch_count} 本书的数量不匹配")
        print("   可能原因:")
        print("   1. noteCount = 划线 + 评论的总数")
        print("   2. 部分划线被过滤（无 markText 或 chapterUid）")
        print("   3. 同步延迟（网页端显示的数据未同步到 API）")
    
    if match_count == total_with_notes:
        print(f"\n✅ 完美！所有 {total_with_notes} 本书的划线数量都匹配")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    diagnose()







