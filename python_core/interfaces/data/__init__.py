"""Data access and data-shape interfaces."""

from python_core.interfaces.data.cache import Cache
from python_core.interfaces.data.query import Query
from python_core.interfaces.data.query_handler import QueryHandler
from python_core.interfaces.data.repository import Repository
from python_core.interfaces.data.serializer import Serializer

__all__ = ["Cache", "Query", "QueryHandler", "Repository", "Serializer"]
