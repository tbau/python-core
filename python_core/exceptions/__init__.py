"""Exception classes exported by python-core."""

from python_core.exceptions.base.python_core_error import PythonCoreError
from python_core.exceptions.common.configuration_error import ConfigurationError
from python_core.exceptions.common.conflict_error import ConflictError
from python_core.exceptions.common.not_found_error import NotFoundError
from python_core.exceptions.common.validation_error import ValidationError
from python_core.exceptions.integration.dependency_error import DependencyError
from python_core.exceptions.integration.external_api_error import ExternalApiError
from python_core.exceptions.integration.message_queue_error import MessageQueueError
from python_core.exceptions.integration.operation_timeout_error import OperationTimeoutError
from python_core.exceptions.integration.rate_limit_error import RateLimitError
from python_core.exceptions.integration.redis_error import RedisError
from python_core.exceptions.persistence.outbox_error import OutboxError
from python_core.exceptions.persistence.query_error import QueryError
from python_core.exceptions.persistence.repository_error import RepositoryError
from python_core.exceptions.persistence.transaction_error import TransactionError
from python_core.exceptions.reliability.idempotency_error import IdempotencyError
from python_core.exceptions.reliability.idempotency_required_error import IdempotencyRequiredError
from python_core.exceptions.reliability.retry_exhausted_error import RetryExhaustedError
from python_core.exceptions.security.authentication_error import AuthenticationError
from python_core.exceptions.security.authorization_error import AuthorizationError
from python_core.exceptions.web.middleware_error import MiddlewareError

__all__ = [
    "AuthenticationError",
    "AuthorizationError",
    "ConfigurationError",
    "ConflictError",
    "DependencyError",
    "ExternalApiError",
    "IdempotencyError",
    "IdempotencyRequiredError",
    "MessageQueueError",
    "MiddlewareError",
    "NotFoundError",
    "OperationTimeoutError",
    "OutboxError",
    "PythonCoreError",
    "QueryError",
    "RateLimitError",
    "RedisError",
    "RepositoryError",
    "RetryExhaustedError",
    "TransactionError",
    "ValidationError",
]
