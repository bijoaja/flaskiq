from app.service.prompts import HomePrompts

if __name__ == "__main__":
    prompt = HomePrompts().home_prompt()
    print(prompt)