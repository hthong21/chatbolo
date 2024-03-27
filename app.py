from flask import Flask, render_template, request
import google.generativeai as genai
from datetime import datetime
import markdown
from markupsafe import Markup  # Nhập thư viện markdown

app = Flask(__name__)

# Giả sử bạn đã cấu hình API_KEY ở đâu đó
API_KEY = 'YOUR_API_KEY'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    if question.strip().lower() == 'bye':
        response_text = "Goodbye!"
    elif question.strip().lower() == 'time':
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response_text = f"The current time is: {current_time}"
    else:
        response = chat.send_message(question)
        # Chuyển đổi Markdown sang HTML và đảm bảo Flask có thể hiển thị HTML an toàn
        html = markdown.markdown(response.text)
        response_text = Markup(html)
    # Trả về một chuỗi HTML an toàn được tạo từ Markdown
    return response_text

if __name__ == '__main__':
    app.run(debug=True)
