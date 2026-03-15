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
        self.data_file = data_file
        self.index = []
        self.load_from_disk()

    def start(self):
        while True:
            try:
                line = sys.stdin.readline().strip()
                if not line:
                    break
                self.execute_command(line)
            except KeyboardInterrupt:
                break
            except Exception as e:
                sys.stderr.write(f"Error: {e}\n")

    def execute_command(self, command_line):
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
            print(result)
            sys.stdout.flush()

    def append_to_log(self, key, value):
        try:
            with open(self.data_file, 'a') as f:
                f.write(f"SET {key} {value}\n")
                f.flush()
                os.fsync(f.fileno())
        except IOError as e:
            sys.stderr.write(f"Error writing to disk: {e}\n")

    def load_from_disk(self):
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
        for i, (k, v) in enumerate(self.index):
            if k == key:
                self.index[i] = (key, value)
                return
        self.index.append((key, value))

    def set(self, key, value):
        self.append_to_log(key, value)
        self.update_index(key, value)

    def get(self, key):
        for k, v in self.index:
            if k == key:
                return v
        return "NULL"


if __name__ == "__main__":
    store = SimpleKeyValueStore()
    store.start()
