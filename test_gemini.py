"""Test Gemini AI integration."""
import google.generativeai as genai
from config import get_settings

settings = get_settings()

print("Testing Gemini API directly...")
print(f"API Key: {settings.GEMINI_API_KEY[:20]}...")

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    print("\n✅ Gemini configured successfully")
    print("🧪 Sending test prompt...")
    
    response = model.generate_content("Write a one-sentence summary about India's technology sector.")
    
    print(f"\n✅ Response received!")
    print(f"Text: {response.text}")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"Details: {str(e)}")

