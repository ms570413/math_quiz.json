import json
import matplotlib.pyplot as plt
import telebot
import os

# Ab hum direct token nahi likhenge, GitHub Secrets se mangwayenge
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def create_math_image(text, filename="math_temp.png"):
    """Ye function text/math ko padh kar ek safed background wali image banayega"""
    fig = plt.figure(figsize=(8, 4))
    
    # Text ko image par likhna
    fig.text(0.05, 0.5, text, fontsize=16, va='center', ha='left')
    
    # Axes (graph lines) ko hide karna
    plt.axis('off')
    
    # Image ko save karna
    plt.savefig(filename, bbox_inches='tight', dpi=300, facecolor='white')
    plt.close()

def send_quiz():
    # 1. JSON file ko load karna
    with open('math_quiz.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Har question ko process karna
    for item in data['quiz']:
        print(f"Sending Question {item['id']}...")
        
        # Question aur options ko ek format mein joddna
        full_text = f"Question {item['id']}:\n{item['question']}\n\n"
        full_text += f"(A) {item['options'][0]}\n"
        full_text += f"(B) {item['options'][1]}\n"
        full_text += f"(C) {item['options'][2]}\n"
        full_text += f"(D) {item['options'][3]}"
        
        # Image banana
        image_path = "math_temp.png"
        create_math_image(full_text, image_path)
        
        # 3. Telegram par image bhejna
        with open(image_path, "rb") as photo:
            bot.send_photo(CHAT_ID, photo)
            
        # 4. Telegram par inbuilt Quiz/Poll bhejna (jisme student click kar sake)
        # 'A' ka index 0 hota hai, 'B' ka 1, etc.
        correct_index = ord(item['correct_option']) - 65 
        
        bot.send_poll(
            chat_id=CHAT_ID,
            question="Choose the correct option:",
            options=["Option A", "Option B", "Option C", "Option D"],
            type="quiz",
            correct_option_id=correct_index,
            is_anonymous=False
        )
        
        # Image bhejkar delete kar dena taaki kachra jama na ho
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == "__main__":
    print("Bot start ho raha hai...")
    send_quiz()
    print("Saare questions bhej diye gaye!")
