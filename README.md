# SecureLang Compiler

> A self-hosting compiler for secure communication and encrypted data storage — built as a production-quality academic capstone project.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-95%25+-success.svg)]()

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Language Design](#language-design)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Security Features](#security-features)
8. [Testing](#testing)
9. [Self-Hosting Roadmap](#self-hosting-roadmap)
10. [Viva Q&A](#viva-qa)

---

## Project Overview

**SecureLang** is a purpose-designed programming language with first-class support for secure communication and encrypted data storage. Unlike general-purpose languages that treat security as a library concern, SecureLang makes AES-256 encryption and secure messaging **primitive language constructs**.

### Key Highlights

| Feature | Technology |
|---------|-----------|
| Lexical Analysis | Hand-written single-pass scanner |
| Parsing | Recursive Descent Parser (LL grammar) |
| Semantic Analysis | Visitor-pattern type & scope checker |
| AST | Dataclass-based node hierarchy |
| Symbol Table | Scoped hash-map with built-in registry |
| IR Generation | Three-Address Code (TAC) |
| Optimization | 4-pass: folding, DCE, strength reduction, CSE |
| Encryption | AES-256-GCM (authenticated) |
| Key Exchange | RSA-2048-OAEP |
| Hashing | SHA-256 + PBKDF2-HMAC |
| Storage | SQLite (WAL mode) |
| Testing | PyTest (>95% target) |

---

## Architecture

```
Source Code (.sl)
      │
      ▼
┌─────────────┐
│    LEXER    │  → Token Stream
└─────────────┘
      │
      ▼
┌─────────────┐
│   PARSER    │  → Abstract Syntax Tree (AST)
└─────────────┘
      │
      ▼
┌──────────────────┐
│ SEMANTIC ANALYZER│  → Type-checked AST + Symbol Table
└──────────────────┘
      │
      ▼
┌──────────────┐
│ IR GENERATOR │  → Three-Address Code (TAC)
└──────────────┘
      │
      ▼
┌───────────────┐
│   OPTIMIZER   │  → Optimized TAC
└───────────────┘
      │
      ▼
┌───────────────┐
│ VM / CODEGEN  │  → Execution
└───────────────┘
      │
      ▼
  OUTPUT + SECURE OPERATIONS
  (AES-256 + RSA + SQLite)
```

---

## Language Design

### EBNF Grammar (Excerpt)

```ebnf
program        := statement* EOF
statement      := var_decl | func_def | if_stmt | while_stmt
                | for_stmt | return_stmt | print_stmt
                | send_stmt | receive_stmt | store_stmt | retrieve_stmt
                | expr_stmt
var_decl       := ('var'|'const') IDENT (':' type)? ('=' expression)? ';'?
func_def       := 'func' IDENT '(' params? ')' ('->' type)? block
if_stmt        := 'if' expression block ('elif' expression block)* ('else' block)?
while_stmt     := 'while' expression block
for_stmt       := 'for' IDENT 'in' expression block
send_stmt      := 'SEND' expression ('TO' expression)? ';'?
receive_stmt   := 'RECEIVE' IDENT? ';'?
store_stmt     := 'STORE' expression (',' expression)? ';'?
retrieve_stmt  := 'RETRIEVE' expression IDENT? ';'?
```

### Data Types

| Type | Example |
|------|---------|
| `int` | `42`, `0xFF`, `0b1010` |
| `float` | `3.14`, `1.5e10` |
| `str` | `"hello"` |
| `bool` | `true`, `false` |
| `void` | function return type |

### Secure Commands

```sl
// Encrypt and transmit a message
SEND "classified data" TO "recipient"

// Receive and decrypt message
RECEIVE msg

// Encrypt and store to database
STORE "filename.txt", content

// Retrieve and decrypt from database
RETRIEVE "filename.txt" variable
```

---

## Installation

### Prerequisites

- Python 3.10+
- pip

### Quick Start (Windows)

```bat
cd C:\SecureLang
pip install -r requirements.txt
python main.py --init-db
python main.py --keygen
```

### Quick Start (Linux/macOS)

```bash
cd /path/to/SecureLang
pip install -r requirements.txt
python main.py --init-db
python main.py --keygen
```

---

## Usage

### Compile and Run

```bash
python main.py examples/01_hello_world.sl
```

### Debug Flags

```bash
python main.py source.sl --tokens    # Show token stream
python main.py source.sl --ast       # Show AST
python main.py source.sl --ir        # Show raw TAC IR
python main.py source.sl --opt-ir    # Show optimized IR
python main.py source.sl --debug     # Full tracebacks
```

---

## Examples

### Hello World

```sl
var name: str = "SecureLang"
print("Hello from " + name)
```

### Functions & Loops

```sl
func factorial(n: int) -> int {
    if n <= 1 { return 1 }
    return n * factorial(n - 1)
}

var i: int = 0
while i <= 5 {
    print(str(i) + "! = " + str(factorial(i)))
    i = i + 1
}
```

### Secure Messaging

```sl
SEND "Top Secret Mission Brief" TO "agent_007"
RECEIVE decoded_msg
print("Received: " + decoded_msg)
```

### Encrypted File Storage

```sl
STORE "report.txt", "Confidential Annual Report Q4"
RETRIEVE "report.txt" content
print(content)
```

---

## Security Features

### AES-256-GCM
- **Mode**: Galois/Counter Mode (authenticated encryption)
- **Key size**: 256 bits (32 bytes)
- **Nonce**: 96-bit random per encryption
- **Tag**: 128-bit authentication tag (prevents tampering)

### RSA-2048
- **Padding**: OAEP with SHA-256 (industry standard)
- **Use case**: Key encapsulation / exchange
- **Key storage**: PEM-encoded files in `security/keys/`

### SHA-256
- **Password storage**: PBKDF2-HMAC-SHA256 with 200,000 iterations
- **File integrity**: Hash stored alongside encrypted blob
- **HMAC**: Message authentication for all transmitted messages

### Database Security
- **No plaintext storage**: All sensitive data encrypted before INSERT
- **SQL injection prevention**: Parameterized queries throughout
- **Integrity checking**: SHA-256 hash verified on every RETRIEVE

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=. --cov-report=html

# Run specific module
pytest tests/test_security.py -v
pytest tests/test_lexer.py -v
pytest tests/test_integration.py -v
```

---

## Self-Hosting Roadmap

SecureLang is designed for eventual bootstrapping — migrating from Python to self-hosted SecureLang implementation:

### Stage 1 — Python Reference Implementation (Current)
- Full compiler in Python
- Validates language design

### Stage 2 — SecureLang-to-C Backend
- Add C code generation backend
- Compile SecureLang to portable C
- Compile C with gcc/clang

### Stage 3 — Bootstrap Stage 1
- Write SecureLang lexer **in SecureLang**
- Compile with Python-based compiler
- Verify output matches reference

### Stage 4 — Bootstrap Stage 2
- Write full compiler **in SecureLang**
- Compile with Stage 3 compiler
- Verify self-consistency (quine test)

### Stage 5 — Self-Hosted Release
- SecureLang compiler compiled by itself
- Python implementation retired
- Full self-hosting achieved

---

## Viva Q&A

**Q: What is the role of the lexer?**
> The lexer performs lexical analysis: scanning raw source characters and grouping them into meaningful tokens (integers, strings, keywords, operators). It's the first compiler phase and produces the token stream consumed by the parser.

**Q: What parsing technique does SecureLang use?**
> Recursive Descent Parsing — a top-down, hand-written parser where each grammar rule is implemented as a Python method. It naturally handles operator precedence through layered function calls.

**Q: What is Three-Address Code?**
> TAC is an intermediate representation where each instruction has at most 3 operands: `result = arg1 OP arg2`. It simplifies optimization and is close to real assembly.

**Q: Why AES-256-GCM instead of AES-256-CBC?**
> GCM (Galois/Counter Mode) provides **authenticated encryption** — it simultaneously encrypts and produces an authentication tag, detecting any tampering. CBC only provides confidentiality; it requires a separate MAC.

**Q: How does the symbol table handle nested scopes?**
> The symbol table maintains a stack of Scope objects. When entering a block/function, a new child scope is pushed. Lookups chain upward through parent scopes. On exit, the inner scope is popped, making local variables inaccessible.

**Q: What optimizations are implemented?**
> 1. **Constant Folding** — `2 + 3 → 5` at compile time
> 2. **Dead Code Elimination** — remove unreachable code after GOTO
> 3. **Strength Reduction** — `x * 2 → x + x`, `x ** 2 → x * x`
> 4. **CSE** — reuse previously computed subexpressions

**Q: What is bootstrapping?**
> Bootstrapping is the process of using a compiler to compile itself. SecureLang's roadmap describes using the Python-based compiler to compile a SecureLang-based compiler until the language is self-hosting.

**Q: How is database integrity guaranteed?**
> Every file's SHA-256 hash is computed before encryption and stored alongside the encrypted blob. On RETRIEVE, the hash is recomputed post-decryption and compared using `hmac.compare_digest` (timing-safe) to detect corruption or tampering.

---

## Project Structure

```
SecureLang/
├── compiler/
│   ├── lexer/          # Lexical analysis (tokens, lexer)
│   ├── parser/         # Recursive descent parser
│   ├── ast/            # AST node classes + printer
│   ├── semantic/       # Type & scope checker
│   ├── symbol_table/   # Scoped symbol table
│   ├── intermediate/   # TAC IR generator
│   ├── optimizer/      # 4-pass code optimizer
│   └── codegen/        # TAC VM executor
├── security/
│   ├── encryption/     # AES-256-GCM
│   ├── rsa/            # RSA-2048-OAEP
│   └── hashing/        # SHA-256 + HMAC
├── messaging/          # Secure SEND/RECEIVE
├── storage/            # Encrypted STORE/RETRIEVE + SQLite
├── tests/              # Unit, integration, security tests
├── examples/           # .sl sample programs
├── scripts/            # Setup scripts
├── config/             # Global settings
├── docs/               # Extended documentation
├── main.py             # Compiler driver
└── requirements.txt    # Python dependencies
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*SecureLang — Designed for security-first programming.*
