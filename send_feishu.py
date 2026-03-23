"""
飞书机器人推送
"""
import requests
import json
import os
from datetime import datetime

# 飞书Webhook (需要设置环境变量)
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

def send_feishu_card(news_list, html_url):
    """发送飞书卡片消息"""
    if not FEISHU_WEBHOOK:
        print("⚠️ 未设置飞书Webhook")
        return False
    
    # 限制显示条数
    ai_news = [n for n in news_list if n.get("category") == "ai_hotspot"][:3]
    art_news = [n for n in news_list if n.get("category") in ["art_inspiration", "art_style"]][:3]
    
    # 构建卡片内容
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"🌊 AI Daily - {datetime.now().strftime('%m月%d日')}资讯"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": "**🤖 AI技术热点**"}
                }
            ]
        }
    }
    
    # 添加AI新闻
    for n in ai_news:
        card["card"]["elements"].append({
            "tag": "div",
            "text": {
                "tag": "lark_md", 
                "content": f"• [{n.get('title', '')[:50]}]({n.get('url', '')})"
            }
        })
    
    # 添加艺术新闻
    if art_news:
        card["card"]["elements"].append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": "\n**🎨 艺术灵感**"}
        })
        for n in art_news:
            card["card"]["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md", 
                    "content": f"• [{n.get('title', '')[:50]}]({n.get('url', '')})"
                }
            })
    
    # 添加查看更多按钮
    card["card"]["elements"].append({
        "tag": "action",
        "actions": [
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "📖 查看完整资讯"},
                "type": "primary",
                "url": html_url
            }
        ]
    })
    
    # 发送
    try:
        resp = requests.post(FEISHU_WEBHOOK, json=card, timeout=10)
        print(f"飞书推送结果: {resp.status_code}")
        return resp.status_code == 200
    except Exception as e:
        print(f"飞书推送失败: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # 读取 data.json
    try:
        with open('output/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        news_list = data.get('news', [])
        html_url = 'https://lilyluoli.github.io/ai-daily-news/'
        send_feishu_card(news_list, html_url)
    except FileNotFoundError:
        print("⚠️ output/data.json 不存在")
    except Exception as e:
        print(f"⚠️ 错误: {e}")
