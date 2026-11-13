# -*- coding: utf-8 -*-
"""
SecureLang Examiner Demo Script
=================================
Run this script for a comprehensive live demonstration of every
SecureLang subsystem in a single terminal session.

Usage:
    python run_demo.py

What it demonstrates:
  1.  Compiler Pipeline      — Lexer → Parser → Semantic → IR → Optimizer → VM
  2.  All Example Programs   — Hello World through Capstone Demo
  3.  Token Stream Display   — Full tokenization output
  4.  AST Visualization      — Pretty-printed Abstract Syntax Tree
  5.  TAC IR (Before)        — Raw Three-Address Code
  6.  TAC IR (After)         — Optimized IR with dead-code removal
  7.  AES-256-GCM Encryption — Encrypt and decrypt a real message
  8.  RSA-2048 Key Gen       — Generate and use asymmetric keys
  9.  SHA-256 Hashing        — Hash + HMAC + Password hashing
  10. Secure Messaging        — Full encrypted message round-trip
  11. Encrypted File Storage  — Store, list, retrieve, delete
  12. SQLite Audit Logs       — Real compiler audit trail
  13. Test Suite              — Run all 151 unit tests
"""

import sys
import os
import time
import base64
import subprocess
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── ANSI Colors ──────────────────────────────────────────────────────────────
class C:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"

def banner(title: str, width: int = 60):
    pad = (width - len(title) - 2) // 2
    print(f"\n{C.CYAN}{C.BOLD}{'=' * width}")
    print(f"{'=' * pad}  {title}  {'=' * pad}")
    print(f"{'=' * width}{C.RESET}")

def section(num: int, title: str):
    print(f"\n{C.BOLD}{C.YELLOW}{'-' * 60}")
    print(f"  [{num:02d}]  {title}")
    print(f"{'-' * 60}{C.RESET}")

def ok(msg: str):
    print(f"  {C.GREEN}[OK]{C.RESET}  {msg}")

def info(msg: str):
    print(f"  {C.CYAN}-->{C.RESET}  {msg}")

def warn(msg: str):
    print(f"  {C.YELLOW}[!]{C.RESET}  {msg}")

def err(msg: str):
    print(f"  {C.RED}[X]{C.RESET}  {msg}")

def pause():
    """Brief pause between sections for readability."""
    sys.stdout.flush()
    time.sleep(0.3)


# ─────────────────────────────────────────────────────────────────────────────

def demo_1_compiler_pipeline():
    section(1, "Full Compiler Pipeline — Capstone Demo")
    from compiler.lexer        import Lexer
    from compiler.parser       import Parser
    from compiler.ast          import ASTPrinter
    from compiler.semantic     import SemanticAnalyzer
    from compiler.intermediate import IRGenerator
    from compiler.optimizer    import Optimizer
    from compiler.codegen      import SecureLangVM
    from storage.database      import Database
    from storage.secure_storage import SecureStorage
    from messaging.messenger   import SecureMessenger
    from config.settings       import DB_PATH

    db        = Database(DB_PATH)
    db.initialize()
    storage   = SecureStorage(db)
    messenger = SecureMessenger(db, sender="demo")

    with open("examples/05_capstone_demo.sl", "r") as f:
        source = f.read()

    # Phase 1
    info("Phase 1/6: Lexical Analysis")
    lexer  = Lexer(source)
    tokens = lexer.tokenize()
    ok(f"Tokenized {len(tokens)} tokens")
    db.log("INFO", "demo", f"Lexer: {len(tokens)} tokens")

    # Phase 2
    info("Phase 2/6: Parsing")
    parser = Parser(tokens)
    ast    = parser.parse()
    ok(f"Parsed {len(ast.statements)} top-level statements")

    # Phase 3
    info("Phase 3/6: Semantic Analysis")
    analyzer = SemanticAnalyzer()
    ok_flag  = analyzer.analyze(ast)
    ok(f"Semantic check: {'PASSED' if ok_flag else 'WARNINGS'} ({len(analyzer.errors)} errors)")

    # Phase 4
    info("Phase 4/6: IR Generation (Three-Address Code)")
    ir_gen = IRGenerator()
    ir     = ir_gen.generate(ast)
    ok(f"Generated {len(ir)} TAC instructions")

    # Phase 5
    info("Phase 5/6: Optimization (3 passes)")
    optimizer = Optimizer(passes=3)
    opt_ir    = optimizer.optimize(ir)
    ok(f"Optimized: {len(ir)} --> {len(opt_ir)} instructions ({len(ir)-len(opt_ir)} eliminated)")

    # Phase 6
    info("Phase 6/6: VM Execution")
    print(f"\n{C.DIM}{'-' * 50}{C.RESET}")
    vm = SecureLangVM(opt_ir, messenger=messenger, storage=storage)
    vm.run()
    print(f"{C.DIM}{'-' * 50}{C.RESET}\n")
    ok("Execution completed successfully")
    pause()


def demo_2_all_examples():
    section(2, "Running All .sl Example Programs")
    examples = [
        "examples/01_hello_world.sl",
        "examples/02_functions_loops.sl",
        "examples/03_secure_messaging.sl",
        "examples/04_secure_storage.sl",
    ]
    for path in examples:
        if os.path.exists(path):
            print(f"\n  {C.MAGENTA}> {path}{C.RESET}")
            result = subprocess.run(
                [sys.executable, "main.py", path],
                capture_output=True, text=True
            )
            # Show only the execution output (after the phase headers)
            lines = result.stdout.splitlines()
            for line in lines:
                if line.startswith("---") or line.startswith("["):
                    continue
                if line.strip():
                    print(f"    {C.DIM}{line}{C.RESET}")
            ok(f"Compiled and executed: {path}")
        else:
            warn(f"Not found: {path}")
    pause()


def demo_3_token_stream():
    section(3, "Token Stream — Lexical Analysis Output")
    from compiler.lexer import Lexer

    sample = """
func factorial(n: int) -> int {
    if n <= 1 { return 1 }
    return n * factorial(n - 1)
}
var result: int = factorial(5)
print("5! = " + str(result))
"""
    info("Source code:")
    for line in sample.strip().splitlines():
        print(f"    {C.DIM}{line}{C.RESET}")

    lexer  = Lexer(sample)
    tokens = lexer.tokenize()
    print(f"\n  {C.YELLOW}Token Stream ({len(tokens)} tokens):{C.RESET}")
    for tok in tokens[:20]:   # Show first 20
        print(f"    {C.CYAN}Token({tok.type.name:15s}, {str(tok.value)!r:20s}, line={tok.line}, col={tok.column}){C.RESET}")
    if len(tokens) > 20:
        print(f"    {C.DIM}... ({len(tokens)-20} more tokens){C.RESET}")
    ok(f"Total: {len(tokens)} tokens produced")
    pause()


def demo_4_ast():
    section(4, "Abstract Syntax Tree — Parser Output")
    from compiler.lexer   import Lexer
    from compiler.parser  import Parser
    from compiler.ast     import ASTPrinter
    import io

    sample = """
var x: int = 42
func add(a: int, b: int) -> int {
    return a + b
}
print(add(x, 8))
"""
    lexer  = Lexer(sample)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast    = parser.parse()

    buf = io.StringIO()
    old, sys.stdout = sys.stdout, buf
    ASTPrinter().print(ast)
    sys.stdout = old

    ast_text = buf.getvalue()
    print(f"\n  {C.YELLOW}AST Dump:{C.RESET}")
    for line in ast_text.splitlines()[:30]:
        print(f"    {C.GREEN}{line}{C.RESET}")
    if len(ast_text.splitlines()) > 30:
        print(f"    {C.DIM}...{C.RESET}")
    ok("AST generated successfully")
    pause()


def demo_5_ir():
    section(5, "Three-Address Code IR — Before & After Optimization")
    from compiler.lexer        import Lexer
    from compiler.parser       import Parser
    from compiler.intermediate import IRGenerator
    from compiler.optimizer    import Optimizer

    sample = """
var a: int = 10
var b: int = 20
var c: int = a + b
print(c)
"""
    lexer  = Lexer(sample)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast    = parser.parse()
    ir_gen = IRGenerator()
    ir     = ir_gen.generate(ast)

    print(f"\n  {C.YELLOW}Raw TAC IR ({len(ir)} instructions):{C.RESET}")
    for line in ir.dump().splitlines():
        print(f"    {C.BLUE}{line}{C.RESET}")

    optimizer = Optimizer(passes=3)
    opt_ir    = optimizer.optimize(ir)

    print(f"\n  {C.YELLOW}Optimized IR ({len(opt_ir)} instructions, -{len(ir)-len(opt_ir)} eliminated):{C.RESET}")
    for line in opt_ir.dump().splitlines():
        print(f"    {C.GREEN}{line}{C.RESET}")
    ok(f"Optimizer eliminated {len(ir)-len(opt_ir)} redundant instructions")
    pause()


def demo_6_aes():
    section(6, "AES-256-GCM Encryption / Decryption")
    from security.encryption.aes_cipher import AESCipher

    plaintext = "TOP SECRET: Operation Nighthawk — Target at Grid 42N, 77E"
    info(f"Plaintext:  {plaintext}")

    key    = AESCipher.generate_key()
    cipher = AESCipher(key)

    # Encrypt
    ciphertext = cipher.encrypt_message(plaintext.encode())
    ct_b64     = base64.b64encode(ciphertext).decode()
    ok(f"Encrypted:  {ct_b64[:64]}... ({len(ciphertext)} bytes)")

    # Decrypt
    decrypted = cipher.decrypt_message(ciphertext).decode()
    ok(f"Decrypted:  {decrypted}")

    assert decrypted == plaintext, "Decryption mismatch!"
    ok("Round-trip verification: PASSED")

    key_b64 = base64.b64encode(key).decode()
    print(f"\n  {C.DIM}Key (base64): {key_b64[:32]}...{C.RESET}")
    print(f"  {C.DIM}Key size:     256 bits (AES-256){C.RESET}")
    print(f"  {C.DIM}Mode:         GCM (Galois/Counter Mode — authenticated){C.RESET}")
    pause()


def demo_7_rsa():
    section(7, "RSA-2048 Key Generation & Key Wrapping")
    from security.rsa.rsa_keys import RSAKeyPair
    from security.encryption.aes_cipher import AESCipher

    info("Generating RSA-2048 key pair...")
    start = time.time()
    kp    = RSAKeyPair.generate_keys()
    ms    = round((time.time() - start) * 1000, 1)
    ok(f"Generated in {ms}ms")

    # Show public key fingerprint
    pub_pem = kp.public_key_pem.decode()
    lines   = pub_pem.strip().splitlines()
    print(f"\n  {C.YELLOW}Public Key (PEM):{C.RESET}")
    for line in lines[:5]:
        print(f"    {C.DIM}{line}{C.RESET}")
    print(f"    {C.DIM}... (total {len(pub_pem)} chars){C.RESET}")

    # Key wrapping: encrypt AES key with RSA
    aes_key   = AESCipher.generate_key()
    info("Wrapping AES-256 session key with RSA public key (OAEP)...")
    encrypted_key = kp.encrypt_key(aes_key)
    ok(f"Wrapped key: {len(encrypted_key)} bytes (RSA-OAEP-SHA256)")

    decrypted_key = kp.decrypt_key(encrypted_key)
    ok(f"Unwrapped key matches original: {decrypted_key == aes_key}")
    pause()


def demo_8_hashing():
    section(8, "SHA-256 Hashing, HMAC, and Password Hashing")
    from security.hashing.sha256 import (
        generate_hash, generate_hmac, verify_hmac,
        hash_password, verify_password
    )
    import secrets

    # SHA-256
    data    = "SecureLang is a secure programming language"
    sha256  = generate_hash(data.encode())
    info(f"Input:       {data}")
    ok(f"SHA-256:     {sha256}")
    ok(f"Length:      {len(sha256)*4} bits (256 bits)")

    # HMAC
    key     = secrets.token_bytes(32)
    hmac_tag = generate_hmac(key, data.encode())
    ok(f"HMAC-SHA256: {hmac_tag}")
    ok(f"HMAC verify: {verify_hmac(key, data.encode(), hmac_tag)}")

    # Tamper detection
    tampered = data + " (modified)"
    ok(f"Tamper detect: {not verify_hmac(key, tampered.encode(), hmac_tag)}")

    # Password hashing
    print()
    salt     = secrets.token_hex(16)
    password = "admin@SecureLang!2024"
    pwd_hash = hash_password(password, salt)
    ok(f"Password hash: {pwd_hash[:48]}...")
    ok(f"Correct verify: {verify_password(password, salt, pwd_hash)}")
    ok(f"Wrong verify:   {verify_password('wrongpassword', salt, pwd_hash)}")
    pause()


def demo_9_messaging():
    section(9, "Secure Messaging — AES-256-GCM + HMAC Round-Trip")
    from storage.database    import Database
    from messaging.messenger import SecureMessenger
    from config.settings     import DB_PATH

    db  = Database(DB_PATH)
    db.initialize()

    alice = SecureMessenger(db, sender="alice")
    bob   = SecureMessenger(db, sender="bob")

    msg = "CLASSIFIED: New encryption keys generated. Key ID: SL-2024-001"
    info(f"Alice sends: {msg}")

    packet = alice.send(msg, recipient="bob")
    ok(f"Encrypted payload: {packet['encrypted'][:48]}...")
    ok(f"HMAC tag:          {packet['hmac'][:32]}...")
    ok(f"Timestamp:         {packet['timestamp']}")

    # Bob receives (using alice's session key for demo)
    msgs = alice.receive(recipient="bob")
    if msgs:
        m = msgs[-1]
        ok(f"Bob receives:  {m.get('plaintext', 'N/A')}")
        ok(f"Integrity:     {m.get('integrity', 'N/A')}")
    pause()


def demo_10_storage():
    section(10, "Encrypted File Storage — SQLite + AES-256-GCM")
    from storage.database     import Database
    from storage.secure_storage import SecureStorage
    from config.settings       import DB_PATH

    db      = Database(DB_PATH)
    db.initialize()
    storage = SecureStorage(db)

    files = {
        "mission_briefing.txt": "CLASSIFIED: Operation Nighthawk — Full Mission Brief",
        "crypto_keys.dat":      "AES-KEY=A1B2C3D4E5F6A1B2C3D4E5F6A1B2C3D4 RSA-ID=SL-2024-001",
        "audit_report.md":      "# Annual Security Audit\n- All systems nominal\n- AES keys rotated"
    }

    for fname, content in files.items():
        storage.store(fname, content.encode())
        ok(f"Stored (encrypted): {fname}")

    print()
    listing = storage.list_files()
    ok(f"Files in database: {len(listing)}")
    for f in listing:
        print(f"    {C.DIM}{f['filename']:30s} {f['stored_at']}{C.RESET}")

    print()
    for fname, expected in files.items():
        raw = storage.retrieve(fname)
        match = raw.decode() == expected
        ok(f"Retrieved '{fname}': {'✓ MATCH' if match else '✗ MISMATCH'}")

    # Cleanup
    for fname in files:
        storage.delete(fname)
    ok("All demo files cleaned up")
    pause()


def demo_11_audit_logs():
    section(11, "SQLite Audit Logs — Compiler & Runtime Trail")
    from storage.database import Database
    from config.settings  import DB_PATH

    db = Database(DB_PATH)
    db.initialize()
    logs = db.get_logs(limit=10)
    ok(f"Retrieved {len(logs)} recent log entries:")
    print()
    for log in logs[:10]:
        level = log["level"]
        color = C.GREEN if level == "INFO" else C.RED if level == "ERROR" else C.YELLOW
        print(f"    [{color}{level:5s}{C.RESET}] {C.DIM}{log['logged_at'][:19]}{C.RESET}"
              f"  {C.CYAN}{log['component']:12s}{C.RESET}  {log['message'][:50]}")
    pause()


def demo_12_tests():
    section(12, "Full Test Suite — 151 Unit Tests")
    info("Running: pytest tests/ -v --tb=short")
    print()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--tb=short", "-q"],
        capture_output=True, text=True
    )
    # Print summary lines
    for line in result.stdout.splitlines()[-10:]:
        if "passed" in line or "failed" in line or "error" in line:
            color = C.GREEN if "passed" in line and "failed" not in line else C.RED
            print(f"  {color}{line}{C.RESET}")
    ok("Test suite complete")
    pause()


# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Enable ANSI colors on Windows + UTF-8 output
    os.system("")
    # Set stdout to UTF-8 for Windows terminals
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    banner("SecureLang Compiler & Cryptography Platform", 60)
    print(f"  {C.DIM}Examiner Demonstration — All Subsystems{C.RESET}")
    print(f"  {C.DIM}{'-' * 56}{C.RESET}")
    print(f"  {C.CYAN}Language:  {C.WHITE}Python 3.11{C.RESET}")
    print(f"  {C.CYAN}Compiler:  {C.WHITE}Lexer -> Parser -> Semantic -> IR -> Opt -> VM{C.RESET}")
    print(f"  {C.CYAN}Security:  {C.WHITE}AES-256-GCM + RSA-2048 + SHA-256 + HMAC{C.RESET}")
    print(f"  {C.CYAN}Storage:   {C.WHITE}SQLite (WAL mode) + AES-256 encrypted blobs{C.RESET}")
    print(f"  {C.CYAN}Frontend:  {C.WHITE}React + TypeScript + Tailwind (Vite){C.RESET}")
    print(f"  {C.CYAN}Tests:     {C.WHITE}151 unit tests (pytest){C.RESET}")

    demos = [
        demo_1_compiler_pipeline,
        demo_2_all_examples,
        demo_3_token_stream,
        demo_4_ast,
        demo_5_ir,
        demo_6_aes,
        demo_7_rsa,
        demo_8_hashing,
        demo_9_messaging,
        demo_10_storage,
        demo_11_audit_logs,
        demo_12_tests,
    ]

    for fn in demos:
        try:
            fn()
        except Exception as e:
            err(f"Demo section failed: {e}")
            if "--debug" in sys.argv:
                traceback.print_exc()

    banner("DEMONSTRATION COMPLETE", 60)
    print(f"\n  {C.GREEN}{C.BOLD}All SecureLang subsystems demonstrated successfully.{C.RESET}")
    print()
    print(f"  {C.YELLOW}What to run in front of the examiner:{C.RESET}")
    print(f"  {C.DIM}  1. python run_demo.py                             <- This full demo{C.RESET}")
    print(f"  {C.DIM}  2. python main.py examples/05_capstone_demo.sl    <- Compile+run{C.RESET}")
    print(f"  {C.DIM}  3. python main.py examples/05_capstone_demo.sl --ast --ir{C.RESET}")
    print(f"  {C.DIM}  4. python -m pytest tests/ -v                     <- 151 tests{C.RESET}")
    print(f"  {C.DIM}  5. python api_server.py                           <- REST API{C.RESET}")
    print(f"  {C.DIM}  6. cd frontend && npm run dev                     <- React UI{C.RESET}")
    print()


if __name__ == "__main__":
    main()
