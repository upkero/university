class FairError(Exception):
    """Base exception for fair management errors."""


class NotFoundError(FairError):
    """Raised when an entity is not found."""


class ValidationError(FairError):
    """Raised when a validation rule is violated."""


class ConflictError(FairError):
    """Raised when an operation conflicts with current state."""
