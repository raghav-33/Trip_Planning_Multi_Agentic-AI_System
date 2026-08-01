import sys
import os
import runpy

# 1. Get the absolute paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AVIATION_SRC_DIR = os.path.join(CURRENT_DIR, "aviationstack-mcp", "src")

# 2. Force the source directory to the very front of Python's path
sys.path.insert(0, AVIATION_SRC_DIR)

# 3. Execute the module as if we typed 'python -m aviationstack_mcp'
if __name__ == "__main__":
    # We pass system arguments to the module so "mcp run" gets forwarded
    runpy.run_module("aviationstack_mcp", run_name="__main__")