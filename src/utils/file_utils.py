"""File utility functions for reading and validating text files."""

import os
from pathlib import Path
from typing import Optional


def read_text_file(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """
    Read a text file with error handling.
    
    Args:
        file_path: Path to the text file
        encoding: File encoding (default: utf-8)
    
    Returns:
        File content as string, or None if error
    """
    try:
        # Try primary encoding
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    
    except UnicodeDecodeError:
        # Try alternative encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        
        for alt_encoding in encodings:
            try:
                with open(file_path, 'r', encoding=alt_encoding) as file:
                    return file.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
    
    except (IOError, OSError, FileNotFoundError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
    print(f"Could not decode file {file_path} with any encoding")
    return None


def validate_file(file_path: Path, max_size_mb: int = 10) -> bool:
    """
    Validate that a file exists and is within size limits.
    
    Args:
        file_path: Path to the file
        max_size_mb: Maximum file size in MB
    
    Returns:
        True if file is valid, False otherwise
    """
    try:
        if not file_path.exists():
            return False
        
        if not file_path.is_file():
            return False
        
        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            print(f"File {file_path} is too large: {file_size_mb:.2f}MB > {max_size_mb}MB")
            return False
        
        return True
    
    except (OSError, IOError):
        return False


def ensure_directory_exists(directory_path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory
    """
    directory_path.mkdir(parents=True, exist_ok=True)


def get_file_stats(file_path: Path) -> dict:
    """
    Get basic statistics about a file.
    
    Args:
        file_path: Path to the file
    
    Returns:
        Dictionary with file statistics
    """
    try:
        stat = file_path.stat()
        return {
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified_time': stat.st_mtime,
            'created_time': stat.st_ctime
        }
    except (OSError, IOError):
        return {
            'size_bytes': 0,
            'size_mb': 0,
            'modified_time': 0,
            'created_time': 0
        }