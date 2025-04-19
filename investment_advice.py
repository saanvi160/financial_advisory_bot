import os
import fitz  # PyMuPDF to read PDF
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# 🔐 Set your Gemini API key
genai.configure(api_key="AIzaSyA7DrzBgrZkW-Za7itPE8VneZDCM69_L-Y")

app = Flask(__name__)

# 📂 Load data from PDF database folder
def extract_text_from_pdfs(folder_path="D:/OneDrive/Desktop/financial bot/Project_Saadhna_2024/database"):
    text = ""
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            with fitz.open(os.path.join(folder_path, file)) as doc:
                for page in doc:
                    text += page.get_text() + "\n"
    return text

financial_data = extract_text_from_pdfs()

# 🧠 Prompt template for investment advice
prompt_template = """You are an AI assistant that helps users with investment advice. Use the provided financial knowledge and user input to give a personalized recommendation.

User Details:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Current Savings: ₹{current_saving}
- Investment Goals: {investment_goals}
- Risk Tolerance: {risk_tolerance}
- Time Horizon: {time_horizon}
- Preferred Investment Type: {investment_type}
- Amount Available for Investment: ₹{investment_amount}
- Other Investments: {other_investments}
- Expected Returns: {expected_returns}

Financial Knowledge:
{financial_data}

Please provide detailed investment advice for this user.
"""

@app.route('/')
def index():
    return render_template('investment_advice.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    user_data = request.form.to_dict()
    prompt = create_prompt(user_data)
    advice = generate(prompt)

    if not advice.strip():
        advice = "Sorry, I couldn't generate an investment recommendation. Please try again."

    return jsonify({'advice': advice})

def create_prompt(user_data):
    return prompt_template.format(**user_data, financial_data=financial_data[:2000])

def generate(prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])
    if response and response.text:
        return response.text.strip()
    return "No response generated."

if __name__ == '__main__':
    app.run(debug=True)
