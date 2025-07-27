import requests
import re
import os
import base64
import uuid

# === CONFIG ===
## token isi disini
REPO_NAME = 'andikaap99/asset'
BRANCH = 'main'
TARGET_FOLDER = ''

def get_drive_file_id(drive_link):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_link)
    return match.group(1) if match else None

def download_drive_file(file_id):
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    session = requests.Session()
    response = session.get(download_url, stream=True)

    # Handle large files with confirm token
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            download_url = f'https://drive.google.com/uc?export=download&confirm={value}&id={file_id}'
            response = session.get(download_url, stream=True)
            break

    filename = f"{file_id}_{uuid.uuid4().hex[:8]}.tmp"
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(32768):
            f.write(chunk)

    print(f"Downloaded: {filename}")
    return filename

def upload_to_github(file_path, target_path):
    with open(file_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')

    url = f'https://api.github.com/repos/{REPO_NAME}/contents/{target_path}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    data = {
        'message': f'Add {os.path.basename(file_path)}',
        'content': content,
        'branch': BRANCH,
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Uploaded to GitHub successfully!")
        return response.json()['content']['download_url']
    else:
        print(f"Failed to upload: {response.status_code} - {response.text}")
        return None

def convert_drive_link(drive_link: str) -> str:
    file_id = get_drive_file_id(drive_link)
    if not file_id:
        raise ValueError("Invalid Google Drive link.")
    
    downloaded_file = download_drive_file(file_id)
    target_path_in_repo = f"{TARGET_FOLDER}{os.path.basename(downloaded_file)}"
    direct_github_url = upload_to_github(downloaded_file, target_path_in_repo)

    # Hapus file sementara
    os.remove(downloaded_file)

    if direct_github_url:
        return direct_github_url
    else:
        raise ValueError("Failed to upload to GitHub.")

def convert_drive_link_pdf(drive_link: str) -> str:
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/file/d/{file_id}/preview"
    return drive_link
