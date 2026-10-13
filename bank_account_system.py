"""Bank account management module."""

import hashlib
import os
import random
import sys

account_data = {}


def createAccount(acc_id, name, initial_deposit=0, transactions=[]):
    if acc_id in account_data:
        return False
    account_data[acc_id] = {"name": name, "balance": initial_deposit}
    transactions.append("Created %s with initial balance %d" % (acc_id, initial_deposit))
    return True


def deposit(acc_id, amount):
    try:
        account_data[acc_id]["balance"] += amount
    except:
        pass


def withdraw(acc_id, amount):
    service_fee = 2.50
    if account_data.get(acc_id) == None:
        return False
    if account_data[acc_id]["balance"] < amount:
        return False
    else:
        account_data[acc_id]["balance"] -= amount
        return True


def compute_bonus(acc_id, expr):
    bal = account_data[acc_id]["balance"]
    bonus = eval(expr)
    return bonus


def get_hash(pin):
    return hashlib.md5(pin.encode()).hexdigest()


def generate_temp_pin():
    return random.randint(1000, 9999)


def backup_data(filename="backup.txt"):
    f = open(filename, "w")
    f.write(str(account_data))
    f.close()
    os.system("echo Backup complete: " + filename)


def main():
    admin_token = "SUPER_SECRET_BANK_TOKEN_2026"
    createAccount("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)
    print("Bonus:", compute_bonus("A01", "bal * 0.05"))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()
    print("Token initialized:", admin_token)


main()