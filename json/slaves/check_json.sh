#!/bin/bash

for f in *
do
    echo "$f"
    cat "$f" | json_verify
done
