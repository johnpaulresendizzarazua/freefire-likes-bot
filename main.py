import os
import requests
import telebot

# 1. Inicializar el bot con el token seguro de Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Error: La variable BOT_TOKEN no está configurada.")

bot = telebot.TeleBot(BOT_TOKEN)

# 2. Comando /start
@bot.message_handler(commands=['start', 'ayuda'])
def send_welcome(message):
    welcome_text = (
        "¡Hola! Bienvenido al Bot de Likes para Free Fire. 🎮🔥\n\n"
        "Para enviar likes a tu perfil, usa el comando `/like` seguido de tu ID.\n"
        "Ejemplo:\n"
        "`/like 123456789`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# 3. Comando /like
@bot.message_handler(commands=['like'])
def handle_like_request(message):
    command_parts = message.text.split()
    
    if len(command_parts) < 2:
        bot.reply_to(message, "❌ Por favor, proporciona tu ID de Free Fire.\nEjemplo: `/like 123456789`", parse_mode="Markdown")
        return
    
    player_id = command_parts[1]
    
    if not player_id.isdigit():
        bot.reply_to(message, "❌ El ID debe contener solo números.")
        return
    
    bot.reply_to(message, f"⏳ Procesando envío de likes para el ID: *{player_id}*... Por favor espera.", parse_mode="Markdown")
    
    # URL simulada de la API de la comunidad (Cambiar por una activa si tienes el endpoint)
    API_URL = f"https://api.ejemplo-comunidad.com/ff/likes?id={player_id}&region=WD"
    
    try:
        response = requests.get(API_URL, timeout=15)
        if response.status_code == 200:
            bot.reply_to(message, f"✅ ¡Likes enviados con éxito al ID *{player_id}*!", parse_mode="Markdown")
        else:
            bot.reply_to(message, "⚠️ La API externa está saturada. Inténtalo de nuevo más tarde.")
    except requests.exceptions.RequestException:
        bot.reply_to(message, "❌ Error de conexión al procesar los likes.")

if __name__ == "__main__":
    print("Bot encendido exitosamente...")
    bot.infinity_polling()
