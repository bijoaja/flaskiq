from app import render_template

class ViewHome:
    @staticmethod
    def home():
        
        return render_template("home/index.html", name="Template Flask")
