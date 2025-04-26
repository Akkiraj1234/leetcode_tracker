from typing import Optional


class LeetSolverError(Exception):
    """Base exception for all errors in the LeetSolver application."""

    def __init__(self, message: str, *, cause: Optional[Exception] = None):
        self.message = message
        self.cause = cause
        super().__init__(message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message!r}, cause={self.cause!r})"


class DirectoryNotFoundError(LeetSolverError):
    """Raised when the required directory is not found."""

    def __init__(self, path: str, *, cause: Optional[Exception] = None):
        message = f"Required directory not found: '{path}'"
        self.path = path
        super().__init__(message, cause=cause)


class ValidationError(LeetSolverError):
    """Raised when a file or folder fails validation and cannot be auto-fixed."""

    def __init__(self, name: str, reason: Optional[str] = None, *, cause: Optional[Exception] = None):
        message = f"Validation failed for '{name}'."
        if reason:
            message += f" Reason: {reason}"
        self.name = name
        self.reason = reason
        super().__init__(message, cause=cause)


class FileCreationError(LeetSolverError):
    """Raised when a file cannot be created."""

    def __init__(self, file_path: str, *, cause: Optional[Exception] = None):
        message = f"Failed to create file: '{file_path}'"
        self.file_path = file_path
        super().__init__(message, cause=cause)


class DatabaseConnectionError(LeetSolverError):
    """Raised when the SQLite database fails to connect."""

    def __init__(self, db_path: str, *, cause: Optional[Exception] = None):
        message = f"Could not connect to database at: '{db_path}'"
        self.db_path = db_path
        super().__init__(message, cause=cause)


class SchemaMismatchError(LeetSolverError):
    """Raised when a file does not match the required schema."""

    def __init__(self, file_name: str, expected_schema: str, *, cause: Optional[Exception] = None):
        message = (
            f"Schema mismatch in file '{file_name}'. Expected schema: '{expected_schema}'"
        )
        self.file_name = file_name
        self.expected_schema = expected_schema
        super().__init__(message, cause=cause)


class FolderValidationError(LeetSolverError):
    """Raised when a required folder is missing or invalid."""

    def __init__(self, folder_name: str, *, cause: Optional[Exception] = None):
        message = f"Folder validation failed or missing: '{folder_name}'"
        self.folder_name = folder_name
        super().__init__(message, cause=cause)
