import ollama
import os
from dotenv import load_dotenv

load_dotenv()


class TokenBudgetChat:
    def __init__(self, model_name: str, system_prompt: str, max_messages: int = 4):
        """Manages conversation history using a programmatic Sliding Window."""
        self.model_name = model_name
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.max_messages = max_messages
        self.history = []

    def chat(self, user_input: str):
        print(f"User: {user_input}")
        self.history.append({"role": "user", "content": user_input})
        
        # Sliding Window: Remove oldest entries if the message budget is exceeded
        while len(self.history) > self.max_messages:
            removed = self.history.pop(0)
            print(f"[Memory Cleanup] Removed oldest entry: {removed['role'].upper()} - '{removed['content']}'")
            
        payload = [self.system_prompt] + self.history
        
        try:
            response = ollama.chat(model=os.getenv(self.model_name, "phi3:latest"), messages=payload)
            assistant_reply = response['message']['content']
            
            print(f"Bot: {assistant_reply}")
            print(f"[Memory Status] History size: {len(self.history) + 1}/{self.max_messages + 1} slots used\n" + "-"*40)
            
            self.history.append({"role": "assistant", "content": assistant_reply})
            return assistant_reply
            
        except Exception as e:
            return f"Chat error: {str(e)}"


if __name__ == "__main__":
    SYSTEM_PROMPT = "You are an impatient bot."
    
    bot = TokenBudgetChat(model_name='phi3:latest', system_prompt=SYSTEM_PROMPT, max_messages=4)
    print("Execution started. Tracking history budget:\n" + "="*40)

    bot.chat("Hello.")
    bot.chat("How is the weather today?")
    # Exceeds the 4-message history limit. Watch the first turn drop out.
    bot.chat("How do I get maximal muscle strength?")
    bot.chat("Where is Paris located?")