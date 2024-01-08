"""Init file of GitAddNB package
"""

from gitaddnb.add import gitaddnb

try:
    from gitaddnb._version import __version__
except ImportError:
    try:
        from setuptools_scm import get_version  # type: ignore

        __version__ = get_version()
    except (ImportError, LookupError) as e:
        __version__ = str(e)
