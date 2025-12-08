from app import app
import os
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    print(f"🚀 Starting server on port {os.getenv('FLASK_RUN_PORT', 8080)}")

    app.run(
        host="0.0.0.0",
        debug=os.getenv("FLASK_DEBUG", "False") == "TRUE",
        threaded=True,
        port=int(os.getenv("FLASK_RUN_PORT", 8080)),
    )
