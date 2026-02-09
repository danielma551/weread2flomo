"""
配置管理器 - 支持环境变量和 YAML 配置

优先级：环境变量 > config.yaml > 默认值
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = "config.yaml"):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            print(f"⚠️  配置文件不存在: {self.config_path}，使用默认配置")
            return self.get_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config or self.get_default_config()
        except Exception as e:
            print(f"⚠️  加载配置文件失败: {e}，使用默认配置")
            return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'sync': {
                'days_limit': 7,
                'max_highlights_per_sync': 50,
                'sync_reviews': True
            },
            'default_template': 'simple',
            'tags': {
                'default': ['#微信读书'],
                'add_book_title': True,
                'add_author': False,
                'enable_ai_tags': False,
                'max_ai_tags': 3
            },
            'ai': {
                'provider': 'none'
            },
            'advanced': {
                'request_delay': 1.0,
                'log_level': 'INFO'
            },
            'notification': {
                'telegram': {
                    'enabled': False
                }
            }
        }

    def get(self, key: str, default: Any = None, env_key: Optional[str] = None) -> Any:
        """
        获取配置项（优先级：环境变量 > config.yaml > 默认值）

        Args:
            key: 配置键，支持点号分隔的路径，如 'sync.days_limit'
            default: 默认值
            env_key: 对应的环境变量键名（如果提供）

        Returns:
            配置值
        """
        # 1. 优先从环境变量获取
        if env_key:
            env_value = os.getenv(env_key)
            # 如果环境变量存在且不为空字符串
            if env_value is not None and env_value.strip() != '':
                # 先尝试转换为数字（避免 '1' 被当作 True）
                try:
                    if '.' in env_value:
                        return float(env_value)
                    else:
                        return int(env_value)
                except ValueError:
                    pass
                
                # 如果不是数字，再转换布尔值
                if env_value.lower() in ('true', 'yes'):
                    return True
                elif env_value.lower() in ('false', 'no'):
                    return False
                
                # 否则返回字符串
                return env_value
        
        # 2. 从 config.yaml 获取
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_template(self, template_name: Optional[str] = None) -> str:
        """
        获取模板内容

        Args:
            template_name: 模板名称，如果不指定则使用默认模板

        Returns:
            模板字符串
        """
        if template_name is None:
            # 优先从环境变量获取
            template_name = os.getenv('DEFAULT_TEMPLATE') or self.get('default_template', 'simple')

        templates = self.get('templates', {})
        template = templates.get(template_name, {})

        return template.get('format', self.get_default_template())

    def get_default_template(self) -> str:
        """获取默认模板格式"""
        return """📖 《{book_title}》- {author}

> {highlight_text}

{chapter_info}

{tags}"""

    def get_book_category(self, book_title: str, author: str = "") -> Optional[str]:
        """
        根据书名和作者判断书籍分类

        Args:
            book_title: 书名
            author: 作者

        Returns:
            分类名称，如果无法分类则返回None
        """
        categories = self.get('book_categories', {})

        # 检查每个分类的关键词
        for category_name, category_config in categories.items():
            keywords = category_config.get('keywords', [])

            # 检查书名或作者是否包含关键词
            text = f"{book_title} {author}".lower()
            for keyword in keywords:
                if keyword.lower() in text:
                    return category_name

        return None

    def get_category_tags(self, category: str) -> list:
        """
        获取分类的标签

        Args:
            category: 分类名称

        Returns:
            标签列表
        """
        categories = self.get('book_categories', {})
        category_config = categories.get(category, {})
        return category_config.get('tags', [])

    def get_category_template(self, category: str) -> str:
        """
        获取分类的模板

        Args:
            category: 分类名称

        Returns:
            模板名称
        """
        categories = self.get('book_categories', {})
        category_config = categories.get(category, {})
        template_name = category_config.get('template')

        if template_name:
            return self.get_template(template_name)

        return self.get_template()

    def should_enable_ai_tags(self) -> bool:
        """是否启用AI标签"""
        return self.get('tags.enable_ai_tags', False, env_key='ENABLE_AI_TAGS')

    def get_ai_provider(self) -> str:
        """获取AI服务提供商（从 config.yaml）"""
        return self.get('ai.provider', 'none')
    
    def get_ai_api_key(self) -> str:
        """获取AI API Key（从 .env 环境变量，敏感信息）"""
        return os.getenv('AI_API_KEY', '')
    
    def get_ai_api_base(self) -> str:
        """获取AI API Base URL（从 config.yaml）"""
        return self.get('ai.api_base', 'https://api.openai.com/v1')
    
    def get_ai_model(self) -> str:
        """获取AI模型名称（从 config.yaml）"""
        return self.get('ai.model', 'gpt-3.5-turbo')

    def get_days_limit(self) -> int:
        """获取天数限制"""
        return self.get('sync.days_limit', 0, env_key='SYNC_DAYS_LIMIT')

    def get_max_highlights(self) -> int:
        """获取最大划线数限制"""
        return self.get('sync.max_highlights_per_sync', 50, env_key='SYNC_MAX_HIGHLIGHTS')

    def get_request_delay(self) -> float:
        """获取请求延迟"""
        return self.get('advanced.request_delay', 1.0, env_key='REQUEST_DELAY')
    
    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.get('advanced.log_level', 'INFO', env_key='LOG_LEVEL')
    
    def get_max_retries(self) -> int:
        """获取最大重试次数"""
        return self.get('advanced.max_retries', 3, env_key='MAX_RETRIES')
    
    def should_sync_reviews(self) -> bool:
        """是否同步笔记"""
        return self.get('sync.sync_reviews', True, env_key='SYNC_REVIEWS')
    
    def get_max_ai_tags(self) -> int:
        """获取AI标签的最大数量"""
        return self.get('tags.max_ai_tags', 3, env_key='MAX_AI_TAGS')
    
    def should_add_book_title_tag(self) -> bool:
        """是否添加书名作为标签"""
        return self.get('tags.add_book_title', True, env_key='ADD_BOOK_TITLE_TAG')
    
    def should_add_author_tag(self) -> bool:
        """是否添加作者作为标签"""
        return self.get('tags.add_author', False, env_key='ADD_AUTHOR_TAG')
    
    def should_enable_ai_summary(self) -> bool:
        """是否启用AI摘要"""
        return self.get('ai.enable_summary', False, env_key='ENABLE_AI_SUMMARY')
    
    def get_ai_summary_min_length(self) -> int:
        """获取AI摘要的最小文本长度"""
        return self.get('ai.summary_min_length', 100, env_key='AI_SUMMARY_MIN_LENGTH')

    def should_enable_telegram(self) -> bool:
        """是否启用 Telegram 通知"""
        return self.get('notification.telegram.enabled', False, env_key='ENABLE_TELEGRAM')


# 全局配置实例
config = ConfigManager()


if __name__ == "__main__":
    # 测试配置管理器
    print("=== 配置管理器测试 ===\n")

    print(f"天数限制: {config.get_days_limit()}")
    print(f"默认模板: {config.get('default_template')}")
    print(f"启用AI标签: {config.should_enable_ai_tags()}")

    print("\n=== 测试书籍分类 ===")
    test_books = [
        ("高效能人士的七个习惯", "史蒂芬·柯维"),
        ("三体", "刘慈欣"),
        ("代码大全", "史蒂夫·迈克康奈尔"),
    ]

    for title, author in test_books:
        category = config.get_book_category(title, author)
        print(f"\n书名: {title}")
        print(f"作者: {author}")
        print(f"分类: {category}")
        if category:
            print(f"标签: {config.get_category_tags(category)}")

    print("\n=== 模板示例 ===")
    template = config.get_template('simple')
    print(template)
