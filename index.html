// ============ 状态管理 ============
let cart = [];
let currentCategory = 'all';

// ============ DOM 引用 ============
const menuGrid = document.getElementById('menuGrid');
const cartItems = document.getElementById('cartItems');
const totalPrice = document.getElementById('totalPrice');
const cartCount = document.getElementById('cartCount');
const cartBadge = document.getElementById('cartBadge');
const cartSidebar = document.getElementById('cartSidebar');
const cartToggle = document.getElementById('cartToggle');
const closeCart = document.getElementById('closeCart');
const checkoutBtn = document.getElementById('checkoutBtn');
const toast = document.getElementById('toast');

// ============ 渲染菜单 ============
function renderMenu(category = 'all') {
    const filtered = category === 'all' 
        ? MENU_ITEMS 
        : MENU_ITEMS.filter(item => item.category === category);
    
    menuGrid.innerHTML = filtered.map(item => `
        <div class="menu-item" data-id="${item.id}">
            <span class="emoji">${item.emoji}</span>
            <h3>${item.name}</h3>
            <p class="description">${item.description}</p>
            <p class="price">¥${item.price.toFixed(2)}</p>
            <button class="add-btn" onclick="addToCart(${item.id})">+</button>
        </div>
    `).join('');
}

// ============ 购物车操作 ============
function addToCart(itemId) {
    const item = MENU_ITEMS.find(i => i.id === itemId);
    if (!item) return;

    const existing = cart.find(i => i.id === itemId);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ ...item, quantity: 1 });
    }

    updateCartUI();
    showToast(`✅ 已添加 ${item.name}`, 'success');
}

function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    updateCartUI();
}

function updateQuantity(itemId, change) {
    const item = cart.find(i => i.id === itemId);
    if (!item) return;

    item.quantity += change;
    if (item.quantity <= 0) {
        removeFromCart(itemId);
        return;
    }
    updateCartUI();
}

function clearCart() {
    cart = [];
    updateCartUI();
}

// ============ 更新 UI ============
function updateCartUI() {
    const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);

    totalPrice.textContent = `¥${total.toFixed(2)}`;
    cartCount.textContent = `🛒 ${count}`;
    cartBadge.textContent = count;

    renderCartItems();
}

function renderCartItems() {
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">🛒 购物车是空的</p>';
        return;
    }

    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.emoji} ${item.name}</div>
                <div class="cart-item-price">¥${(item.price * item.quantity).toFixed(2)}</div>
            </div>
            <div class="cart-item-controls">
                <button onclick="updateQuantity(${item.id}, -1)">−</button>
                <span class="quantity">${item.quantity}</span>
                <button onclick="updateQuantity(${item.id}, 1)">+</button>
                <button onclick="removeFromCart(${item.id})" style="background:#e74c3c;color:white;margin-left:5px;">✕</button>
            </div>
        </div>
    `).join('');
}

// ============ Telegram 通知 ============
async function sendTelegramMessage(orderDetails) {
    const { botToken, chatId } = TELEGRAM_CONFIG;

    // 检查配置
    if (botToken === 'YOUR_BOT_TOKEN' || chatId === 'YOUR_CHAT_ID') {
        showToast('⚠️ 请先配置 Telegram Bot Token 和 Chat ID', 'error');
        return false;
    }

    // 构建消息
    const timestamp = new Date().toLocaleString('zh-CN');
    let message = `🆕 **新订单通知**\n\n`;
    message += `🕐 时间：${timestamp}\n`;
    message += `📋 订单详情：\n`;
    
    orderDetails.items.forEach((item, index) => {
        message += `${index + 1}. ${item.emoji} ${item.name} × ${item.quantity} = ¥${(item.price * item.quantity).toFixed(2)}\n`;
    });
    
    message += `\n💰 总计：**¥${orderDetails.total.toFixed(2)}**`;
    message += `\n\n📦 请尽快准备！`;

    try {
        const response = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
        },
            body: JSON.stringify({
                chat_id: chatId,
                text: message,
                parse_mode: 'Markdown'
            })
        });

        const data = await response.json();
        if (data.ok) {
            showToast('✅ 订单已发送到 Telegram', 'success');
            return true;
        } else {
            showToast(`❌ 发送失败：${data.description}`, 'error');
            return false;
        }
    } catch (error) {
        showToast(`❌ 网络错误：${error.message}`, 'error');
        return false;
    }
}

// ============ 结账 ============
async function handleCheckout() {
    if (cart.length === 0) {
        showToast('⚠️ 购物车是空的', 'error');
        return;
    }

    const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const orderDetails = {
        items: cart.map(item => ({
            id: item.id,
            name: item.name,
            emoji: item.emoji,
            price: item.price,
            quantity: item.quantity
        })),
        total: total
    };

    // 显示订单摘要
    const orderSummary = cart.map(item => 
        `  ${item.emoji} ${item.name} × ${item.quantity} = ¥${(item.price * item.quantity).toFixed(2)}`
    ).join('\n');
    
    const confirmMessage = `📋 确认订单\n\n${orderSummary}\n\n💰 总计：¥${total.toFixed(2)}\n\n确认发送到 Telegram？`;
    
    if (!confirm(confirmMessage)) return;

    // 发送到 Telegram
    const success = await sendTelegramMessage(orderDetails);
    
    if (success) {
        clearCart();
        // 关闭购物车
        cartSidebar.classList.remove('open');
    }
}

// ============ Toast 通知 ============
let toastTimeout;

function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ============ 事件监听 ============
// 分类过滤
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        currentCategory = this.dataset.category;
        renderMenu(currentCategory);
    });
});

// 购物车切换
cartToggle.addEventListener('click', () => {
    cartSidebar.classList.toggle('open');
});

closeCart.addEventListener('click', () => {
    cartSidebar.classList.remove('open');
});

// 点击外部关闭购物车
document.addEventListener('click', (e) => {
    if (cartSidebar.classList.contains('open') && 
        !cartSidebar.contains(e.target) && 
        !cartToggle.contains(e.target)) {
        cartSidebar.classList.remove('open');
    }
});

// 结账按钮
checkoutBtn.addEventListener('click', handleCheckout);

// 键盘快捷键：ESC 关闭购物车
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && cartSidebar.classList.contains('open')) {
        cartSidebar.classList.remove('open');
    }
});

// ============ 初始化 ============
renderMenu();
updateCartUI();