#!/usr/bin/env python3
import sys
import json

# Fields we want to drop from metadata
DROP_FIELDS = {
    "creationTimestamp",
    "resourceVersion",
    "uid",
    "generation",
    "managedFields",
    "selfLink",
}

def clean_k8s_obj(obj):
    if "metadata" in obj:
        for f in DROP_FIELDS:
            obj["metadata"].pop(f, None)
        # Remove noisy annotations if present
        if "annotations" in obj["metadata"]:
            obj["metadata"]["annotations"].pop("kubectl.kubernetes.io/last-applied-configuration", None)
            if not obj["metadata"]["annotations"]:
                obj["metadata"].pop("annotations")
    return obj

if __name__ == "__main__":
    data = json.load(sys.stdin)
    data = clean_k8s_obj(data)
    json.dump(data, sys.stdout, indent=2)
