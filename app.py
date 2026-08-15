# -*- coding: utf-8 -*-
import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# ==================== 配置区域（必填）====================
TELEGRAM_BOT_TOKEN = "8939398684:AAHscEJ4st2XHCBNgFpcfpFH7Cu8MqNLTjk"   # 替换为 @BotFather 给你的 Token
TELEGRAM_CHAT_ID = "1949334561"       # 替换为你的用户 ID（或群组 ID）
# =======================================================

# ---------- Telegram 发送函数 ----------
def send_telegram_message(order_data):
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID":
        print("⚠️ 请先配置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")
        return False

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
{ '备注：' + order_data['customer'].get('note', '') if order_data['customer'].get('note') else '' }

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

# ---------- 菜单数据 ----------
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

# ---------- 内嵌 HTML（就是之前完整的点餐页面）----------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
    <title>🍽️ 点菜系统</title>
    <style>
        /* 全部样式代码（太长省略，实际使用时复制之前的完整样式） */
        /* 这里为了节省篇幅，我放一个极简样式，但建议你用之前完整样式 */
        * { margin:0; padding:0; box-sizing:border-box; font-family: system-ui; }
        body { background:#f7f3eb; padding:16px; display:flex; justify-content:center; }
        .app-container { max-width:1400px; width:100%; background:#fffdf9; border-radius:32px; padding:24px 28px 32px; box-shadow: 0 20px 60px rgba(0,0,0,0.08); }
        .header { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-bottom:28px; border-bottom:2px solid #f0e8e0; padding-bottom:16px; }
        .header h1 { font-size:28px; font-weight:700; color:#3d2c1b; }
        .header h1 span { background:#e8590c; color:#fff; font-size:14px; padding:2px 12px; border-radius:20px; margin-left:10px; }
        .main-grid { display:grid; grid-template-columns:1fr 380px; gap:32px; }
        .category { margin-bottom:32px; }
        .category-title { font-size:20px; font-weight:600; color:#3d2c1b; border-left:5px solid #e8590c; padding-left:12px; margin-bottom:14px; }
        .dish-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:14px; }
        .dish-card { background:#fff; border-radius:18px; padding:16px; box-shadow:0 2px 10px rgba(0,0,0,0.03); border:1px solid #f0e8e0; }
        .dish-emoji { font-size:28px; }
        .dish-name { font-weight:600; font-size:17px; color:#2d1f12; }
        .dish-desc { font-size:13px; color:#8a7a6a; margin:4px 0 10px; }
        .dish-bottom { display:flex; justify-content:space-between; align-items:center; }
        .dish-price { font-weight:700; font-size:18px; color:#e8590c; }
        .btn-add { background:#e8590c; color:#fff; border:none; border-radius:40px; padding:6px 18px; font-weight:600; cursor:pointer; }
        .cart-section { background:#fcf9f6; border-radius:24px; padding:20px; border:1px solid #f0e8e0; position:sticky; top:20px; }
        .cart-header { display:flex; justify-content:space-between; margin-bottom:18px; }
        .cart-count { background:#e8590c; color:#fff; border-radius:30px; padding:0 12px; line-height:26px; }
        .cart-list { max-height:340px; overflow-y:auto; margin-bottom:16px; }
        .cart-empty { text-align:center; color:#b0a094; padding:36px 0; }
        .cart-item { display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #eee7e0; }
        .cart-item-controls { display:flex; align-items:center; gap:8px; }
        .btn-qty { width:28px; height:28px; border-radius:30px; border:1px solid #ddd2c8; background:#fff; font-size:16px; cursor:pointer; }
        .item-qty { font-weight:600; min-width:20px; text-align:center; }
        .cart-total { display:flex; justify-content:space-between; padding:16px 0 12px; border-top:2px dashed #e0d6cc; font-weight:600; }
        .total-price { font-size:26px; color:#e8590c; }
        .customer-form { display:flex; flex-direction:column; gap:12px; }
        .form-row { display:flex; gap:10px; flex-wrap:wrap; }
        .field { flex:1; min-width:120px; }
        .customer-form label { font-size:13px; font-weight:500; color:#5a4a3a; display:block; margin-bottom:3px; }
        .customer-form input, .customer-form textarea { width:100%; padding:10px 14px; border-radius:12px; border:1px solid #e0d6cc; font-size:15px; }
        .btn-submit { background:#e8590c; color:#fff; border:none; border-radius:40px; padding:14px; font-size:18px; font-weight:700; cursor:pointer; }
        .toast { position:fixed; bottom:30px; left:50%; transform:translateX(-50%); background:#2d1f12; color:#fff; padding:14px 28px; border-radius:60px; opacity:0; transition:0.35s; pointer-events:none; }
        .toast.show { opacity:1; }
        @media (max-width:900px) { .main-grid { grid-template-columns:1fr; } .cart-section { position:static; } }
    </style>
</head>
<body>
<div class="app-container">
    <header class="header"><h1>🍽️ 点菜 <span>堂食/外卖</span></h1></header>
    <div class="main-grid">
        <section class="menu-section" id="menuSection"></section>
        <aside class="cart-section">
            <div class="cart-header"><h2>🛒 购物车</h2><span class="cart-count" id="cartCount">0</span></div>
            <div class="cart-list" id="cartList"><div class="cart-empty">🧺 还没有点菜</div></div>
            <div class="cart-total"><span>合计</span><span class="total-price" id="totalPrice">0.00</span></div>
            <div class="customer-form">
                <div class="form-row">
                    <div class="field"><label>👤 姓名 *</label><input id="custName" placeholder="张先生" /></div>
                    <div class="field"><label>📞 电话 *</label><input id="custPhone" placeholder="手机号" /></div>
                </div>
                <div class="field"><label>📝 备注</label><textarea id="custNote" placeholder="口味/桌号/地址"></textarea></div>
                <button class="btn-submit" id="submitBtn">📤 提交订单</button>
            </div>
        </aside>
    </div>
</div>
<div id="toast" class="toast"></div>
<script>
// 菜单数据（和 Python 中保持一致）
const MENU_DATA = {{ menu|tojson }};
let cart = {};
const menuSection = document.getElementById('menuSection');
const cartList = document.getElementById('cartList');
const cartCount = document.getElementById('cartCount');
const totalPriceEl = document.getElementById('totalPrice');
const submitBtn = document.getElementById('submitBtn');
const custName = document.getElementById('custName');
const custPhone = document.getElementById('custPhone');
const custNote = document.getElementById('custNote');
const toast = document.getElementById('toast');
let toastTimer = null;

function renderMenu() {
    let html = '';
    for (const [category, dishes] of Object.entries(MENU_DATA)) {
        html += `<div class="category"><div class="category-title">${category}</div><div class="dish-grid">`;
        for (const d of dishes) {
            html += `<div class="dish-card">
                <div class="dish-emoji">${d.emoji||'🍽️'}</div>
                <div class="dish-name">${d.name}</div>
                <div class="dish-desc">${d.desc||''}</div>
                <div class="dish-bottom">
                    <span class="dish-price">${d.price}</span>
                    <button class="btn-add" data-id="${d.id}" data-name="${d.name}" data-price="${d.price}">+ 加入</button>
                </div>
            </div>`;
        }
        html += `</div></div>`;
    }
    menuSection.innerHTML = html;
}

function addToCart(id, name, price) {
    if (cart[id]) cart[id].quantity += 1;
    else cart[id] = { id, name, price, quantity: 1 };
    renderCart();
    showToast(`➕ 已添加 ${name}`);
}

function changeQty(id, delta) {
    if (!cart[id]) return;
    cart[id].quantity += delta;
    if (cart[id].quantity <= 0) delete cart[id];
    renderCart();
}

function getItems() { return Object.values(cart); }
function getTotal() { return getItems().reduce((s,i) => s + i.price * i.quantity, 0); }
function getCount() { return getItems().reduce((s,i) => s + i.quantity, 0); }

function renderCart() {
    const items = getItems();
    cartCount.textContent = getCount();
    totalPriceEl.textContent = getTotal().toFixed(2);
    if (items.length === 0) {
        cartList.innerHTML = `<div class="cart-empty">🧺 还没有点菜</div>`;
        return;
    }
    let html = '';
    for (const item of items) {
        html += `<div class="cart-item">
            <div><div class="cart-item-name">${item.name}</div><div>¥${item.price}/份</div></div>
            <div class="cart-item-controls">
                <button class="btn-qty" data-id="${item.id}" data-delta="-1">−</button>
                <span class="item-qty">${item.quantity}</span>
                <button class="btn-qty" data-id="${item.id}" data-delta="1">+</button>
                <span>¥${(item.price*item.quantity).toFixed(2)}</span>
            </div>
        </div>`;
    }
    cartList.innerHTML = html;
    cartList.querySelectorAll('.btn-qty').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(btn.dataset.id);
            const delta = parseInt(btn.dataset.delta);
            changeQty(id, delta);
        });
    });
}

function showToast(msg, type='') {
    if (toastTimer) clearTimeout(toastTimer);
    toast.textContent = msg;
    toast.className = 'toast show';
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2500);
}

async function submitOrder() {
    const items = getItems();
    if (items.length === 0) { showToast('⚠️ 购物车为空', 'error'); return; }
    const name = custName.value.trim(), phone = custPhone.value.trim();
    if (!name || !phone) { showToast('⚠️ 请填写姓名和电话', 'error'); return; }
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ 提交中...';
    try {
        const resp = await fetch('/api/order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                items: items.map(i => ({ name: i.name, price: i.price, quantity: i.quantity })),
                customer: { name, phone, note: custNote.value.trim() || '' }
            })
        });
        const result = await resp.json();
        if (resp.ok && result.success) {
            showToast('✅ 订单提交成功！已通知老板');
            cart = {}; renderCart();
            custName.value = ''; custPhone.value = ''; custNote.value = '';
        } else {
            showToast('❌ ' + (result.message || '提交失败'), 'error');
        }
    } catch(e) {
        showToast('❌ 网络错误，请检查服务器', 'error');
    }
    submitBtn.disabled = false;
    submitBtn.textContent = '📤 提交订单';
}

// 事件绑定
menuSection.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-add');
    if (!btn) return;
    addToCart(parseInt(btn.dataset.id), btn.dataset.name, parseFloat(btn.dataset.price));
});
submitBtn.addEventListener('click', submitOrder);
renderMenu();
renderCart();
</script>
</body>
</html>
"""

# ---------- Flask 路由 ----------
@app.route('/')
def index():
    # 把菜单数据传入模板渲染
    return render_template_string(HTML_TEMPLATE, menu=MENU)

@app.route('/api/menu')
def get_menu():
    return jsonify(MENU)

@app.route('/api/order', methods=['POST'])
def submit_order():
    data = request.get_json()
    if not data or 'items' not in data or 'customer' not in data:
        return jsonify({"success": False, "message": "订单数据不完整"}), 400
    if not data['items']:
        return jsonify({"success": False, "message": "购物车为空"}), 400

    success = send_telegram_message(data)
    if success:
        return jsonify({"success": True, "message": "订单提交成功！"})
    else:
        return jsonify({"success": False, "message": "通知发送失败，请稍后重试"}), 500

if __name__ == '__main__':
    print("="*50)
    print("🍽️  点菜系统已启动")
    print(f"📱 访问 http://127.0.0.1:5000 开始点菜")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)