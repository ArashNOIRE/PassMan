
# PassMan

A simple command-line password manager written in Python for storing, generating, and managing website passwords.

## Overview

PassMan provides a minimal interface to:
- Create and verify a master password.
- Store passwords locally.
- Generate passwords with configurable options (numbers, symbols, uppercase, lowercase, length).
- Perform basic CRUD operations on stored passwords (add, remove, rename, change, list, search).

This project is intended as a small educational example — not a production-ready secure password manager.

## Contents

- `main.py` — CLI entry point and main program flow (master password management, CRUD operations).
- `PassGen.py` — password generator (controls for numbers, symbols, uppercase, lowercase, length).
- `Pass2File.py` — file I/O for saving/loading passwords, hashing and integrity checks.

## Requirements

- Python 3.7 or newer

## Installation & Running

1. Clone the repository:
   ```
   git clone https://github.com/ArashNOIRE/PassMan.git
   cd PassMan
   ```

2. Run the program:
   ```
   python main.py
   ```

On the first run you will be prompted to set a master password. The program will create a `master.key` file in the project directory.

## Usage

When you start the program and pass master verification, you can choose one of the following actions:

- `add` — Add a new website and password (option to generate a password).
- `remove` — Remove a website and its password.
- `see` — Show all stored passwords (asks for confirmation).
- `rename` — Rename a website entry (key).
- `change` — Change the password for a website.
- `search` — Search for a website and display its password.
- `exit` — Exit the program.

Example "add" flow (interactive):
```
What do you want to do? (add, remove, see, rename, change, search, exit): add
Enter website: example.com
Generate password? (y/n): y
Include numbers? (y/n): y
Include symbols? (y/n): n
Include uppercase letters? (y/n): y
Include lowercase letters? (y/n): y
Enter password length: 12
Password: Ab3dE4fG5h6j for example.com added.
```

## Files created by the app

- `master.key` — contains the hashed master password and other integrity-related lines.
- Additional files managed by `Pass2File.py` (names depend on constants like `KEY_FILE`, `PASS_FILE` inside that module).

## Security considerations (important)

This project is a simple example and not intended for production use. Important security improvements to consider before using it for real secrets:

- Use a strong, memory-hard KDF (e.g., PBKDF2, scrypt, or Argon2) with a salt when hashing the master password.
- Never store passwords in plain text on disk. Encrypt stored passwords using a key derived from the master password.
- Protect files with appropriate filesystem permissions.
- Consider using well-audited libraries (e.g., cryptography) for encryption primitives rather than homegrown crypto.
- Add secure handling to avoid exposing secrets in logs or via process arguments.

## Contributing

Contributions are welcome. Suggestions and improvements might include:
- Encrypting password storage.
- Using a secure key derivation function with salt.
- Adding export/import (CSV) with encryption.
- Building a GUI or TUI for easier use.
- Adding unit tests and CI checks.

Please open an issue to discuss larger changes before submitting a pull request.

## License

No license file included in the repository currently. If you'd like an open-source license (for example, MIT), add a `LICENSE` file and update this README.

## Contact

If you have questions or want to propose changes, open an issue in the repository.
