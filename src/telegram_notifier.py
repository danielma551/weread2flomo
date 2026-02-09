"""
Telegram 通知客户端 - L4 原子层
单一职责：通过 Telegram Bot API 发送消息
"""
import html
import os

import requests
from dotenv import load_dotenv

load_dotenv()


class TelegramNotifier:
    """Telegram Bot 消息通知"""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.api_base = os.getenv("TELEGRAM_API_BASE", "https://api.telegram.org")

    def is_enabled(self) -> bool:
        from .config_manager import config
        if not config.should_enable_telegram():
            return False
        return bool(self.bot_token and self.chat_id)

    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        if not self.is_enabled():
            return False
        try:
            url = f"{self.api_base}/bot{self.bot_token}/sendMessage"
            resp = requests.post(url, json={
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode
            }, timeout=10)
            if resp.ok:
                print("📬 Telegram 通知发送成功")
                return True
            else:
                print(f"⚠️  Telegram 通知发送失败: {resp.status_code}")
                return False
        except Exception as e:
            print(f"⚠️  Telegram 通知发送异常: {type(e).__name__}")
            return False

    def format_sync_report(self, stats, total_synced: int,
                           processed_books: int, total_books: int,
                           total_synced_ids: int) -> str:
        duration = stats.get_duration()

        if stats.errors:
            status = "❌ 有错误"
        elif stats.warnings:
            status = "⚠️ 有警告"
        else:
            status = "✅ 成功"

        lines = [
            "<b>📊 WeRead2Flomo 同步报告</b>",
            "",
            f"<b>状态</b>：{status}",
            f"<b>耗时</b>：{duration:.1f} 秒",
            "",
            "<b>📋 基本统计</b>",
            f"  📚 处理书籍：{int(processed_books)}/{int(total_books)}",
            f"  ✨ 本次新同步：{int(total_synced)} 条",
            f"  📊 累计已同步：{int(total_synced_ids)} 条",
            f"  ❌ 失败：{int(stats.failed_highlights)} 条",
        ]

        if stats.ai_summary_attempted > 0 or stats.ai_tags_attempted > 0:
            lines.append("")
            lines.append("<b>🤖 AI 功能</b>")
            if stats.ai_summary_attempted > 0:
                lines.append(f"  摘要：{stats.ai_summary_generated}/{stats.ai_summary_attempted} 成功")
            if stats.ai_tags_attempted > 0:
                lines.append(f"  标签：{stats.ai_tags_generated}/{stats.ai_tags_attempted} 成功")

        if stats.book_details:
            lines.append("")
            lines.append("<b>📖 书籍详情</b>")
            for title, author, count in stats.book_details[:5]:
                safe_title = html.escape(title)
                safe_author = html.escape(author)
                lines.append(f"  · 《{safe_title}》({safe_author}): {count} 条")
            if len(stats.book_details) > 5:
                lines.append(f"  · ...还有 {len(stats.book_details) - 5} 本")

        if stats.warnings:
            lines.append("")
            lines.append(f"<b>⚠️ 警告 ({len(stats.warnings)})</b>")
            for w in stats.warnings[:3]:
                lines.append(f"  · {html.escape(str(w))}")

        if stats.errors:
            lines.append("")
            lines.append(f"<b>❌ 错误 ({len(stats.errors)})</b>")
            for e in stats.errors[:3]:
                lines.append(f"  · {html.escape(str(e))}")

        text = "\n".join(lines)
        if len(text) > 4096:
            text = text[:4090]
            last_newline = text.rfind('\n')
            if last_newline > 3500:
                text = text[:last_newline]
            text += "\n..."
        return text
