import json
import os
import sys
from jinja2 import Environment, FileSystemLoader
from validators import validate_cluster, ValidationError

TEMPLATE_DIR = "jinja2-templates"
OUTPUT_BASE_DIR = "generated-yaml-output"

if len(sys.argv) != 2:
    print("Usage: python render_yaml.py <path-to-json>")
    sys.exit(1)

INPUT_FILE = sys.argv[1]

if not os.path.exists(INPUT_FILE):
    print(f"ERROR: File not found → {INPUT_FILE}")
    sys.exit(1)

try:
    env_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]

    with open(INPUT_FILE) as f:
        data = json.load(f)

    cluster = data["cluster"]
    networking = data["networking"]
    nodes = data["nodes"]

    validate_cluster(networking, nodes)

    # OUTPUT_DIR = os.path.join(OUTPUT_BASE_DIR, env_name)
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    install_template = env.get_template("install-config.yaml.j2")
    agent_template = env.get_template("agent-config.yaml.j2")

    install_output = install_template.render(
        cluster=cluster,
        networking=networking,
        nodes=nodes
    )

    installfilename=f"{env_name}-install-config.yaml"
    
    with open(os.path.join(OUTPUT_BASE_DIR, installfilename), "w", encoding='utf-8') as f:
        f.write(install_output)

    agent_output = agent_template.render(
        cluster=cluster,
        networking=networking,
        nodes=nodes
    )

    agentfilename=f"{env_name}-agent-config.yaml"
    
    with open(os.path.join(OUTPUT_BASE_DIR, agentfilename), "w", encoding='utf-8') as f:
        f.write(agent_output)

    print(f"\n✅ YAML files generated → {OUTPUT_BASE_DIR}")

except ValidationError as e:
    print("\n❌ VALIDATION FAILED")
    print(str(e))
    sys.exit(1)

except Exception as e:
    print("\n❌ UNEXPECTED ERROR")
    print(str(e))
    sys.exit(1)