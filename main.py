"""
SecureLang Compiler Driver
============================
Main entry point for the SecureLang compiler and runtime.

Pipeline:
  Source Code (.sl)
    → Lexer         (tokens)
    → Parser        (AST)
    → Semantic Analyzer (type + scope checking)
    → IR Generator  (Three-Address Code)
    → Optimizer     (4 passes)
    → VM Executor   (run)

Usage:
  python main.py source.sl              # compile and run
  python main.py source.sl --ast        # show AST
  python main.py source.sl --ir         # show IR before optimization
  python main.py source.sl --opt-ir     # show IR after optimization
  python main.py source.sl --tokens     # show token stream
  python main.py --init-db              # initialize the database
  python main.py --keygen               # generate RSA key pair
"""

import sys
import os
import argparse
import traceback

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer   import Lexer, LexerError
from compiler.parser  import Parser, ParseError
from compiler.ast     import ASTPrinter
from compiler.semantic import SemanticAnalyzer, SemanticError
from compiler.intermediate import IRGenerator
from compiler.optimizer    import Optimizer
from compiler.codegen      import SecureLangVM

from storage.database      import Database
from storage.secure_storage import SecureStorage
from messaging.messenger   import SecureMessenger
from security.rsa.rsa_keys import RSAKeyPair

from config.settings import DB_PATH, KEY_DIR


# ── ANSI Color Codes ──────────────────────────────────────────────────────────
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"


def banner():
    print(f"{C.CYAN}{C.BOLD}")
    print("=" * 56)
    print("   SecureLang Compiler  v1.0.0")
    print("   Secure Communication & Encrypted Data Storage")
    print("=" * 56)
    print(C.RESET)


def compile_and_run(source: str, source_name: str, args, db: Database,
                    messenger: SecureMessenger, storage: SecureStorage):
    """
    Full compilation pipeline: source → execution.
    Returns True on success, False on error.
    """

    # ── Phase 1: Lexical Analysis ─────────────────────────────────────────────
    print(f"{C.CYAN}[1/6] Lexical Analysis...{C.RESET}")
    try:
        lexer  = Lexer(source)
        tokens = lexer.tokenize()
        db.log("INFO", "lexer", f"Tokenized {len(tokens)} tokens from {source_name}")
    except LexerError as e:
        print(f"{C.RED}[ERROR] Lexer Error: {e}{C.RESET}")
        db.log("ERROR", "lexer", str(e))
        return False

    if args.tokens:
        print(f"\n{C.YELLOW}--- Token Stream ---{C.RESET}")
        for tok in tokens:
            print(f"  {tok}")
        print()

    # ── Phase 2: Parsing ──────────────────────────────────────────────────────
    print(f"{C.CYAN}[2/6] Parsing...{C.RESET}")
    try:
        parser = Parser(tokens)
        ast    = parser.parse()
        db.log("INFO", "parser", f"Parsed AST with {len(ast.statements)} top-level statements")
    except ParseError as e:
        print(f"{C.RED}[ERROR] Parse Error: {e}{C.RESET}")
        db.log("ERROR", "parser", str(e))
        return False

    if args.ast:
        print(f"\n{C.YELLOW}--- Abstract Syntax Tree ---{C.RESET}")
        ASTPrinter().print(ast)
        print()

    # ── Phase 3: Semantic Analysis ────────────────────────────────────────────
    print(f"{C.CYAN}[3/6] Semantic Analysis...{C.RESET}")
    analyzer = SemanticAnalyzer()
    ok       = analyzer.analyze(ast)
    if analyzer.errors:
        for err in analyzer.errors:
            print(f"{C.RED}  [X] {err}{C.RESET}")
            db.log("ERROR", "semantic", str(err))
        if not ok:
            print(f"{C.RED}[ERROR] Semantic analysis failed with {len(analyzer.errors)} error(s){C.RESET}")
            return False
        print(f"{C.YELLOW}  [!] Semantic warnings present but continuing...{C.RESET}")
    else:
        print(f"  {C.GREEN}[OK] No semantic errors{C.RESET}")
        db.log("INFO", "semantic", "Semantic analysis passed")

    # ── Phase 4: IR Generation ────────────────────────────────────────────────
    print(f"{C.CYAN}[4/6] Generating Intermediate Representation...{C.RESET}")
    ir_gen = IRGenerator()
    ir     = ir_gen.generate(ast)
    db.log("INFO", "ir_gen", f"Generated {len(ir)} TAC instructions")

    if args.ir:
        print(f"\n{C.YELLOW}--- Intermediate Representation (TAC) ---{C.RESET}")
        print(ir.dump())
        print()

    # ── Phase 5: Optimization ─────────────────────────────────────────────────
    print(f"{C.CYAN}[5/6] Optimizing...{C.RESET}")
    before     = len(ir)
    optimizer  = Optimizer(passes=3)
    opt_ir     = optimizer.optimize(ir)
    after      = len(opt_ir)
    reduction  = before - after
    db.log("INFO", "optimizer",
           f"Optimization: {before} -> {after} instructions (-{reduction})")
    print(f"  {C.GREEN}[OK] {before} -> {after} instructions "
          f"({reduction} eliminated){C.RESET}")

    if args.opt_ir:
        print(f"\n{C.YELLOW}--- Optimized IR ---{C.RESET}")
        print(opt_ir.dump())
        print()

    # ── Phase 6: Execution ────────────────────────────────────────────────────
    print(f"{C.CYAN}[6/6] Executing...{C.RESET}")
    print(f"{C.YELLOW}{'-'*50}{C.RESET}")
    db.log("INFO", "vm", f"Starting execution of {source_name}")
    try:
        vm = SecureLangVM(opt_ir, messenger=messenger, storage=storage)
        vm.run()
        db.log("INFO", "vm", "Execution completed successfully")
    except Exception as e:
        print(f"\n{C.RED}[ERROR] Runtime Error: {e}{C.RESET}")
        db.log("ERROR", "vm", str(e))
        if args.debug:
            traceback.print_exc()
        return False

    print(f"{C.YELLOW}{'-'*50}{C.RESET}")
    print(f"{C.GREEN}[OK] Execution completed successfully{C.RESET}")
    return True


def init_database(db: Database):
    """Initialize the SQLite database schema."""
    print(f"{C.CYAN}Initializing database at: {DB_PATH}{C.RESET}")
    db.initialize()
    print(f"{C.GREEN}[OK] Database initialized successfully{C.RESET}")
    db.log("INFO", "setup", "Database initialized")


def generate_keys():
    """Generate and save an RSA-2048 key pair."""
    os.makedirs(KEY_DIR, exist_ok=True)
    priv_path = os.path.join(KEY_DIR, "private.pem")
    pub_path  = os.path.join(KEY_DIR, "public.pem")
    print(f"{C.CYAN}Generating RSA-2048 key pair...{C.RESET}")
    kp = RSAKeyPair.generate_keys()
    kp.save_private(priv_path)
    kp.save_public(pub_path)
    print(f"{C.GREEN}[OK] Private key: {priv_path}{C.RESET}")
    print(f"{C.GREEN}[OK] Public key:  {pub_path}{C.RESET}")


def main():
    banner()

    parser = argparse.ArgumentParser(
        prog="securelang",
        description="SecureLang Compiler & Runtime"
    )
    parser.add_argument("source",     nargs="?", help="Source file (.sl)")
    parser.add_argument("--tokens",   action="store_true", help="Print token stream")
    parser.add_argument("--ast",      action="store_true", help="Print AST")
    parser.add_argument("--ir",       action="store_true", help="Print raw IR")
    parser.add_argument("--opt-ir",   action="store_true", help="Print optimized IR")
    parser.add_argument("--init-db",  action="store_true", help="Initialize database")
    parser.add_argument("--keygen",   action="store_true", help="Generate RSA key pair")
    parser.add_argument("--debug",    action="store_true", help="Show full tracebacks")

    args = parser.parse_args()

    # Initialize database (always needed)
    db = Database(DB_PATH)
    db.initialize()

    if args.init_db:
        init_database(db)
        return

    if args.keygen:
        generate_keys()
        return

    if not args.source:
        parser.print_help()
        return

    if not os.path.isfile(args.source):
        print(f"{C.RED}[ERROR] File not found: {args.source}{C.RESET}")
        sys.exit(1)

    with open(args.source, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Initialize runtime services
    storage   = SecureStorage(db)
    messenger = SecureMessenger(db, sender="runtime")

    success = compile_and_run(
        source_code, args.source, args, db, messenger, storage
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
