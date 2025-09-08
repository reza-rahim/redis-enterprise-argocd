#!/usr/bin/env python3
import sys
import yaml  # pip install pyyaml

def clean_k8s_obj(obj, name: str):
    # Drop full metadata
    obj.pop("metadata", None)
    # Add back only minimal metadata with name
    obj["metadata"] = {"name": name}
    return obj

if __name__ == "__main__":
    data = yaml.safe_load(sys.stdin)     # read YAML from stdin
    # Replace with your secret name
    secret_name = "my-secret"
    data = clean_k8s_obj(data, secret_name)
    yaml.safe_dump(
        data,
        sys.stdout,
        sort_keys=False,
        default_flow_style=False
    )

