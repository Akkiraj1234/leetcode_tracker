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
        message = f"Validation failed for '{name}' Validation."
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


class SQLiteVersionError(LeetSolverError):
    """Raised when the SQLite version is incompatible."""

    def __init__(self, current_version: str, required_version: str, *, cause: Optional[Exception] = None):
        message = (
            f"Incompatible SQLite version: '{current_version}'. "
            f"Required version: '{required_version}' or higher."
        )
        self.current_version = current_version
        self.required_version = required_version
        super().__init__(message, cause=cause)


class TableNotFoundError(LeetSolverError):
    """Raised when a required table is missing in the SQLite database."""

    def __init__(self, table_name: str, *, cause: Optional[Exception] = None):
        message = f"Table '{table_name}' is missing in the database."
        self.table_name = table_name
        super().__init__(message, cause=cause)


class ColumnMismatchError(LeetSolverError):
    """Raised when a column is missing or has a mismatched type in the SQLite database."""

    def __init__(self, table_name: str, column_name: str, expected_type: str, actual_type: Optional[str] = None, *, cause: Optional[Exception] = None):
        message = f"Column '{column_name}' in table '{table_name}' is missing or has a mismatched type."
        if actual_type:
            message += f" Expected: '{expected_type}', Found: '{actual_type}'."
        self.table_name = table_name
        self.column_name = column_name
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__(message, cause=cause)


class ConstraintValidationError(LeetSolverError):
    """Raised when a database constraint is violated."""

    def __init__(self, constraint: str, table_name: str, *, cause: Optional[Exception] = None):
        message = f"Constraint '{constraint}' violated in table '{table_name}'."
        self.constraint = constraint
        self.table_name = table_name
        super().__init__(message, cause=cause)


class JSONDecodeError(LeetSolverError):
    """Raised when a JSON file cannot be parsed."""

    def __init__(self, file_path: str, *, cause: Optional[Exception] = None):
        message = f"Failed to decode JSON file: '{file_path}'"
        self.file_path = file_path
        super().__init__(message, cause=cause)


class BackupError(LeetSolverError):
    """Raised when a backup operation fails."""

    def __init__(self, operation: str, target: str, *, cause: Optional[Exception] = None):
        message = f"Backup operation '{operation}' failed for target: '{target}'"
        self.operation = operation
        self.target = target
        super().__init__(message, cause=cause)


class PermissionErrorLS(LeetSolverError):
    """Raised when a file or directory has insufficient permissions."""

    def __init__(self, path: str, action: str, *, cause: Optional[Exception] = None):
        """
        Args:
            path (str): The path that caused the permission error.
            action (str): The action that failed (e.g., 'read', 'write', 'create').
            cause (Optional[Exception]): The underlying exception, if any.
        """
        message = (
            f"Permission error: Unable to {action} at path '{path}'. "
            "Please check the permissions or delete the file to continue."
        )
        self.path = path
        self.action = action
        super().__init__(message, cause=cause)

