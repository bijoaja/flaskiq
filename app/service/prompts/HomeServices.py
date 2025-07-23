class HomePrompts:
    def __init__(self):
        self.readme = self.load_readme()
    
    def load_readme(self, path="README.md"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "README.md tidak ditemukan."

    
    
    def home_prompt(self, data: dict = None):
        system_prompt = f"""
Anda adalah Asisten FlaskIQ yang bersedia memberikan jawaban terkait FlaskIQ. Pastikan anda memberikan jawaban menggunakan bahasa Indonesia yang baik dan benar.
Berikut penjelasan tenant FlaskIQ:
{self.readme}
        """
        
        return {"role": "system", "content": system_prompt}