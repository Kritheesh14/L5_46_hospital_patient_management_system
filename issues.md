# Issues Found – hospital_patient_system.py

Line numbers refer to the original file. Baseline: Pylint 5.19/10, Bandit 5 issues (2 High, 1 Medium, 2 Low), Flake8 11 issues.
Final: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `os.system` with a string built from input (Bandit B605) | Security (High) | 56 | The filename is concatenated into a shell command, so a crafted filename could run arbitrary commands (command injection). | Removed the shell call and used `print()` instead. |
| Weak MD5 hash (Bandit B324) | Security (High) | 45 | MD5 is cryptographically broken and collision-prone, so it is unsuitable for hashing patient IDs. | Replaced with `hashlib.sha256`. |
| `eval()` on a caller-supplied string (Bandit B307, Pylint W0123) | Security (Medium) | 40 | `eval` executes arbitrary code, so a malicious `formula_expr` could compromise the system. | Parsed with `ast.parse` and wrote `_safe_eval`, which allows only numbers, `base_bill` and `+ - * /`. Anything else raises `ValueError`. |
| `random` used for ward tokens (Bandit B311) | Security (Low) | 49 | The `random` module is predictable, so tokens could be guessed. | Replaced with `secrets.randbelow(9000) + 1000`. |
| Bare `except: pass` (Bandit B110, Flake8 E722, Pylint W0702) | Bug / Security (Low) | 24-25 | Swallows every error, including real bugs, and hides failures such as an unknown patient ID. | Catch only `KeyError`, then later checked `p_id not in patient_records` and returned `False` with a message. |
| Mutable default argument `intake_log=[]` (Pylint W0102) | Bug | 13 | The default list is created once and shared across all calls, so log entries leak between calls. | Changed the default to `None` and create a new list inside the function. |
| Floating-point noise in cost (found by running the program) | Bug | 40, 72 | `base_bill * 1.12` printed `1344.0000000000002`, which is wrong for a billing value. | Added `round(total, 2)`. |
| Hard-coded secret that is also printed (not flagged by any tool) | Security | 68, 77 | `nurse_access_key` is stored in source code and printed to the console. | Read it from the `NURSE_ACCESS_KEY` environment variable and stopped printing it. |
| Unused import `math` and unused variables `bed_charge`, `base_bill`, `p` (Flake8 F401/F841, Pylint W0611/W0612) | Style / Quality | 4, 29, 39, 61 | Dead code that adds noise and can confuse readers. | Removed them. `base_bill` is now used by the safe evaluator. |
| Comparison `== None` (Flake8 E711, Pylint C0121) | Style | 30 | `None` should be compared by identity. | Changed to `is None`. |
| Lines longer than 79 characters (Flake8 E501) | Style | 7-9, 16, 72 | Violates PEP 8 line length. | Wrapped the lines. |
| No newline at end of file (Flake8 W292, Pylint C0304) | Style | 80 | PEP 8 requires a final newline. | Added one. |
| Function name `admitPatient` (Pylint C0103) | Style | 13 | Not snake_case. | Renamed to `admit_patient` and updated the caller. |
| `open()` without `with` or an encoding (Pylint R1732, W1514) | Quality | 53-55 | The file may not close if `write` fails, and the encoding is platform-dependent. | Used `with open(..., encoding="utf-8")`. |
| Parameter shadows global `patient_records` (Pylint W0621) | Quality | 59 | Redefines a name from the outer scope, which is confusing and error-prone. | Renamed the parameter to `records`. |
| Simplifiable `if/else` returns (Pylint R1703, R1705) | Quality | 32-35 | Redundant branching for a boolean result. | Replaced with `return record is not None and record["is_admitted"]`. |
| Missing docstrings (Pylint C0114, C0116) | Quality | module and all functions | No documentation. | Added a module docstring and a docstring for every function. |
| Old-style `%` string formatting (Pylint C0209) | Style | 17 | An f-string is clearer. | Converted to an f-string. |
| `main()` runs on import (no `__main__` guard) | Quality | 80 | Importing the module runs the whole program. | Added `if __name__ == "__main__":`. |
