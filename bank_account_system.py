"""Bank account management module."""

import hashlib
import os
import secrets

ACCOUNT_DATA = {}
SERVICE_FEE = 2.50


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create a new account and log it. Return False if the ID exists."""
    if transactions is None:
        transactions = []
    if acc_id in ACCOUNT_DATA:
        return False
    ACCOUNT_DATA[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


def deposit(acc_id, amount):
    """Add a positive amount to an account. Return True on success."""
    if amount <= 0 or acc_id not in ACCOUNT_DATA:
        return False
    ACCOUNT_DATA[acc_id]["balance"] += amount
    return True


def withdraw(acc_id, amount):
    """Withdraw amount plus the service fee. Return True on success."""
    if amount <= 0 or acc_id not in ACCOUNT_DATA:
        return False
    total = amount + SERVICE_FEE
    if ACCOUNT_DATA[acc_id]["balance"] < total:
        return False
    ACCOUNT_DATA[acc_id]["balance"] -= total
    return True


def compute_bonus(acc_id, rate):
    """Return the promotional bonus: balance multiplied by rate."""
    return ACCOUNT_DATA[acc_id]["balance"] * rate


def get_hash(pin, salt=None):
    """Return a salted PBKDF2-SHA256 hash of the PIN as 'salt:digest'."""
    if salt is None:
        salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, 600_000)
    return salt.hex() + ":" + digest.hex()


def generate_temp_pin():
    """Return a cryptographically secure 4-digit temporary PIN."""
    return secrets.randbelow(9000) + 1000


def backup_data(filename="backup.txt"):
    """Write the ledger to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(ACCOUNT_DATA))
    print("Backup complete:", filename)


def main():
    """Run a small demonstration of the account system."""
    admin_token = os.environ.get("BANK_ADMIN_TOKEN")
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", 0.05))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token is not None)


if __name__ == "__main__":
    main()
