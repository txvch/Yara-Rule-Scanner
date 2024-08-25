# Yara Rule Scanner
Yara Rule Scanner is an open-source tool written in Python to ensure that your Yara rules work!

This scanner helps you test your Yara rules against specific executables like cheats, malware, suspicious files, or other patterns of interest.

## Features
**Open Source:** Fully available for customization and improvement.

**Simple Setup:** Requires only a .yar file and a target executable to start scanning.

**Efficient Scanning:** Best used for scanning a single folder or a specific set of files

## Getting Started
**Python:** Make sure you have Python installed on your computer.

**Yara:** Install Yara using pip if you don't have it already: pip install yara-python

## Setup
**Place the Python:** Make sure the Python code is in the same directory as your yara.yar

**Prepare Your Yara Rules:** Ensure you have a yara.yar file in the same directory where you're executing the Python script. This file should contain the Yara rules you want to test.

**Place the Executable:** Ensure the executable file (or files) you want to scan with your Yara rules is in a separate directory with minimum 300 files.

# Usage
Run the Python script to start scanning: py yara rule scanner.py

**Note:** To prevent performance issues, avoid scanning a large number of files. Scanning your Downloads folder or a flder with a maximum of 100,000 should be fine.

# Contributing
Feel free to open an issue or submit a pull request with your improvements. Whether it's a bug fix, a new feature, or better documentation, i appreciate your help.

# Contact
For questions or support, please contact technicallsupportt on discord!
