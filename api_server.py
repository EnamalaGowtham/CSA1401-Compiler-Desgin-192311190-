"""
SecureLang API Server
======================
FastAPI backend that bridges the React dashboard frontend with the
SecureLang compiler, cryptography, and storage subsystems.

Endpoints:
  POST /api/compile           - Compile + execute SecureLang source code
  POST /api/compile/tokens    - Return token stream for a source
  POST /api/compile/ast       - Return AST dump for a source
  POST /api/compile/ir        - Return TAC IR for a source (pre/post optimization)
  POST /api/encrypt           - AES-256-GCM encrypt a payload
  POST /api/decrypt           - AES-256-GCM decrypt a payload
  POST /api/hash              - SHA-256 hash a value
  POST /api/keygen            - Generate RSA-2048 key pair
  GET  /api/messages          - Retrieve stored messages
  POST /api/messages/send     - Send an encrypted message
  GET  /api/files             - List stored encrypted files
  POST /api/files/store       - Store a file (encrypted)
  POST /api/files/retrieve    - Retrieve a file (decrypted)
  GET  /api/logs              - Get audit log entries
  GET  /api/health            - Health check

Run:
    pip install fastapi uvicorn
    python api_server.py
"""

import sys
import os
import io
import json
import base64
import traceback
import time
from datetime import datetime
from typing import Optional

# FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compiler.lexer      import Lexer, LexerError
from compiler.parser     import Parser, ParseError
from compiler.ast        import ASTPrinter
from compiler.semantic   import SemanticAnalyzer, SemanticError
from compiler.intermediate import IRGenerator
from compiler.optimizer   import Optimizer
from compiler.codegen     import SecureLangVM

from security.encryption.aes_cipher import AESCipher
from security.hashing.sha256 import generate_hash, generate_hmac, verify_hmac, hash_password
from security.rsa.rsa_keys   import RSAKeyPair

from storage.database       import Database
from storage.secure_storage  import SecureStorage
from messaging.messenger     import SecureMessenger
from config.settings         import DB_PATH, KEY_DIR


# ── App Setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="SecureLang API",
    description="REST API for the SecureLang Compiler & Cryptography Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict to the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Shared Services ───────────────────────────────────────────────────────────

db        = Database(DB_PATH)
db.initialize()
storage   = SecureStorage(db)
messenger = SecureMessenger(db, sender="api_runtime")


# ── Request / Response Models ─────────────────────────────────────────────────

class CompileRequest(BaseModel):
    source: str
    filename: str = "main.sl"

class EncryptRequest(BaseModel):
    plaintext: str
    key_b64: Optional[str] = None   # Optional: provide your own AES key (base64)

class DecryptRequest(BaseModel):
    ciphertext_b64: str
    key_b64: str

class HashRequest(BaseModel):
    value: str
    password_mode: bool = False     # Use PBKDF2 password hashing if True

class SendMessageRequest(BaseModel):
    message: str
    recipient: str = "broadcast"

class StoreFileRequest(BaseModel):
    filename: str
    data: str

class RetrieveFileRequest(BaseModel):
    filename: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _capture_vm_output(source: str, messenger_: SecureMessenger, storage_: SecureStorage) -> dict:
    """Run full pipeline, capture stdout, and return structured results."""
    start_ms = time.time()
    output_lines = []
    errors = []

    # Redirect stdout to capture VM print() calls
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Phase 1: Lex
        lexer  = Lexer(source)
        tokens = lexer.tokenize()

        # Phase 2: Parse
        parser = Parser(tokens)
        ast    = parser.parse()

        # Phase 3: Semantic
        analyzer = SemanticAnalyzer()
        ok = analyzer.analyze(ast)
        if analyzer.errors:
            errors = [str(e) for e in analyzer.errors]
            if not ok:
                raise SemanticError("Semantic analysis failed")

        # Phase 4: IR
        ir_gen = IRGenerator()
        ir     = ir_gen.generate(ast)
        ir_before = ir.dump()
        ir_count_before = len(ir)

        # Phase 5: Optimize
        optimizer = Optimizer(passes=3)
        opt_ir    = optimizer.optimize(ir)
        ir_after  = opt_ir.dump()
        ir_count_after = len(opt_ir)

        # Phase 6: Execute
        vm = SecureLangVM(opt_ir, messenger=messenger_, storage=storage_)
        vm.run()

        captured = sys.stdout.getvalue()
        output_lines = captured.splitlines()

    except (LexerError, ParseError, SemanticError) as e:
        errors.append(str(e))
        ir_before = ""
        ir_after  = ""
        ir_count_before = ir_count_after = 0
        tokens = []
        ast = None
        captured = ""
        output_lines = []
    except Exception as e:
        errors.append(f"[RuntimeError] {e}")
        captured = sys.stdout.getvalue()
        output_lines = captured.splitlines()
        ir_before = ir_after = ""
        ir_count_before = ir_count_after = 0
        tokens = []
        ast = None
    finally:
        sys.stdout = old_stdout

    elapsed_ms = round((time.time() - start_ms) * 1000, 2)
    success = len([e for e in errors if "SemanticError" not in e or "error" in e.lower()]) == 0 and not any("RuntimeError" in e or "ParseError" in e or "LexerError" in e for e in errors)

    return {
        "success":           len(errors) == 0,
        "output":            output_lines,
        "errors":            errors,
        "elapsed_ms":        elapsed_ms,
        "token_count":       len(tokens) if tokens else 0,
        "ir_before":         ir_before,
        "ir_after":          ir_after,
        "instructions_before": ir_count_before,
        "instructions_after":  ir_count_after,
    }


def _tokenize_only(source: str) -> list:
    """Return token stream as list of dicts."""
    lexer  = Lexer(source)
    tokens = lexer.tokenize()
    return [
        {"type": t.type.name, "value": str(t.value), "line": t.line, "col": t.column}
        for t in tokens
    ]


def _ast_dump(source: str) -> str:
    """Return AST as indented text."""
    lexer  = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast    = parser.parse()

    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        ASTPrinter().print(ast)
    finally:
        sys.stdout = old_stdout
    return buf.getvalue()


# ── API Routes ────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """Health check — confirms the API server is reachable."""
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "subsystems": {
            "compiler":  "online",
            "database":  "connected",
            "crypto":    "active",
            "messaging": "ready"
        }
    }


@app.post("/api/compile")
def compile_and_run(req: CompileRequest):
    """
    Full compilation pipeline: source code → execution output.
    Returns stdout, errors, timing, and IR statistics.
    """
    db.log("INFO", "api", f"Compile request: {req.filename} ({len(req.source)} chars)")
    result = _capture_vm_output(req.source, messenger, storage)
    db.log(
        "INFO" if result["success"] else "ERROR",
        "api",
        f"Compile {'OK' if result['success'] else 'FAILED'} in {result['elapsed_ms']}ms"
    )
    return result


@app.post("/api/compile/tokens")
def get_tokens(req: CompileRequest):
    """Return the full token stream for a SecureLang source."""
    try:
        tokens = _tokenize_only(req.source)
        return {"tokens": tokens, "count": len(tokens)}
    except LexerError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/api/compile/ast")
def get_ast(req: CompileRequest):
    """Return the AST dump (indented text) for a SecureLang source."""
    try:
        ast_text = _ast_dump(req.source)
        return {"ast": ast_text}
    except (LexerError, ParseError) as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.post("/api/compile/ir")
def get_ir(req: CompileRequest):
    """Return pre- and post-optimization TAC IR for a SecureLang source."""
    try:
        lexer  = Lexer(req.source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast    = parser.parse()
        ir_gen = IRGenerator()
        ir     = ir_gen.generate(ast)
        optimizer = Optimizer(passes=3)
        opt_ir    = optimizer.optimize(ir)
        return {
            "ir_before": ir.dump(),
            "ir_after":  opt_ir.dump(),
            "count_before": len(ir),
            "count_after":  len(opt_ir),
            "eliminated": len(ir) - len(opt_ir)
        }
    except (LexerError, ParseError, SemanticError) as e:
        raise HTTPException(status_code=422, detail=str(e))


# ── Cryptography Endpoints ────────────────────────────────────────────────────

@app.post("/api/encrypt")
def encrypt_payload(req: EncryptRequest):
    """AES-256-GCM encrypt a plaintext payload. Returns ciphertext + key (base64)."""
    try:
        if req.key_b64:
            key = base64.b64decode(req.key_b64)
        else:
            key = AESCipher.generate_key()
        cipher = AESCipher(key)
        ct     = cipher.encrypt_message(req.plaintext.encode("utf-8"))
        return {
            "ciphertext_b64": base64.b64encode(ct).decode("ascii"),
            "key_b64":        base64.b64encode(key).decode("ascii"),
            "algorithm":      "AES-256-GCM",
            "key_size_bits":  256,
            "original_size_bytes":  len(req.plaintext.encode()),
            "encrypted_size_bytes": len(ct),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/decrypt")
def decrypt_payload(req: DecryptRequest):
    """AES-256-GCM decrypt a base64-encoded ciphertext."""
    try:
        key = base64.b64decode(req.key_b64)
        ct  = base64.b64decode(req.ciphertext_b64)
        cipher    = AESCipher(key)
        plaintext = cipher.decrypt_message(ct).decode("utf-8")
        return {"plaintext": plaintext, "algorithm": "AES-256-GCM"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/hash")
def hash_value(req: HashRequest):
    """SHA-256 hash a value, or PBKDF2-HMAC-SHA256 password hash."""
    try:
        if req.password_mode:
            import secrets
            salt = secrets.token_hex(16)
            hashed = hash_password(req.value, salt)
            return {"hash": hashed, "salt": salt, "algorithm": "PBKDF2-HMAC-SHA256"}
        else:
            h = generate_hash(req.value.encode("utf-8"))
            return {"hash": h, "algorithm": "SHA-256", "length_bits": 256}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/keygen")
def generate_keys():
    """Generate an RSA-2048 key pair and return as PEM strings."""
    try:
        kp = RSAKeyPair.generate_keys()
        pub_pem = kp.public_key_pem.decode("utf-8")
        # Encrypt a test payload
        test_msg = b"SecureLang RSA Test"
        encrypted = kp.encrypt_key(test_msg)
        decrypted = kp.decrypt_key(encrypted)
        return {
            "public_key_pem":    pub_pem,
            "key_size_bits":     2048,
            "algorithm":         "RSA-OAEP-SHA256",
            "roundtrip_test":    decrypted == test_msg,
            "generated_at":      datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Messaging Endpoints ───────────────────────────────────────────────────────

@app.post("/api/messages/send")
def send_message(req: SendMessageRequest):
    """Encrypt and store a secure message."""
    try:
        packet = messenger.send(req.message, req.recipient)
        db.log("INFO", "messaging", f"Message sent to '{req.recipient}' ({len(req.message)} chars)")
        return {
            "success":   True,
            "packet":    {k: v for k, v in packet.items() if k != "encrypted"},  # Don't expose raw ciphertext
            "encrypted": True,
            "algorithm": "AES-256-GCM + HMAC-SHA256"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/messages")
def get_messages(recipient: str = "runtime", limit: int = 20):
    """Retrieve and decrypt stored messages."""
    try:
        all_msgs = db.fetch_messages(recipient)[-limit:]
        return {
            "messages": all_msgs,
            "count":    len(all_msgs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Storage Endpoints ─────────────────────────────────────────────────────────

@app.post("/api/files/store")
def store_file(req: StoreFileRequest):
    """AES-encrypt and store a file in the SQLite database."""
    try:
        storage.store(req.filename, req.data.encode("utf-8"))
        sha = generate_hash(req.data.encode("utf-8"))
        db.log("INFO", "storage", f"Stored encrypted file '{req.filename}' (hash: {sha[:16]}...)")
        return {
            "success":   True,
            "filename":  req.filename,
            "sha256":    sha,
            "size_bytes": len(req.data.encode()),
            "encrypted": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/files/retrieve")
def retrieve_file(req: RetrieveFileRequest):
    """Decrypt and return a stored file's content."""
    try:
        raw = storage.retrieve(req.filename)
        content = raw.decode("utf-8")
        return {
            "success":  True,
            "filename": req.filename,
            "content":  content,
            "size_bytes": len(raw)
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{req.filename}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files")
def list_files():
    """List all encrypted files stored in the database."""
    try:
        files = db.list_files()
        return {"files": files, "count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/files/{filename}")
def delete_file(filename: str):
    """Delete a stored file."""
    try:
        deleted = db.delete_file(filename)
        return {"success": deleted, "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Audit Logs ────────────────────────────────────────────────────────────────

@app.get("/api/logs")
def get_logs(component: str = None, level: str = None, limit: int = 50):
    """Return audit log entries, filterable by component and log level."""
    try:
        logs = db.get_logs(component=component, level=level, limit=limit)
        return {"logs": logs, "count": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 56)
    print("  SecureLang API Server  v1.0.0")
    print("  http://localhost:8000")
    print("  Swagger UI: http://localhost:8000/docs")
    print("=" * 56)
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
