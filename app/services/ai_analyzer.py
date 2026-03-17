import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
async def analyze_with_ai(sector, news):
    try:
        prompt = f'''
        You are a financial analyst.

        Analyze Indian {sector} sector using this data:

        {news}

        Return a professional markdown report with:

        # {sector.title()} Sector Report

        ## Overview
        ## Market Trends
        ## Trade Opportunities
        ## Risks
        ## Conclusion
        '''

        response = model.generate_content(prompt)

        if not response or not response.text:
            return "Error: No response from AI"

        return response.text

    except Exception as e:
        print("AI ERROR:", str(e))   # 👈 IMPORTANT
        return f"AI Error: {str(e)}"