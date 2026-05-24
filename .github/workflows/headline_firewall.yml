name: 🤖 Automated Headline Learning Loop Firewall

on:
  schedule:
    - cron: '0 * * * *'
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  execute-firewall:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: 📥 Check out Repository Workspace
        uses: actions/checkout@v4

      - name: 🐍 Initialize Python Runtime Environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: 📦 Install Required Data Visualization Packages
        run: |
          python -m pip install --upgrade pip
          pip install matplotlib

      - name: 🔍 Debug Directory Contents
        run: |
          echo "=== Displaying all files checked out in runner ==="
          ls -la

      - name: ⚙️ Execute Headline Verification and Decoupling Matrix
        run: |
          # If file is named slightly differently, this diagnostic lookahead prevents crashing
          if [ -f "headline_manipulation_firewall.py" ]; then
            python headline_manipulation_firewall.py
          elif [ -f "headline_learning_loop.py" ]; then
            python headline_learning_loop.py
          else
            echo "❌ ERROR: No matching firewall python script found in root directory!"
            exit 1
          fi

      - name: 🚀 Commit and Push Updated Telemetry to Learning Loop
        run: |
          git config --global user.name "GitHub Actions Bot"
          git config --global user.email "actions@github.com"
          
          git add headline_decoupling_matrix.json headline_decoupling_telemetry.png || true
          git add headline_manipulation_log.json structural_divergence_telemetry.png || true
          
          if git diff-index --quiet HEAD --; then
            echo "No structural discrepancies detected. Learning loop matrix is currently stable."
          else
            git commit -m "🤖 [SYSTEMIC AUTOMATION]: Ingested new headline telemetry - Adjusted alignment reward map"
            git push origin main
          fi
