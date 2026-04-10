import importlib.util
import os


def _load_module(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(filename, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_home    = _load_module("home.service.py")
_chatbot = _load_module("chatbot.service.py")
_docs    = _load_module("docs.service.py")
_cms     = _load_module("cms.service.py")

HomeApiService  = _home.HomeApiService
ChatbotService  = _chatbot.ChatbotService
DocsApiService  = _docs.DocsApiService
CmsApiService   = _cms.CmsApiService

__all__ = ["HomeApiService", "ChatbotService", "DocsApiService", "CmsApiService"]
