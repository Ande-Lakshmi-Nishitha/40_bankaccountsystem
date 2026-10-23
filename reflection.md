# Reflection

**1. Which tool caught the most important issues?**
Bandit. Its High findings (MD5 hashing and os.system) and the eval call were the real security risks. Pylint reported the most items overall, mostly quality problems, and was the only tool to flag the mutable default argument (W0102). Flake8 found style problems and some dead code.

**2. Any false positives or hard-to-interpret findings?**
B105 fired because of the variable name "admin_token". It was a real hardcoded secret here, but Bandit matches on names, so it can false-positive. Pylint and Flake8 reported `bal` as unused only because eval hid its use; removing eval resolved that confusion.

**3. How would you use these tools in a workflow?**
Run Flake8 and Pylint in a pre-commit hook and in CI, run Bandit in CI, and fail the build on High or Medium Bandit findings. Treat Pylint as a score threshold such as 9.5.

**4. What did static analysis improve?**
Bandit went from 6 findings to 0, Flake8 from 7 to 0, and Pylint from 5.62 to 10.00. It also exposed a real logic bug: the service fee was never charged. The tools did not notice that withdraw's result is ignored in main, so I still had to run the program and read its output.