import importlib.util
import os


def _load_module(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    spec = importlib.util.spec_from_file_location(filename, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cms = _load_module("cms.controller.py")

CmsView = _cms.CmsView

__all__ = ["CmsView"]
