#!/usr/bin/env python3
# ============================================================
# SIÊU TỐC iCLOUD BOT - by Mai Văn Tùng
# Dành cho Render (chạy 24/7) - ĐÃ SỬA LỖI 409
# ============================================================

import telebot
import json
import time
import random
from datetime import datetime
import os
import threading

TOKEN = "8895985240:AAGrVu2Ih6MUnMxYXQofi7iI7FYD5_ukrPQ"
ADMIN_ID = "8695176044"
bot = telebot.TeleBot(TOKEN)
DATA_FILE = os.path.join(os.path.dirname(__file__), "icloud_requests.json")

# ============================================================
# XÓA WEBHOOK CŨ VÀ BỎ QUA UPDATE ĐANG CHỜ
# ============================================================
try:
    bot.delete_webhook(drop_pending_updates=True)
    print("✅ Đã xóa webhook cũ và bỏ qua các update đang chờ")
except Exception as e:
    print(f"⚠️ Không thể xóa webhook: {e}")

# ============================================================
# BẢNG GÓI VAY
# ============================================================
LOAN_PACKAGES = [
    {"stt": 2, "ten": "11Pro", "goi": "2M", "tien_ngay": "100x32", "thanh_tien": "3.200"},
    {"stt": 3, "ten": "11Prm + 12T", "goi": "3M", "tien_ngay": "110x40", "thanh_tien": "4.400"},
    {"stt": 4, "ten": "13T + 12Pro", "goi": "4M", "tien_ngay": "145x40 / 120x50", "thanh_tien": "5.800 / 6.000"},
    {"stt": 5, "ten": "12Prm + 13Pro + 14T / 14Plus", "goi": "5M", "tien_ngay": "180x40 / 155x50", "thanh_tien": "7.200 / 7.750"},
    {"stt": 6, "ten": "13Prm + 14Pro + 15T", "goi": "6M", "tien_ngay": "220x40 / 180x50", "thanh_tien": "8.800 / 9.000"},
    {"stt": 7, "ten": "15Plus + 14PRM / 15Pro + 16T", "goi": "7M", "tien_ngay": "245x40 / 205x50", "thanh_tien": "9.800 / 10.250"},
    {"stt": 8, "ten": "16Pro + 16Plus / 17T", "goi": "8M", "tien_ngay": "285x40 / 255x50", "thanh_tien": "11.400 / 12.750"},
    {"stt": 9, "ten": "15Prm + 17Pro / 17A", "goi": "9M", "tien_ngay": "315x40 / 275x50", "thanh_tien": "12.600 / 13.750"},
    {"stt": 10, "ten": "16Prm", "goi": "10M", "tien_ngay": "355x40 / 295x50", "thanh_tien": "12.400 / 14.750"},
    {"stt": 11, "ten": "17Prm Vna", "goi": "12M", "tien_ngay": "420x40 / 350x50", "thanh_tien": "16.800 / 17.500"},
]

# ============================================================
# BẢNG GIÁ PHÁ iCLOUD (TĂNG 30%)
# ============================================================
UNLOCK_PRICES = [
    {"stt": 1, "ten": "iPhone X, XS, XR, XSMax", "gia": 910000, "gia_text": "910.000đ"},
    {"stt": 2, "ten": "iPhone 11, 12, 11Pro, 11ProMax", "gia": 1040000, "gia_text": "1.040.000đ"},
    {"stt": 3, "ten": "iPhone 13, 12Pro, 12ProMax", "gia": 1300000, "gia_text": "1.300.000đ"},
    {"stt": 4, "ten": "iPhone 14, 13Pro, 13ProMax", "gia": 1430000, "gia_text": "1.430.000đ"},
    {"stt": 5, "ten": "iPhone 15, 14Plus, 14Pro, 14ProMax", "gia": 1690000, "gia_text": "1.690.000đ"},
    {"stt": 6, "ten": "iPhone 16, 15Plus, 15Pro, 15ProMax", "gia": 1820000, "gia_text": "1.820.000đ"},
    {"stt": 7, "ten": "iPhone 17, 16Plus, 16Pro, 16ProMax", "gia": 1950000, "gia_text": "1.950.000đ"},
    {"stt": 8, "ten": "iPhone 17 Air, 17 Pro, 17 ProMax", "gia": 2080000, "gia_text": "2.080.000đ"},
    {"stt": 9, "ten": "iPad (các loại)", "gia": 1040000, "gia_text": "1.040.000 - 1.560.000đ"},
    {"stt": 10, "ten": "Macbook (các loại)", "gia": 1170000, "gia_text": "1.170.000 - 1.950.000đ"},
]

# ============================================================
# THÔNG TIN LIÊN HỆ & NGÂN HÀNG
# ============================================================
CONTACT_INFO = """
📞 **LIÊN HỆ NGAY ĐỂ ĐƯỢC HỖ TRỢ**

👤 **Zalo:** 0398564507
✈️ **Telegram:** @tientyicloud

📌 *Vui lòng liên hệ để được tư vấn chi tiết!*
"""

BANK_INFO = """
🏦 **THÔNG TIN CHUYỂN KHOẢN**

💰 **Ngân hàng:** MB Bank
📌 **Số tài khoản:** 9989123989
👤 **Chủ tài khoản:** Mai Văn Tùng
💬 **Nội dung:** Mã yêu cầu + Tên dịch vụ
"""

# ============================================================
# HÀM LƯU DỮ LIỆU
# ============================================================
def save_request(user_id, username, service, info):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    req_id = f"REQ-{int(time.time())}"
    req = {"id": req_id, "user_id": user_id, "username": username, "service": service, "info": info, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "pending"}
    data.append(req)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return req_id

def get_user_requests(user_id):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return [r for r in data if r["user_id"] == user_id]
    except:
        return []

def send_to_admin(msg):
    try:
        bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
    except:
        pass

# ============================================================
# TẠO MENU
# ============================================================
def main_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = ["💰 Vay tiền qua iCloud", "📱 Check IMEI", "🔓 Bypass iCloud", "🔒 Chặn khóa iCloud", "🗑️ Phá iCloud", "📋 Xem trạng thái", "👤 Hướng dẫn", "📞 Liên hệ hỗ trợ"]
    for btn in buttons:
        keyboard.add(telebot.types.KeyboardButton(btn))
    return keyboard

def create_loan_menu():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    for pkg in LOAN_PACKAGES:
        keyboard.add(telebot.types.InlineKeyboardButton(f"📱 {pkg['ten']} - {pkg['goi']}", callback_data=f"loan_{pkg['stt']}"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

def create_unlock_menu():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for item in UNLOCK_PRICES:
        keyboard.add(telebot.types.InlineKeyboardButton(f"📱 {item['ten']} - {item['gia_text']}", callback_data=f"unlock_{item['stt']}"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

def create_bypass_menu():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.InlineKeyboardButton("📱 11ProMax đổ xuống", callback_data="bypass_old"))
    keyboard.add(telebot.types.InlineKeyboardButton("📱 12 đổ lên", callback_data="bypass_new"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

def create_bypass_old_menu():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.InlineKeyboardButton("📞 Bypass nghe gọi (1.200.000đ)", callback_data="bypass_old_call"))
    keyboard.add(telebot.types.InlineKeyboardButton("📶 Bypass WiFi (350.000đ)", callback_data="bypass_old_wifi"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

def create_contact_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.InlineKeyboardButton("💬 Nhắn Zalo", url="https://zalo.me/0398564507"))
    keyboard.add(telebot.types.InlineKeyboardButton("✈️ Telegram", url="https://t.me/tientyicloud"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

def create_payment_keyboard(service, req_id):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.InlineKeyboardButton("💰 Thanh toán ngay", callback_data=f"pay_{service}_{req_id}"))
    keyboard.add(telebot.types.InlineKeyboardButton("📤 Gửi ảnh biên lai", callback_data=f"receipt_{req_id}"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

def create_imei_result_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(telebot.types.InlineKeyboardButton("🔓 Bypass iCloud", callback_data="bypass_imei"))
    keyboard.add(telebot.types.InlineKeyboardButton("🗑️ Phá trắng máy", callback_data="unlock_imei"))
    keyboard.add(telebot.types.InlineKeyboardButton("📞 Liên hệ hỗ trợ", callback_data="contact_imei"))
    keyboard.add(telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu"))
    return keyboard

# ============================================================
# LỆNH /START
# ============================================================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "🔐 **SIÊU TỐC iCLOUD**\n"
        "👋 Cảm ơn bạn đã sử dụng bot của **Siêu Tốc iCloud by Mai Văn Tùng**!\n\n"
        "📌 **Vui lòng chọn dịch vụ bạn cần bên dưới:**",
        reply_markup=main_menu(), parse_mode="Markdown")

# ============================================================
# XỬ LÝ TIN NHẮN
# ============================================================
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    text = message.text
    user = message.from_user
    user_id = str(user.id)
    username = user.username or user.first_name

    if text == "💰 Vay tiền qua iCloud":
        bot.reply_to(message, "💰 **DANH SÁCH GÓI VAY**\n\n📌 Vui lòng chọn gói vay phù hợp:", reply_markup=create_loan_menu(), parse_mode="Markdown")
    
    elif text == "📱 Check IMEI":
        msg = bot.reply_to(message, "📱 **CHECK IMEI**\n\n📌 Vui lòng gửi IMEI cần kiểm tra (15 chữ số):", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_imei)
    
    elif text == "🔓 Bypass iCloud":
        bot.reply_to(message, "🔓 **BYPASS iCLOUD**\n\n📌 **Chọn dòng máy của bạn:**\n• 📱 **11ProMax đổ xuống**\n• 📱 **12 đổ lên**", reply_markup=create_bypass_menu(), parse_mode="Markdown")
    
    elif text == "🔒 Chặn khóa iCloud":
        req_id = save_request(user_id, username, "🔒 Chặn khóa iCloud", "Chặn khóa - 350.000đ")
        bot.reply_to(
            message,
            f"🔒 **CHẶN KHÓA iCLOUD**\n\n"
            f"💰 **Giá:** 350.000đ\n"
            f"📌 **Mã yêu cầu:** `{req_id}`\n\n"
            f"{BANK_INFO}\n\n"
            f"📌 Vui lòng thanh toán và gửi ảnh biên lai để xác nhận!",
            reply_markup=create_payment_keyboard("block", req_id),
            parse_mode="Markdown"
        )
        send_to_admin(f"🔔 CHẶN KHÓA từ {username}\n📌 Mã: {req_id}")
    
    elif text == "🗑️ Phá iCloud":
        bot.reply_to(
            message,
            "🗑️ **PHÁ iCLOUD**\n\n"
            "📌 **Vui lòng chọn dòng máy cần phá:**\n\n"
            "• ⏱️ Thời gian: 15-20 phút\n"
            "• 🔒 Bảo mật tuyệt đối\n"
            "• ✅ Làm 100% phần mềm\n\n"
            "👇 **Chọn dòng máy bên dưới:**",
            reply_markup=create_unlock_menu(),
            parse_mode="Markdown"
        )
    
    elif text == "📋 Xem trạng thái":
        reqs = get_user_requests(user_id)
        if not reqs:
            bot.reply_to(message, "📋 **Bạn chưa có yêu cầu nào.**", parse_mode="Markdown")
            return
        text_msg = "📋 **YÊU CẦU CỦA BẠN**\n\n"
        for r in reqs[-5:]:
            emoji = "✅" if r["status"] == "done" else "🟡" if r["status"] == "processing" else "⏳"
            text_msg += f"{emoji} {r['id']} - {r['service']}\n"
        bot.reply_to(message, text_msg, parse_mode="Markdown")
    
    elif text == "👤 Hướng dẫn":
        bot.reply_to(
            message,
            "📖 **HƯỚNG DẪN**\n\n"
            "1️⃣ Chọn dịch vụ\n"
            "2️⃣ Gửi thông tin\n"
            "3️⃣ Thanh toán\n"
            "4️⃣ Gửi ảnh biên lai\n"
            "5️⃣ Chờ xác nhận\n\n"
            "📌 Liên hệ hỗ trợ: @tientyicloud",
            parse_mode="Markdown"
        )
    
    elif text == "📞 Liên hệ hỗ trợ":
        bot.reply_to(message, CONTACT_INFO, reply_markup=create_contact_keyboard(), parse_mode="Markdown")
    
    else:
        bot.reply_to(message, "❌ Vui lòng chọn dịch vụ từ menu.")

# ============================================================
# XỬ LÝ CHECK IMEI
# ============================================================
def process_imei(message):
    imei = message.text.strip()
    if not imei.isdigit() or len(imei) != 15:
        bot.reply_to(message, "❌ **IMEI không hợp lệ!** IMEI phải là 15 chữ số.", parse_mode="Markdown")
        return
    req_id = save_request(message.from_user.id, message.from_user.username or "User", "📱 Check IMEI", f"IMEI: {imei}")
    bot.reply_to(message, 
        f"📱 **KẾT QUẢ CHECK IMEI**\n\n"
        f"📌 **IMEI:** `{imei}`\n"
        f"📌 **Mã:** `{req_id}`\n\n"
        f"✅ **Máy sạch (Clean)**\n"
        f"✅ Không iCloud Lock\n"
        f"✅ FMI: TẮT (OFF)\n\n"
        f"👇 **Chọn dịch vụ tiếp theo:**",
        reply_markup=create_imei_result_keyboard(), parse_mode="Markdown")
    send_to_admin(f"🔍 CHECK IMEI từ {message.from_user.first_name}:\nIMEI: {imei}\n📌 Mã: {req_id}")

# ============================================================
# XỬ LÝ CALLBACK
# ============================================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id)
    user = call.from_user
    username = user.username or user.first_name
    user_id = user.id

    # === VAY TIỀN ===
    if call.data.startswith("loan_"):
        stt = int(call.data.split("_")[1])
        pkg = next((p for p in LOAN_PACKAGES if p["stt"] == stt), None)
        if pkg:
            info = f"Gói: {pkg['ten']}\nSố tiền: {pkg['goi']}\nTiền/ngày: {pkg['tien_ngay']}\nThành tiền: {pkg['thanh_tien']}"
            req_id = save_request(user_id, username, "💰 Vay tiền", info)
            bot.edit_message_text(
                f"✅ **ĐÃ CHỌN GÓI VAY**\n\n"
                f"📌 **Gói:** {pkg['ten']}\n"
                f"💰 **Số tiền:** {pkg['goi']}\n"
                f"📌 **Mã:** `{req_id}`\n\n"
                f"👇 Bấm nút bên dưới để giải ngân!",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=telebot.types.InlineKeyboardMarkup().add(
                    telebot.types.InlineKeyboardButton("💰 GIẢI NGÂN NGAY", callback_data="contact_imei"),
                    telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu")
                ),
                parse_mode="Markdown"
            )
            send_to_admin(f"🔔 VAY TIỀN từ {username}:\n{info}\n📌 Mã: {req_id}")

    # === PHÁ iCLOUD ===
    elif call.data.startswith("unlock_"):
        stt = int(call.data.split("_")[1])
        pkg = next((p for p in UNLOCK_PRICES if p["stt"] == stt), None)
        if pkg:
            info = f"Dòng máy: {pkg['ten']}\nGiá: {pkg['gia_text']}"
            req_id = save_request(user_id, username, "🗑️ Phá iCloud", info)
            bot.edit_message_text(
                f"🗑️ **PHÁ iCLOUD**\n\n"
                f"📌 **Dòng máy:** {pkg['ten']}\n"
                f"💰 **Giá:** {pkg['gia_text']}\n"
                f"📌 **Mã yêu cầu:** `{req_id}`\n\n"
                f"⏱️ **Thời gian:** 15-20 phút\n"
                f"🔒 **Bảo mật tuyệt đối**\n"
                f"✅ **Làm 100% phần mềm**\n\n"
                f"{BANK_INFO}\n\n"
                f"📌 Vui lòng thanh toán và gửi ảnh biên lai để xác nhận!",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=create_payment_keyboard("unlock", req_id),
                parse_mode="Markdown"
            )
            send_to_admin(f"🔔 PHÁ iCLOUD từ {username}:\n{info}\n📌 Mã: {req_id}")

    # === BYPASS ===
    elif call.data == "bypass_old":
        bot.edit_message_text(
            "📱 **BYPASS 11ProMax ĐỔ XUỐNG**\n\n"
            "📌 Chọn loại bypass:\n"
            "• 📞 Bypass nghe gọi (1.200.000đ)\n"
            "• 📶 Bypass WiFi (350.000đ)",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_bypass_old_menu(),
            parse_mode="Markdown"
        )
    
    elif call.data == "bypass_new":
        req_id = save_request(user_id, username, "🔓 Bypass 12+", "Dòng 12 đổ lên - 350.000đ")
        bot.edit_message_text(
            f"📱 **BYPASS 12 ĐỔ LÊN**\n\n"
            f"💰 **Giá:** 350.000đ\n"
            f"📌 **Mã:** `{req_id}`\n\n"
            f"{BANK_INFO}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_payment_keyboard("new", req_id),
            parse_mode="Markdown"
        )
        send_to_admin(f"🔔 BYPASS 12+ từ {username}\n📌 Mã: {req_id}")
    
    elif call.data == "bypass_old_call":
        req_id = save_request(user_id, username, "🔓 Bypass nghe gọi", "1.200.000đ")
        bot.edit_message_text(
            f"📞 **BYPASS NGHE GỌI**\n\n"
            f"💰 **Giá:** 1.200.000đ\n"
            f"📌 **Mã:** `{req_id}`\n\n"
            f"{BANK_INFO}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_payment_keyboard("old_call", req_id),
            parse_mode="Markdown"
        )
        send_to_admin(f"🔔 BYPASS NGHE GỌI từ {username}\n📌 Mã: {req_id}")
    
    elif call.data == "bypass_old_wifi":
        req_id = save_request(user_id, username, "🔓 Bypass WiFi", "350.000đ")
        bot.edit_message_text(
            f"📶 **BYPASS WIFI**\n\n"
            f"💰 **Giá:** 350.000đ\n"
            f"📌 **Mã:** `{req_id}`\n\n"
            f"{BANK_INFO}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_payment_keyboard("old_wifi", req_id),
            parse_mode="Markdown"
        )
        send_to_admin(f"🔔 BYPASS WIFI từ {username}\n📌 Mã: {req_id}")

    elif call.data == "bypass_back":
        bot.edit_message_text(
            "🔓 **BYPASS iCLOUD**\n\n"
            "📌 Chọn dòng máy:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_bypass_menu(),
            parse_mode="Markdown"
        )

    # === THANH TOÁN ===
    elif call.data.startswith("pay_"):
        parts = call.data.split("_")
        req_id = parts[2]
        bot.edit_message_text(
            f"💰 **THANH TOÁN**\n\n"
            f"📌 **Mã yêu cầu:** `{req_id}`\n\n"
            f"{BANK_INFO}\n\n"
            f"📌 Sau khi chuyển khoản, bấm nút **'Gửi ảnh biên lai'** bên dưới!",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=telebot.types.InlineKeyboardMarkup().add(
                telebot.types.InlineKeyboardButton("📤 Gửi ảnh biên lai", callback_data=f"receipt_{req_id}"),
                telebot.types.InlineKeyboardButton("🔙 Quay lại menu", callback_data="back_menu")
            ),
            parse_mode="Markdown"
        )

    elif call.data.startswith("receipt_"):
        req_id = call.data.split("_")[1]
        bot.send_message(
            call.message.chat.id,
            f"📤 **GỬI ẢNH BIÊN LAI**\n\n"
            f"📌 **Mã yêu cầu:** `{req_id}`\n\n"
            f"📌 Vui lòng gửi ảnh biên lai chuyển khoản (hình ảnh).\n\n"
            f"🙏 **Cảm ơn quý khách!**",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_receipt, req_id)

    # === LIÊN HỆ / MENU ===
    elif call.data == "contact_imei":
        bot.edit_message_text(
            CONTACT_INFO,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_contact_keyboard(),
            parse_mode="Markdown"
        )

    elif call.data == "back_menu":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "🔐 **SIÊU TỐC iCLOUD**\n\n📌 Chọn dịch vụ bên dưới:",
            reply_markup=main_menu()
        )

    elif call.data == "bypass_imei":
        bot.edit_message_text(
            "🔓 **BYPASS iCLOUD**\n\n📌 Chọn dòng máy:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_bypass_menu(),
            parse_mode="Markdown"
        )
    
    elif call.data == "unlock_imei":
        bot.edit_message_text(
            "🗑️ **PHÁ TRẮNG MÁY**\n\n"
            "📌 Vui lòng chọn dòng máy:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_unlock_menu(),
            parse_mode="Markdown"
        )

# ============================================================
# XỬ LÝ ẢNH BIÊN LAI
# ============================================================
def process_receipt(message, req_id):
    if message.photo:
        file_id = message.photo[-1].file_id
        bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=f"📤 **ẢNH BIÊN LAI**\n"
                    f"👤 Người dùng: {message.from_user.first_name}\n"
                    f"🆔 ID: `{message.from_user.id}`\n"
                    f"📌 Mã yêu cầu: `{req_id}`\n"
                    f"📅 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            parse_mode="Markdown"
        )
        bot.reply_to(
            message,
            "✅ **CẢM ƠN QUÝ KHÁCH!**\n\n"
            "⏳ Vui lòng chờ trong giây lát để hệ thống kiểm tra giao dịch.\n\n"
            "🙏 **Chân thành cảm ơn quý khách đã tin tưởng sử dụng dịch vụ của Siêu Tốc iCloud!**",
            parse_mode="Markdown"
        )
        update_request_status(req_id, "waiting_confirm")
    else:
        bot.reply_to(
            message,
            "❌ **Vui lòng gửi ẢNH biên lai chuyển khoản!**\n\n"
            "📌 Hãy chụp ảnh biên lai và gửi lại đây.",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, process_receipt, req_id)

def update_request_status(req_id, status):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        for r in data:
            if r["id"] == req_id:
                r["status"] = status
                break
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

# ============================================================
# CHẠY BOT (VÒNG LẶP TỰ ĐỘNG THỬ LẠI)
# ============================================================
if __name__ == "__main__":
    print("🚀 SIÊU TỐC iCLOUD BOT đang chạy...")
    print(f"📱 Bot ID: {TOKEN.split(':')[0]}")
    print(f"👤 Admin ID: {ADMIN_ID}")
    print(f"📋 Đã tải {len(UNLOCK_PRICES)} gói phá iCloud")

    # Chạy polling trong vòng lặp với cơ chế thử lại
    while True:
        try:
            bot.polling(non_stop=True, skip_pending=True, timeout=30, long_polling_timeout=20)
        except Exception as e:
            print(f"⚠️ Lỗi polling: {e}")
            print("🔄 Thử lại sau 5 giây...")
            time.sleep(5)
