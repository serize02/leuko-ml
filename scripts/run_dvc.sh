#!/bin/bash
set -e

echo "[INFO] Waiting for server to become available..."
until curl -s http://server:8080/ping > /dev/null; do
  sleep 1
done

echo "[INFO] Server is up. Running DVC pipeline..."
dvc repro