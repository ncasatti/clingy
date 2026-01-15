"""Statistics tracking for operations"""

import time
from typing import List


class OperationStats:
    """Track statistics for build/zip operations"""

    def __init__(self):
        self.total_functions = 0
        self.successful = 0
        self.failed = 0
        self.start_time = 0
        self.failed_functions: List[str] = []

    def reset(self):
        """Reset all statistics"""
        self.total_functions = 0
        self.successful = 0
        self.failed = 0
        self.start_time = time.time()
        self.failed_functions = []

    def add_success(self):
        """Increment successful count"""
        self.successful += 1

    def add_failure(self, function_name: str):
        """Increment failure count and track function name"""
        self.failed += 1
        self.failed_functions.append(function_name)

    def get_duration(self) -> float:
        """Get operation duration in seconds"""
        return time.time() - self.start_time

    def get_success_rate(self) -> float:
        """Get success rate as percentage"""
        if self.total_functions == 0:
            return 0.0
        return (self.successful / self.total_functions) * 100


# Global stats instance
stats = OperationStats()
