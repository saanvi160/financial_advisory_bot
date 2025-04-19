import os
import fitz  # PyMuPDF for extracting text from PDFs
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai  # Using Gemini AI

# Set up Gemini API key
genai.configure(api_key="AIzaSyA7DrzBgrZkW-Za7itPE8VneZDCM69_L-Y")

# Initialize Flask app
app = Flask(__name__)

# Function to extract text from PDFs in the 'database' folder
def extract_text_from_pdfs(folder_path="D:/OneDrive/Desktop/financial bot/Project_Saadhna_2024/database"):
    """Extracts text from all PDFs in the given folder."""
    extracted_text = ""

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    extracted_text += page.get_text() + "\n"

    return extracted_text

# Extract financial data from PDFs
financial_data = extract_text_from_pdfs()

# Define the prompt template for Gemini AI
prompt_template = """You are an AI assistant that helps people with financial advice. The answer should be descriptive.

User Information:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: {monthly_income}
- Monthly Expenses: {monthly_expenses}
- Current Saving: {current_saving}
- Investment Goals: {investment_goals}
- Risk Tolerance: {risk_tolerance}
- Loan Term: {loan_term}
- Interest Rate: {interest_rate}
- Credit Score: {credit_score}

Financial Knowledge:
{financial_data}

Provide personalized loan advice based on the user's financial status and best financial practices.
"""

@app.route('/')
def index():
    return render_template('loan_advice.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    user_data = request.form.to_dict()
    prompt = create_prompt(user_data)
    advice = generate(prompt)
    
    if not advice.strip():
        advice = "I'm sorry, but I couldn't generate an answer. Please try again with more details."
    
    return jsonify({'advice': advice})

def create_prompt(user_data):
    """Format the prompt with user input and financial knowledge."""
    return prompt_template.format(**user_data, financial_data=financial_data[:2000])  # Limit to 2000 chars

def generate(prompt):
    """Generate response using Gemini AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])  # Wrap prompt in a list 
    if response and response.text:
        return response.text.strip()
    return "I'm sorry, but I couldn't generate an answer at this time."

if __name__ == '__main__':
    app.run(debug=True)
