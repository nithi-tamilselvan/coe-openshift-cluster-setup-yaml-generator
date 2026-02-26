import sys
import subprocess

if len(sys.argv) != 2:
    print("Usage: python generate.py <env.json>")
    sys.exit(1)

env_file = sys.argv[1]

subprocess.run(["python", "render_yaml.py"], check=True)