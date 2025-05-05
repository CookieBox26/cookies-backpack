import requests
from urllib.parse import urlparse
import os


def get_filename_from_url(url):
    path = urlparse(url).path
    print(path)
    return os.path.basename(path)


def get_filename_from_header(resp):
    cd = resp.headers.get('Content-Disposition', '')
    print(cd)
    if 'filename=' in cd:
        filename = cd.split('filename=')[-1].strip('"').strip('\'')
        return filename
    return None


def download_pdf(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    resp = requests.get(url)
    if resp.status_code == 200 and 'application/pdf' in resp.headers.get('Content-Type', ''):
        filename = get_filename_from_header(resp)
        if not filename:
            filename = get_filename_from_url(url)
        out_file = os.path.join(out_dir, filename)
        with open(out_file, 'wb') as f:
            f.write(resp.content)
        print(f'Downloaded: {out_file}')
        # os.startfile(out_dir)
    else:
        raise Exception(
            'Failed to download PDF. '
            f'Status: {resp.status_code}, '
            f'Content-Type: {resp.headers.get("Content-Type")}'
        )
