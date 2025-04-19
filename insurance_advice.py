import os
import fitz  # Optional if you want to add PDFs later
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

# Set your Gemini API Key
genai.configure(api_key="AIzaSyA7DrzBgrZkW-Za7itPE8VneZDCM69_L-Y")  # saanvi's api key AIzaSyCHrrOY7suHCYlq9LNys0rNKwO9iKShtjA

app = Flask(__name__)

# 🧠 Prompt template for insurance advice
prompt_template = """You are an AI assistant that provides personalized insurance advice. Use the information below to analyze the user's profile and generate a detailed insurance recommendation.

User Information:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{monthly_income}
- Monthly Expenses: ₹{monthly_expenses}
- Current Savings: ₹{current_saving}
- Investment Goals: {investment_goals}
- Risk Tolerance (1–10): {risk_tolerance}
- Type of Financial Advice Needed: {advice_type}
- Current Financial Products: {current_financial_products}
- Existing Debts/Loans: {debts_loans}
- Details of Debts/Loans: {debts_loans_details}

Please provide insurance advice that fits the user’s financial profile, covering aspects like:
- Type of insurance (life, health, term, etc.)
- Suitable coverage amount
- Premium affordability
- Investment-linked or risk-free plans
"""

@app.route('/')
def index():
    return render_template('insurance_advice.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    user_data = request.form.to_dict()
    prompt = create_prompt(user_data)
    advice = generate(prompt)

    if not advice.strip():
        advice = "Sorry, I couldn't generate insurance advice at the moment. Please try again."

    return jsonify({'advice': advice})

def create_prompt(user_data):
    return prompt_template.format(**user_data)

def generate(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([prompt])
        if response and response.text:
            return response.text.strip()
        return "No response generated."
    except Exception as e:
        print("Error:", e)
        return "There was an error connecting to Gemini. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)
