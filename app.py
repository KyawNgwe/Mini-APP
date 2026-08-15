import logging
from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, CallbackContext
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 从环境变量读取配置
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # 接收通知的群组或用户ID

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# ----- 1. 处理点餐请求（示例API） -----
@app.route('/api/order', methods=['POST'])
def handle_order():
    """当客人通过网页/小程序点餐后，前端调用此接口"""
    order_data = request.get_json()
    if not order_data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    # 组装通知消息
    message = (
        f"📢 **新订单通知**\n"
        f"👤 顾客：{order_data.get('customer_name', '匿名')}\n"
        f"📞 电话：{order_data.get('phone', '无')}\n"
        f"📍 地址：{order_data.get('address', '无')}\n\n"
        f"📋 **订单详情：**\n"
    )
    total = 0
    for item in order_data.get('items', []):
        name = item.get('name')
        price = item.get('price')
        quantity = item.get('quantity', 1)
        subtotal = price * quantity
        total += subtotal
        message += f"- {name} x{quantity} = ¥{subtotal}\n"
    message += f"\n💰 **总计：¥{total}**"

    # 发送Telegram通知
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
        return jsonify({"status": "success", "message": "通知已发送"}), 200
    except Exception as e:
        logging.error(f"发送Telegram消息失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# ----- 2. 处理Telegram Bot命令（可选） -----
def start(update: Update, context: CallbackContext):
    update.message.reply_text("你好！欢迎使用点餐系统。请通过我们的网站或小程序下单。")

def handle_message(update: Update, context: CallbackContext):
    update.message.reply_text("请通过我们的官方渠道下单，谢谢！")

# 注册处理器
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ----- 3. Flask路由处理Telegram Webhook -----
@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram将用户消息通过此URL推送过来"""
    if request.method == "POST":
        json_str = request.get_data().decode('UTF-8')
        update = Update.de_json(json_str, bot)
        dispatcher.process_update(update)
        return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)