import os
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

class GeminiWrapper:
    """A wrapper class for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        Args:
            api_key: Optional API key. If not provided, will look for GEMINI_API_KEY in environment.
        """
        # Load environment variables from .env file if present
        load_dotenv()
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in environment as GEMINI_API_KEY")
            
        # Configure the client
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from Gemini.
        Args:
            prompt: The input prompt for generation
        Returns:
            The generated response text
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
        

    def extract_medical_keyword(self, text: str) -> str:
        prompt = f"""
        Extract the most important single medical keyword from the following English text.
        Provide the answer in Korean only. Do not include any English or additional explanations.
        Just return one Korean medical term.
        
        Text: {text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"키워드 추출 중 오류 발생: {str(e)}")

def main():
    """Example usage of the GeminiWrapper class."""
    try:
        # Initialize the wrapper
        gemini = GeminiWrapper()
        
        # Example prompt
        prompt = "안녕하세요"
        
        # Generate and print response
        response = gemini.generate_response(prompt)
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()