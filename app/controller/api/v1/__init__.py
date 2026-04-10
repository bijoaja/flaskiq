import importlib.util
import os


def _load_module(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(filename, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_home    = _load_module("home.controller.py")
_chatbot = _load_module("chatbot.controller.py")
_docs    = _load_module("docs.controller.py")
_cms     = _load_module("cms.controller.py")

HomeResource        = _home.HomeResource
ChatbotResource     = _chatbot.ChatbotResource
ApiDocsResource     = _docs.ApiDocsResource
swaggerui_blueprint = _docs.swaggerui_blueprint
CmsListResource     = _cms.CmsListResource
CmsDetailResource   = _cms.CmsDetailResource

__all__ = [
    "HomeResource", "ChatbotResource", "ApiDocsResource",
    "swaggerui_blueprint", "CmsListResource", "CmsDetailResource"
]
