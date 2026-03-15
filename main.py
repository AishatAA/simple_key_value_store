#!/usr/bin/env python3
"""
Build a Database: The Simple Key-Value Store
CSCE4350 Project
EUID: AJA0285

A persistent key-value store using append-only logging.
Supports SET, GET, and EXIT commands via STDIN/STDOUT.
"""

import sys
import os


class SimpleKeyValueStore:
    """A key-value store with append-only persistence to disk."""
    
    def __init__(self, data_file="data.db"):
        """Initialize the store with a data file and empty index."""
        self.data_file = data_file
        self.index = []  # List of (key, value) tuples - no dictionaries!
        self.load_from_disk()  # Rebuild index from existing log on startup

    def start(self):
        """Main REPL loop: reads commands from STDIN and executes them."""
        while True:
            try:
                line = sys.stdin.readline().strip()
                if not line:  # EOF
                    break
                self.execute_command(line)
            except KeyboardInterrupt:
                break
            except Exception as e:
                # Use stderr for errors to avoid interfering with test output
                sys.stderr.write(f"Error: {e}\n")

    def execute_command(self, command_line):
        """
        Parse and execute a single command.
        Commands: SET <key> <value>, GET <key>, EXIT
        """
        parts = command_line.split()
        if not parts:
            return

        command = parts[0].upper()

        if command == "EXIT":
            sys.exit(0)
        elif command == "SET" and len(parts) == 3:
            self.set(parts[1], parts[2])
        elif command == "GET" and len(parts) == 2:
            result = self.get(parts[1])
            print(result)  # Only GET commands produce output
            sys.stdout.flush()  # Ensure output is sent immediately

    def append_to_log(self, key, value):
        """
        Append a SET operation to the log file.
        Uses flush and fsync for immediate persistence (required by spec).
        """
        try:
            with open(self.data_file, 'a') as f:
                f.write(f"SET {key} {value}\n")
                f.flush()           # Flush Python's internal buffers
                os.fsync(f.fileno())  # Force OS to write to disk
        except IOError as e:
            sys.stderr.write(f"Error writing to disk: {e}\n")

    def load_from_disk(self):
        """
        Rebuild in-memory index by replaying the log file on startup.
        This ensures data consistency after restarts.
        """
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("SET "):
                        parts = line.split(maxsplit=2)
                        if len(parts) == 3:
                            _, key, value = parts
                            self.update_index(key, value)
        except IOError as e:
            sys.stderr.write(f"Error reading from disk: {e}\n")

    def update_index(self, key, value):
        """
        Update the in-memory index with linear search.
        Implements "last write wins" by replacing existing keys.
        """
        # Linear search through list (no dictionaries allowed)
        for i, (k, v) in enumerate(self.index):
            if k == key:
                # Replaces existing key (last write wins)
                self.index[i] = (key, value)
                return
        # This line will append a new key to list
        self.index.append((key, value))

    def set(self, key, value):
        """
        SET command: persist to disk first, then update index.
        Returns nothing (per spec).
        """
        # This line wiil always write to disk first
        self.append_to_log(key, value)
        # This line will update in-memory index
        self.update_index(key, value)

    def get(self, key):
        """
        GET command: linear search through index.
        Returns value if found, empty string if not found (per Gradebot).
        """
        for k, v in self.index:
            if k == key:
                return v
        return ""  # Empty string for nonexistent keys


if __name__ == "__main__":
    """Entry point: create and start the key-value store."""
    store = SimpleKeyValueStore()
    store.start()
