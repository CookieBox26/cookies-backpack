import requests
from urllib.parse import urlparse
import os
import toml
import fitz  # PyMuPDF
# from . import _extra ImportError: DLL load failed while importing _extra -->
# https://pymupdf.readthedocs.io/en/latest/installation.html#problems-after-installation
from cookies_backpack.format_paper_text import format_paper_text


def _get_filename(url, resp):
    cd = resp.headers.get('Content-Disposition', '')
    if 'filename=' in cd:
        filename = cd.split('filename=')[-1].strip('"').strip('\'')
        return filename
    path = urlparse(url).path
    return os.path.basename(path)


def _read_cache(cache_file):
    if not os.path.isfile(cache_file):
        return {}
    with open(cache_file, encoding='utf8', newline='\n') as ifile:
        cache = toml.load(ifile)
    return cache


def _write_cache(cache_file, cache):
    with open(cache_file, mode='w', encoding='utf8', newline='\n') as ofile:
        cache = toml.dump(cache, ofile)


def _download_pdf_impl(url, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cache_file = os.path.join(out_dir, 'cached_pdfs.toml')
    cache = _read_cache(cache_file)

    if url in cache:
        print(f'Already Downloaded: {cache[url]}')
        return cache[url]

    resp = requests.get(url)
    if resp.status_code == 200 and 'application/pdf' in resp.headers.get('Content-Type', ''):
        filename = _get_filename(url, resp)
        out_file = os.path.join(out_dir, filename)
        with open(out_file, 'wb') as f:
            f.write(resp.content)
        print(f'Downloaded: {out_file}')
        cache[url] = out_file
        _write_cache(cache_file, cache)
        return out_file
    else:
        raise Exception(
            'Failed to download PDF. '
            f'Status: {resp.status_code}, '
            f'Content-Type: {resp.headers.get("Content-Type")}'
        )


def download_pdf(url, out_dir, title, paper=True):
    out_file = _download_pdf_impl(url, out_dir)
    raw_txt_file = out_file.replace('.pdf', '.raw.txt')
    formatted_txt_file = out_file.replace('.pdf', '.formatted.txt')
    if not os.path.isfile(raw_txt_file):
        text = ''
        with fitz.open(out_file) as doc:
            for page in doc:
                text += page.get_text()
        with open(raw_txt_file, mode='w', encoding='utf8', newline='\n') as ofile:
            ofile.write(text)
    if paper:
        format_paper_text(raw_txt_file, formatted_txt_file, title)
    os.startfile(out_dir)
