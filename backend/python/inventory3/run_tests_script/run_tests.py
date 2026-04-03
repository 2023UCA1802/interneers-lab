import subprocess
import sys

print("Running regression tests...\n")

result = subprocess.run([sys.executable, "manage.py", "test"])

if result.returncode == 0:
    print("All tests passed")
else:
    print("Tests failed")
    sys.exit(1)