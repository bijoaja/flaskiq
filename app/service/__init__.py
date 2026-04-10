import importlib.util
import os


def _load_module(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(filename, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_home = _load_module("home.service.py")
_cms  = _load_module("cms.service.py")

HomeService = _home.HomeService
CmsService  = _cms.CmsService

__all__ = ["HomeService", "CmsService"]
