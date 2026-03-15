# Simple Key-Value Store

## Project: CSCE4350 - Build a Database: The Simple Key-Value Store

- **EUID**: AJA0285
- **GitHub Username**: AishatAA

## Overview
A simple persistent key-value store implemented in Python that supports SET and GET commands using append-only storage.

## Features
- **SET <key> <value>**: Store a key-value pair
- **GET <key>**: Retrieve value for a key (returns "NULL" if not found)
- **EXIT**: Exit the program
- **Persistence**: All data is immediately written to `data.db` using append-only logging
- **Last-write-wins**: Latest SET for a key overwrites previous values
- **Custom index**: Uses list-based linear search (no dictionaries/maps)

## File Structure
- **main.py** - Main program Implementation
- **data.db** - Append-only storage
- **README.md** - Documentation
- **Gradebot_Screenshot_Prove.png** - Testing results

## How to Run
```bash
python3 main.py
