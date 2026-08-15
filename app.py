# app.py - Flask 主应用
import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ===== 配置区域（请修改为你自己的信息）=====
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # 替换为你的 Bot Token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"      # 替换为你的 Chat ID
# =========================================

# Telegram 发送消息函数
def send_telegram_message(order_data):
    """将订单信息发送到 Telegram"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID":
        print("⚠️ 请先配置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")
        return False

    # 构建消息内容
    items_text = ""
    total_price = 0
    for item in order_data['items']:
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        items_text += f"• {item['name']} x{item['quantity']} = ¥{subtotal:.2f}\n"

    message = f"""
📋 **新订单来了！**
━━━━━━━━━━━━━━━━━
👤 **顾客信息**
姓名：{order_data['customer']['name']}
电话：{order_data['customer']['phone']}
{ '备注：' + order_data['customer']['note'] if order_data['customer'].get('note') else '' }

🍽️ **点餐明细**
{items_text}
━━━━━━━━━━━━━━━━━
💰 **总计：¥{total_price:.2f}**

🕐 下单时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ 订单已发送到 Telegram")
            return True
        else:
            print(f"❌ 发送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False

# ===== 菜单数据 =====
MENU = {
    "热销推荐": [
        {"id": 1, "name": "招牌红烧肉", "price": 58, "emoji": "🥩", "desc": "肥而不腻，入口即化"},
        {"id": 2, "name": "清蒸鲈鱼", "price": 68, "emoji": "🐟", "desc": "鲜美滑嫩，原汁原味"},
        {"id": 3, "name": "宫保鸡丁", "price": 48, "emoji": "🍗", "desc": "麻辣鲜香，经典川菜"},
    ],
    "家常小炒": [
        {"id": 4, "name": "青椒肉丝", "price": 32, "emoji": "🌶️", "desc": "下饭好菜"},
        {"id": 5, "name": "西红柿炒蛋", "price": 28, "emoji": "🍅", "desc": "酸甜可口，营养丰富"},
        {"id": 6, "name": "干煸四季豆", "price": 26, "emoji": "🥬", "desc": "香辣脆嫩"},
    ],
    "汤品": [
        {"id": 7, "name": "紫菜蛋花汤", "price": 18, "emoji": "🥣", "desc": "清淡鲜美"},
        {"id": 8, "name": "玉米排骨汤", "price": 38, "emoji": "🌽", "desc": "香甜浓郁"},
    ],
    "主食": [
        {"id": 9, "name": "白米饭", "price": 3, "emoji": "🍚", "desc": "香软可口"},
        {"id": 10, "name": "炒面", "price": 15, "emoji": "🍜", "desc": "锅气十足"},
    ]
}

# ===== 路由 =====
@app.route('/')
def index():
    """点菜页面"""
    return render_template('index.html', menu=MENU)

@app.route('/api/menu')
def get_menu():
    """获取菜单 API"""
    return jsonify(MENU)

@app.route('/api/order', methods=['POST'])
def submit_order():
    """提交订单 API"""
    data = request.get_json()

    if not data or 'items' not in data or 'customer' not in data:
        return jsonify({"success": False, "message": "订单数据不完整"}), 400

    if not data['items']:
        return jsonify({"success": False, "message": "购物车为空"}), 400

    # 发送到 Telegram
    success = send_telegram_message(data)

    if success:
        return jsonify({"success": True, "message": "订单提交成功！"})
    else:
        return jsonify({"success": False, "message": "订单提交失败，请稍后重试"}), 500

# ===== 启动 =====
if __name__ == '__main__':
    print("=" * 50)
    print("🍽️  点菜系统已启动")
    print(f"📱 访问 http://127.0.0.1:5000 开始点菜")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)