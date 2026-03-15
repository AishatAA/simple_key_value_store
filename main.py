#!/usr/bin/env python3
"""
Build a Database: The Simple Key-Value Store
CSCE4350 Project
EUID: AJA0285
"""

import sys
import os

class SimpleKeyValueStore:
    def __init__(self, data_file="data.db"):
        """Initialize the key-value store"""
        self.data_file = data_file
        self.index = []  # Simple list-based index (no dictionaries!)
        
        # Load existing data on startup
        self.load_from_disk()
    
    def start(self):
        """Start the REPL (Read-Eval-Print Loop)"""
        print("Simple KV Store started. Type SET, GET, or EXIT")
        
        while True:
            try:
                # Read command from stdin
                line = sys.stdin.readline().strip()
                if not line:  # EOF
                    break
                    
                # Parse and execute command
                response = self.execute_command(line)
                if response is not None:
                    print(response)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def execute_command(self, command_line):
        """Parse and execute a command"""
        parts = command_line.split()
        if not parts:
            return None
            
        command = parts[0].upper()
        
        if command == "EXIT":
            sys.exit(0)
        elif command == "SET" and len(parts) == 3:
            return self.set(parts[1], parts[2])
        elif command == "GET" and len(parts) == 2:
            return self.get(parts[1])
        else:
            return "Invalid command"
    
    def append_to_log(self, key, value):
        """Append a SET operation to the log file"""
        try:
            with open(self.data_file, 'a') as f:
                # Format: SET key value
                f.write(f"SET {key} {value}\n")
                f.flush()  # Ensure it's written to disk
                os.fsync(f.fileno())  # Force write to disk
        except IOError as e:
            print(f"Error writing to disk: {e}")
    
    def load_from_disk(self):
        """Load data from disk on startup"""
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
            print(f"Error reading from disk: {e}")
    
    def update_index(self, key, value):
        """Update the in-memory index"""
        # Linear search through the list
        for i, (k, v) in enumerate(self.index):
            if k == key:
                # Update existing key
                self.index[i] = (key, value)
                return
        
        # Add new key-value pair
        self.index.append((key, value))
    
    def set(self, key, value):
        """SET command implementation"""
        # First, persist to disk
        self.append_to_log(key, value)
        
        # Then update in-memory index
        self.update_index(key, value)
        
        return None  # No output for SET commands
    
    def get(self, key):
        """GET command implementation"""
        # Linear search through the index
        for k, v in self.index:
            if k == key:
                return v
        
        # Key not found
        return "NULL"

if __name__ == "__main__":
    store = SimpleKeyValueStore()
    store.start()
