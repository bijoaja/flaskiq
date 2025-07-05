from app import render_template

class ViewDashboard:

    @staticmethod
    def dashboard():
        return render_template("/home/dashboard.html", name="Template_flask")
