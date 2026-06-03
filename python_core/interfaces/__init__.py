"""Small, stable interfaces for application code and adapters.

Import interfaces from their grouped, class-named modules, for example:

```python
from python_core.interfaces.data.repository import Repository
from python_core.interfaces.application.facade import Facade
```

Grouped imports are preferred in new code, but common interfaces are also
exported here for convenience.
"""

from python_core.interfaces.application.facade import Facade
from python_core.interfaces.application.service import Service
from python_core.interfaces.auth.authenticator import Authenticator
from python_core.interfaces.auth.authorizer import Authorizer
from python_core.interfaces.auth.ownership_checker import OwnershipChecker
from python_core.interfaces.auth.password_hasher import PasswordHasher
from python_core.interfaces.auth.token_issuer import TokenIssuer
from python_core.interfaces.auth.token_verifier import TokenVerifier
from python_core.interfaces.data.cache import Cache
from python_core.interfaces.data.query import Query
from python_core.interfaces.data.query_handler import QueryHandler
from python_core.interfaces.data.repository import Repository
from python_core.interfaces.data.serializer import Serializer
from python_core.interfaces.database.database_connector import DatabaseConnector
from python_core.interfaces.database.transaction import Transaction
from python_core.interfaces.database.unit_of_work import UnitOfWork
from python_core.interfaces.files.file_parser import FileParser
from python_core.interfaces.files.file_writer import FileWriter
from python_core.interfaces.files.spreadsheet_writer import SpreadsheetWriter
from python_core.interfaces.integration.external_api_client import ExternalApiClient
from python_core.interfaces.integration.message_handler import MessageHandler
from python_core.interfaces.integration.message_publisher import MessagePublisher
from python_core.interfaces.integration.outbox import Outbox
from python_core.interfaces.integration.redis_client import RedisClient
from python_core.interfaces.middleware.middleware import Middleware
from python_core.interfaces.observability.event_logger import EventLogger
from python_core.interfaces.observability.exception_handler import ExceptionHandler
from python_core.interfaces.observability.exception_reporter import ExceptionReporter

__all__ = [
    "Cache",
    "Authenticator",
    "Authorizer",
    "DatabaseConnector",
    "EventLogger",
    "ExceptionHandler",
    "ExceptionReporter",
    "ExternalApiClient",
    "Facade",
    "FileParser",
    "FileWriter",
    "MessageHandler",
    "MessagePublisher",
    "Middleware",
    "OwnershipChecker",
    "PasswordHasher",
    "Outbox",
    "Query",
    "QueryHandler",
    "RedisClient",
    "Repository",
    "Serializer",
    "Service",
    "SpreadsheetWriter",
    "TokenIssuer",
    "TokenVerifier",
    "Transaction",
    "UnitOfWork",
]
