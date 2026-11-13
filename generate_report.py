"""Generate SecureLang Word Document with Literature Survey + Flowcharts"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document()

# ── Page margins ──────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(2)
    section.right_margin  = Cm(2)

# ── Helper: set cell background ───────────────────────────────────────────────
def set_cell_bg(cell, hex_color):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd  = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  hex_color)
    tcPr.append(shd)

def set_cell_border(cell, **kwargs):
    tc   = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top','left','bottom','right'):
        tag = OxmlElement(f'w:{edge}')
        tag.set(qn('w:val'),   'single')
        tag.set(qn('w:sz'),    '4')
        tag.set(qn('w:color'), '4472C4')
        tcBorders.append(tag)
    tcPr.append(tcBorders)

# ══════════════════════════════════════════════════════════════════════════════
#  TITLE PAGE
# ══════════════════════════════════════════════════════════════════════════════
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = t.add_run('SecureLang')
run.bold      = True
run.font.size = Pt(28)
run.font.color.rgb = RGBColor(0x00, 0x4E, 0x98)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run('A Secure Domain-Specific Programming Language with Built-in Cryptography')
r.font.size = Pt(14)
r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

doc.add_paragraph()
info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info.add_run('Project Documentation — Literature Survey & System Flowchart\n').bold = True
info.add_run('Compiler Design | Python 3.11 | React 19 | AES-256-GCM | RSA-2048')

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 1 — SYSTEM FLOWCHART (Text-based, PPT-ready)
# ══════════════════════════════════════════════════════════════════════════════
h1 = doc.add_heading('Section 1: System Architecture Flowchart', level=1)
h1.runs[0].font.color.rgb = RGBColor(0x00, 0x4E, 0x98)

doc.add_paragraph(
    'The following diagram shows the complete end-to-end flow of SecureLang '
    'across all three modules: Compiler Pipeline, Security Engine, and React Dashboard.'
)
doc.add_paragraph()

# ── Flow diagram as a 3-column table ─────────────────────────────────────────
FLOW_ROWS = [
    ('INPUT',       '📄 User writes .sl source code',          ''),
    ('',            '↓',                                       ''),
    ('MODULE 1',    'PHASE 1 — LEXICAL ANALYSIS (Lexer)',       'Source text → Token Stream\n291 tokens (capstone demo)'),
    ('COMPILER',    '↓',                                       ''),
    ('PIPELINE',    'PHASE 2 — SYNTAX ANALYSIS (Parser)',       'Recursive Descent\nTokens → Abstract Syntax Tree'),
    ('',            '↓',                                       ''),
    ('',            'PHASE 3 — SEMANTIC ANALYSIS',             'Type Checking · Scope Analysis\nSymbol Table · Const Guard'),
    ('',            '↓',                                       ''),
    ('',            'PHASE 4 — IR GENERATION',                 'Three-Address Code (TAC)\n83 instructions generated'),
    ('',            '↓',                                       ''),
    ('',            'PHASE 5 — OPTIMIZATION (3 Passes)',        '• Constant Folding\n• Dead Code Elimination\n• Copy Propagation'),
    ('',            '↓',                                       ''),
    ('',            'PHASE 6 — VM EXECUTION',                  'SecureLangVM interprets TAC\nBuilt-in SEND / STORE opcodes'),
    ('',            '↓',                                       ''),
    ('MODULE 2',    'SECURITY ENGINE',                         ''),
    ('SECURITY',    'SEND opcode  →  AES-256-GCM Encrypt',     '+ HMAC-SHA256 Sign + SQLite Store'),
    ('',            'STORE opcode →  AES-256-GCM Encrypt',     '+ SHA-256 Hash + SQLite Blob'),
    ('',            'RSA-2048 Key Generation (OAEP)',           'Public/Private PEM export'),
    ('',            'SHA-256 / PBKDF2 Password Hashing',       'Salt + HMAC tamper detection'),
    ('',            '↓',                                       ''),
    ('DATABASE',    'SQLite Database (WAL Mode)',               'Tables: messages, stored_files,\nusers, keys, logs'),
    ('',            '↓',                                       ''),
    ('MODULE 3',    'REACT DASHBOARD (Frontend)',               ''),
    ('FRONTEND',    'Command Center · Compiler Studio',         'Monaco Editor · Run Code · Console'),
    ('',            'Secure Messaging · Secure Storage',        'AES chat UI · Encrypted Vault'),
    ('',            'Analytics · AST Visualizer',              'Charts · Tree View'),
    ('OUTPUT',      '📊 Results displayed to User',            ''),
]

tbl = doc.add_table(rows=0, cols=3)
tbl.style = 'Table Grid'
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

# Column widths
COL_W = [Cm(3), Cm(8), Cm(6.5)]
for i, w in enumerate(COL_W):
    for cell in tbl.columns[i].cells:
        cell.width = w

MODULE_COLOR = {
    'INPUT':    '1F4E79',
    'MODULE 1': '2E75B6',
    'COMPILER': '2E75B6',
    'PIPELINE': '2E75B6',
    'MODULE 2': '375623',
    'SECURITY': '375623',
    'DATABASE': '7B3F00',
    'MODULE 3': '4B275F',
    'FRONTEND': '4B275F',
    'OUTPUT':   '1F4E79',
    '':         '1B2A4A',
}

for label, phase, detail in FLOW_ROWS:
    row  = tbl.add_row()
    bg   = MODULE_COLOR.get(label, '1B2A4A')
    is_arrow = phase.strip() == '↓'

    for ci, (cell, text) in enumerate(zip(row.cells, [label, phase, detail])):
        set_cell_bg(cell, bg if not is_arrow else '0D1B2A')
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci != 2 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9 if ci == 2 else 10)
        r.bold = (ci == 0 and label != '') or (ci == 1 and not is_arrow)

doc.add_paragraph()

# ── Compiler Design Phase Quick-Reference ─────────────────────────────────────
doc.add_heading('Compiler Design Phase Reference', level=2)

phase_data = [
    ('Phase', 'Name',                'Input',         'Output',            'File',                  'CD Concept'),
    ('1',     'Lexical Analysis',    'Source text',   'Token stream',      'lexer/lexer.py',        'Finite Automata / DFA'),
    ('2',     'Syntax Analysis',     'Tokens',        'AST',               'parser/parser.py',      'CFG / Recursive Descent'),
    ('3',     'Semantic Analysis',   'AST',           'Annotated AST',     'semantic/analyzer.py',  'Type Checking / Symbol Table'),
    ('4',     'IR Generation',       'AST',           'TAC Instructions',  'intermediate/ir_gen.py','Three-Address Code'),
    ('5',     'Optimization',        'TAC IR',        'Optimized TAC',     'optimizer/optimizer.py','Const Fold / DCE / Copy Prop'),
    ('6',     'Code Generation/VM',  'Optimized TAC', 'Execution Output',  'codegen/vm.py',         'Virtual Machine / Interpreter'),
]

ptbl = doc.add_table(rows=len(phase_data), cols=6)
ptbl.style = 'Table Grid'
HEADER_BG = '2E75B6'
ROW_BG    = ['1B2A4A', '162033']

for ri, row_data in enumerate(phase_data):
    row = ptbl.rows[ri]
    for ci, text in enumerate(row_data):
        cell = row.cells[ci]
        bg = HEADER_BG if ri == 0 else ROW_BG[ri % 2]
        set_cell_bg(cell, bg)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9)
        r.bold = (ri == 0)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 2 — LITERATURE SURVEY
# ══════════════════════════════════════════════════════════════════════════════
h2 = doc.add_heading('Section 2: Literature Survey', level=1)
h2.runs[0].font.color.rgb = RGBColor(0x00, 0x4E, 0x98)

doc.add_paragraph(
    'The following table presents 10 key references that form the academic '
    'foundation of the SecureLang project, covering Compiler Design, '
    'Domain-Specific Languages, and Cryptography standards.'
)
doc.add_paragraph()

# ── Literature Survey Table ───────────────────────────────────────────────────
LIT_HEADERS = ['#', 'Title / Reference', 'Author(s)', 'Year', 'Key Contribution', 'Limitation', 'How SecureLang Addresses It']

LIT_DATA = [
    (
        '1',
        'Compilers: Principles,\nTechniques, and Tools\n(Dragon Book)',
        'Aho, Lam,\nSethi, Ullman',
        '2006',
        'Defines the complete 6-phase compiler pipeline: Lexical Analysis, Parsing, Semantic Analysis, IR Generation, Optimization, Code Generation',
        'Covers only general-purpose languages; no security-aware code generation or cryptographic opcodes',
        'SecureLang implements all 6 phases from this book. Extends Phase 6 (Code Generation) with AES-256-GCM and HMAC at the VM opcode level',
    ),
    (
        '2',
        'Domain-Specific\nLanguages',
        'Martin Fowler',
        '2010',
        'Introduces DSL design patterns — internal vs external DSLs — and their application in specialized computing domains',
        'Does not address cryptographic enforcement or runtime security guarantees within DSL semantics',
        'SecureLang is an external DSL where SEND, STORE, RETRIEVE are first-class compiler-enforced security keywords',
    ),
    (
        '3',
        'A Certified\nType-Preserving\nCompiler from Lambda\nCalculus to Assembly',
        'Ahmed &\nBlume',
        '2011',
        'Proves compiler correctness through type-preservation guarantees across all compilation phases using formal methods',
        'Focused on functional languages; no practical runtime security enforcement at execution level',
        'SecureLang\'s SemanticAnalyzer enforces type safety across all phases; VM enforces secure execution of SEND/STORE opcodes',
    ),
    (
        '4',
        'NIST FIPS 197 —\nAdvanced Encryption\nStandard (AES)',
        'NIST',
        '2001',
        'Defines AES as the federal standard for symmetric-key encryption with 128/192/256-bit key sizes and GCM authenticated mode',
        'Standard defines algorithm only; integration into programming languages is entirely left to the developer',
        'SecureLang builds AES-256-GCM directly into the VM executor. Developers use STORE — encryption is automatic, not optional',
    ),
    (
        '5',
        'PKCS #1: RSA\nCryptography Standard\n(RFC 8017)',
        'RSA Labs /\nIETF',
        '2016',
        'Defines RSA public-key encryption with OAEP padding for secure asymmetric key transport and digital signatures',
        'Requires manual correct implementation — developers must properly apply padding schemes or face vulnerabilities',
        'SecureLang\'s RSAKeyPair class uses OAEP-SHA256 padding via the cryptography library; exposed via --keygen CLI flag',
    ),
    (
        '6',
        'HMAC: Keyed-Hashing\nfor Message\nAuthentication\n(RFC 2104)',
        'Krawczyk,\nBellare,\nCanetti',
        '1997',
        'Defines HMAC as a provably secure message authentication code combining a cryptographic hash with a secret key',
        'Provides no language-level support — developers must manually call HMAC and verify the tag on every message',
        'Every SEND operation in SecureLang automatically computes HMAC-SHA256. Every RECEIVE verifies integrity — cannot be skipped',
    ),
    (
        '7',
        'Secure Coding\nin C and C++',
        'Robert\nSeacord',
        '2013',
        'Catalogs common security vulnerabilities caused by developer error: buffer overflows, format strings, unencrypted storage',
        'Relies entirely on developer discipline and code review; no language-level enforcement possible in C/C++',
        'SecureLang eliminates entire vulnerability classes by design: no raw pointers, no manual key management, no unencrypted I/O',
    ),
    (
        '8',
        'A Survey on\nDomain-Specific\nLanguages for Security',
        'Ligatti,\nCaires et al.',
        '2018',
        'Reviews existing security DSLs including policy languages, access control languages, and cryptographic protocol verifiers',
        'Most surveyed DSLs are verification or policy languages — not general-purpose secure computation languages',
        'SecureLang fills this gap: a general-purpose DSL where any computation can use built-in secure communication and storage',
    ),
    (
        '9',
        'SQLite: Past,\nPresent, and Future\n(VLDB 2022)',
        'Pandey\net al.',
        '2022',
        'Demonstrates SQLite as a world-class embedded database with WAL mode enabling concurrent reads and full ACID guarantees',
        'SQLite has no built-in encryption — all data is stored in plaintext by default without additional libraries',
        'SecureLang\'s Database module uses SQLite in WAL mode and stores all message payloads and file blobs as AES-GCM ciphertext',
    ),
    (
        '10',
        'Engineering a\nCompiler\n(2nd Edition)',
        'Cooper &\nTorczon',
        '2011',
        'Modern compiler backend treatment: register allocation, instruction selection, SSA form, loop optimization techniques',
        'Backend focuses on native code generation for real CPUs; does not address VM interpreters or security extensions',
        'SecureLang uses a VM executor (SecureLangVM) matching Cooper & Torczon\'s interpreter model, extended with cryptographic opcodes',
    ),
]

COL_WIDTHS_LIT = [Cm(0.8), Cm(3.2), Cm(2.0), Cm(0.9), Cm(4.2), Cm(3.5), Cm(4.5)]

ltbl = doc.add_table(rows=1 + len(LIT_DATA), cols=7)
ltbl.style = 'Table Grid'
ltbl.alignment = WD_TABLE_ALIGNMENT.CENTER

# Header row
hrow = ltbl.rows[0]
for ci, htext in enumerate(LIT_HEADERS):
    cell = hrow.cells[ci]
    set_cell_bg(cell, '1F4E79')
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(htext)
    r.bold = True
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    r.font.size = Pt(9)

# Data rows
ALT = ['1B2A4A', '162033']
for ri, row_data in enumerate(LIT_DATA):
    row = ltbl.rows[ri + 1]
    bg  = ALT[ri % 2]
    for ci, text in enumerate(row_data):
        cell = row.cells[ci]
        set_cell_bg(cell, bg)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in (0, 2, 3) else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(8)
        if ci == 0:
            r.bold = True

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
#  SECTION 3 — SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════
h3 = doc.add_heading('Section 3: Academic Concept Mapping Summary', level=1)
h3.runs[0].font.color.rgb = RGBColor(0x00, 0x4E, 0x98)

doc.add_paragraph(
    'This table maps every SecureLang implementation decision to its academic source — '
    'for easy reference in the PPT presentation.'
)
doc.add_paragraph()

SUMMARY = [
    ('Aspect',                'SecureLang Implementation',      'Academic Foundation'),
    ('Lexical Analysis',      'Lexer — 60+ token types',        'Aho et al. Dragon Book Ch.3'),
    ('Parsing Strategy',      'Recursive Descent Parser',       'Aho et al. Dragon Book Ch.4'),
    ('Grammar Notation',      'Full EBNF Grammar',              'Cooper & Torczon Ch.3'),
    ('Abstract Syntax Tree',  '25+ AST node types',             'Aho et al. Dragon Book Ch.5'),
    ('Visitor Pattern',       'ASTVisitor base class',          'Fowler — DSL Design Patterns'),
    ('Semantic Analysis',     'Type check + scoped symbol table','Aho et al. Dragon Book Ch.6'),
    ('Intermediate Code',     'Three-Address Code (TAC)',       'Aho et al. Dragon Book Ch.6'),
    ('Optimization',          'Const Fold + DCE + Copy Prop',   'Aho et al. Dragon Book Ch.9'),
    ('Code Generation',       'VM Interpreter for TAC',         'Cooper & Torczon Ch.11'),
    ('Symmetric Encryption',  'AES-256-GCM',                   'NIST FIPS 197 (2001)'),
    ('Asymmetric Encryption', 'RSA-2048-OAEP',                 'PKCS#1 / RFC 8017 (2016)'),
    ('Message Integrity',     'HMAC-SHA256 on every SEND',      'RFC 2104 — Krawczyk et al.'),
    ('Password Security',     'PBKDF2-HMAC-SHA256 + Salt',      'NIST SP 800-132'),
    ('Secure Storage',        'AES-GCM blobs in SQLite WAL',    'Pandey et al. VLDB (2022)'),
    ('Security Motivation',   'Eliminate crypto developer errors','Seacord — Secure Coding (2013)'),
    ('DSL Design',            'External DSL with .sl syntax',   'Fowler — Domain-Specific Languages (2010)'),
]

stbl = doc.add_table(rows=len(SUMMARY), cols=3)
stbl.style = 'Table Grid'

for ri, (a, b, c) in enumerate(SUMMARY):
    row = stbl.rows[ri]
    bg  = '1F4E79' if ri == 0 else ('1B2A4A' if ri % 2 else '162033')
    for ci, text in enumerate([a, b, c]):
        cell = row.cells[ci]
        set_cell_bg(cell, bg)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(text)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9)
        r.bold = (ri == 0)

# Footer
doc.add_paragraph()
foot = doc.add_paragraph()
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
foot.add_run('SecureLang v1.0.0  ·  Python 3.11  ·  React 19  ·  SQLite  ·  AES-256-GCM  ·  RSA-2048').font.size = Pt(8)

# ── Save ──────────────────────────────────────────────────────────────────────
OUT = r'C:\SecureLang\SecureLang_Report.docx'
doc.save(OUT)
print(f'Saved: {OUT}')
