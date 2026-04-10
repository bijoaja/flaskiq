class HomeService:
    @staticmethod
    def get_context() -> dict:
        """Returns template context dict for the home page."""
        return {"name": "Template Flask"}
