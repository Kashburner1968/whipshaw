import os
import base64
import requests

# --- PLATFORM CONFIGURATION ---
TOKEN = os.getenv("GH_RAW_EXTRACTION_TOKEN")
OWNER = "Kashburner1968"
REPO = "whipshaw"
FILE_PATH = "pipeline_core.py"

# Targets the valid REST API framework endpoint, not the web domain
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def execute_patch():
    if not TOKEN:
        print("[CRITICAL] Aborted: GH_RAW_EXTRACTION_TOKEN environment variable not set.")
        return

    # Step 1: Retrieve current file content and structural object SHA metadata
    print("[1/3] Extracting file metadata and SHA from repository...")
    get_response = requests.get(API_URL, headers=HEADERS)
    
    if get_response.status_code != 200:
        print(f"[ERROR] Failed to fetch source file: {get_response.status_code} - {get_response.text}")
        return
        
    file_data = get_response.json()
    current_sha = file_data["sha"]
    
    # Decode full text layout to apply precise replacement strings
    decoded_text = base64.b64encode(base64.b64decode(file_data["content"])).decode("utf-8")
    raw_script = base64.b64decode(file_data["content"]).decode("utf-8")

    # Step 2: Swap out the broken logic structure cleanly
    broken_line = 'url = f"https://github.com{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"'
    fixed_line = 'url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"'
    
    if broken_line not in raw_script:
        print("[WARN] Target syntax mismatch. Forcing direct line split replacement loop...")
        lines = raw_script.splitlines()
        # Fallback tracking if indentation varies: line 47 maps to index 46
        if "url = f" in lines[46]:
            lines[46] = f"    {fixed_line.strip()}"
            updated_script = "\n".join(lines)
        else:
            print("[CRITICAL] Could not isolate target line context structure automatically.")
            return
    else:
        updated_script = raw_script.replace(broken_line, fixed_line)

    # Step 3: Re-encode clean script array and transmit to GitHub Gateway
    print("[2/3] Encapsulating updated script payload into Base64...")
    encoded_patch = base64.b64encode(updated_script.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": "Patch line 47: Correct base routing from web domain to API infrastructure",
        "content": encoded_patch,
        "sha": current_sha,
        "branch": "main"
    }
    
    print("[3/3] Transmitting payload to GitHub API gateway...")
    put_response = requests.put(API_URL, json=payload, headers=HEADERS)
    
    if put_response.status_code == 200:
        print(f"[SUCCESS] line 47 updated inside {FILE_PATH}. Commit: {put_response.json()['commit']['sha'][:7]}")
    else:
        print(f"[ERROR] API gateway rejected update matrix: {put_response.status_code} - {put_response.text}")

if __name__ == "__main__":
    execute_patch()
