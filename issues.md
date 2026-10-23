# Static Analysis Issue Report: bank_account_system.py

Line numbers refer to the original file (see `reports/before/`).

## Summary

| Tool | Before | After |
|---|---|---|
| Pylint | 5.62/10 (21 messages) | 10.00/10 (0 messages) |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 7 findings | 0 findings (empty report) |

## Issues found by the tools

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|---|
| 1 | MD5 used to hash PINs | Security: Bandit B324 (High) | 44 | MD5 is a broken, unsalted hash and unsuitable for PINs | Commit 1: PBKDF2-HMAC-SHA256 with a random 16-byte salt, stored as `salt:digest` |
| 2 | Shell command built from a string | Security: Bandit B605 (High) | 55 | `os.system("echo ..." + filename)` allows shell injection through the filename | Commit 1: removed the shell call and used `print()` |
| 3 | `eval()` on caller-supplied text | Security: Bandit B307 (Medium), Pylint W0123 | 39 | Arbitrary code execution through the `expr` argument | Commit 1: `compute_bonus` takes a numeric `rate` and returns `bal * rate` |
| 4 | Unused variable `bal` | Dead code: Flake8 F841, Pylint W0612 | 38 | `bal` was only "used" inside the `eval` string, so the tools saw it as unused | Fixed by removing `eval`: `bal` is now used directly (commit 1) |
| 5 | Predictable random for the temp PIN | Security: Bandit B311 (Low) | 48 | `random.randint` is not cryptographically secure | Commit 1: `secrets.randbelow(9000) + 1000` |
| 6 | Hardcoded admin token | Security: Bandit B105 (Low) | 59 | Secret stored in source code and printed to the console | Commit 1: read from the `BANK_ADMIN_TOKEN` environment variable; print only whether it is set |
| 7 | Bare `except` with `pass` | Bug: Bandit B110 (Low), Flake8 E722, Pylint W0702 | 22 | Swallows every error, so a failed deposit is silent and returns `None` | Commit 1: `except KeyError`, return `False`; commit 3: validate the amount and account up front |
| 8 | Mutable default argument | Bug: Pylint W0102 | 11 | `transactions=[]` is shared across calls | Commit 3: default `None`, create the list inside the function |
| 9 | `service_fee` assigned but never used | Logic bug: Flake8 F841, Pylint W0612 | 27 | The withdrawal fee was never charged, so balances and the bonus were wrong | Commit 2: fee applied in `withdraw`; commit 3: moved to the `SERVICE_FEE` constant |
| 10 | Comparison to `None` with `==` | Style: Flake8 E711, Pylint C0121 | 28 | Should use identity, not equality | Commit 2: `is None`; commit 3: `acc_id not in ACCOUNT_DATA` |
| 11 | Unused import `sys` | Style: Flake8 F401, Pylint W0611 | 6 | Dead import | Commit 2: removed |
| 12 | Line too long (89 > 79) | Style: Flake8 E501 | 15 | Exceeds the PEP 8 line limit | Commit 2: wrapped the call in parentheses |
| 13 | No newline at end of file | Style: Flake8 W292, Pylint C0304 | 70 | File did not end with a newline | Commit 2: file ends with a single newline |
| 14 | Unnecessary `else` after `return` | Quality: Pylint R1705 | 30 | Extra nesting that adds nothing | Commit 3: removed the `else` and de-indented |
| 15 | Missing function docstrings (8 functions) | Quality: Pylint C0116 | 11, 19, 26, 37, 43, 47, 51, 58 | No documentation for any function | Commit 3: added a one-line docstring to each function |
| 16 | Function name not snake_case | Quality: Pylint C0103 | 11 | `createAccount` breaks the naming convention | Commit 3: renamed to `create_account` (global renamed to `ACCOUNT_DATA`) |
| 17 | `%` string formatting | Quality: Pylint C0209 | 15 | Old-style formatting | Commit 3: f-string |
| 18 | File opened without `with` or an encoding | Quality: Pylint R1732, W1514 | 52 | The file can leak if `write` fails, and the encoding depends on the platform | Commit 3: `with open(filename, "w", encoding="utf-8")` |

## Problems found by running and reading the code (no tool flagged these)

| Issue | Description | Fix Approach |
|---|---|---|
| `deposit` and `withdraw` accepted zero or negative amounts | A negative deposit would reduce the balance | Commit 3: reject `amount <= 0` and unknown accounts, returning `False` |
| `main()` ran on import | Importing the module had side effects | Commit 3: `if __name__ == "__main__":` guard |
| Secret printed by the program | The token was printed in plain text | Commit 1: token no longer printed |

## Verification

Reports are saved in `reports/before/` and `reports/after/`.

- `pylint_report.txt`: 5.62/10 before, 10.00/10 after.
- `bandit_report.txt`: 6 issues before, "No issues identified" after.
- `flake8_report.txt`: 7 findings before; the after report is empty because there are no findings.
- Behavior change: the bonus is now 64.875 instead of 65.0, because the service fee is charged.