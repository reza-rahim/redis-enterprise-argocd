#!/usr/bin/env python3
import sys
import yaml  # pip install pyyaml

def clean_k8s_obj(obj):
    # Extract original name if present
    name = obj.get("metadata", {}).get("name", "my-secret")
    # Drop all metadata
    obj.pop("metadata", None)
    # Add back only minimal metadata with the name
    obj["metadata"] = {"name": name}
    return obj

if __name__ == "__main__":
    data = yaml.safe_load(sys.stdin)     # read YAML from stdin
    data = clean_k8s_obj(data)
    yaml.safe_dump(
        data,
        sys.stdout,
        sort_keys=False,
        default_flow_style=False
    )


