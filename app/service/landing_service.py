class LandingService:

    API_ROUTES = [
        {"method": "GET",    "path": "/api/v1/",                  "description": "Welcome message",              "auth": False},
        {"method": "POST",   "path": "/api/v1/auth/register",     "description": "Register a new user",         "auth": False},
        {"method": "POST",   "path": "/api/v1/auth/login",        "description": "Authenticate and get JWT",    "auth": False},
        {"method": "POST",   "path": "/api/v1/chatbot",           "description": "Streaming AI chatbot",        "auth": False},
        {"method": "GET",    "path": "/api/v1/cms",               "description": "List CMS pages",              "auth": False},
        {"method": "POST",   "path": "/api/v1/cms",               "description": "Create a CMS page",          "auth": True},
        {"method": "GET",    "path": "/api/v1/cms/<id>",          "description": "Get page by ID",              "auth": False},
        {"method": "PUT",    "path": "/api/v1/cms/<id>",          "description": "Update a page",              "auth": True},
        {"method": "DELETE", "path": "/api/v1/cms/<id>",          "description": "Delete a page",              "auth": True},
        {"method": "GET",    "path": "/api/v1/docs",              "description": "Swagger UI",                  "auth": False},
    ]

    @staticmethod
    def get_context() -> dict:
        return {
            "name":        "FlaskIQ",
            "version":     "2.0.0",
            "description": "A structured Flask template — JWT auth, CMS, AI chatbot, REST API, Swagger.",
            "swagger_url": "/api/v1/docs",
            "cms_url":     "/cms",
            "api_routes":  LandingService.API_ROUTES,
        }
