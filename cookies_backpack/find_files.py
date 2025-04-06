"""
指定の文字列を含むファイルを探します。
python find_files.py ./space2/cookipedia/ setButtonOpenClose .html .js
"""
import os
import argparse


def find_files(target_dir: str, keyword: str, extensions: list[str]) -> list[str]:
    """指定の文字列を含むファイルを探します。

    Args:
        target_dir: 探索するルートディレクトリ
        extensions: 探すファイルの拡張子のリスト（例: ['.txt', '.md']）
        keyword: 検索する文字列

    Returns:
        条件に合致したファイルのパスのリスト
    """
    matched_files = []
    for root, _, files in os.walk(os.path.expanduser(target_dir)):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if keyword in f.read():
                            matched_files.append(file_path)
                except (UnicodeDecodeError, FileNotFoundError):
                    # バイナリや開けないファイルを無視
                    continue
    return matched_files


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_dir')
    parser.add_argument('keyword')
    parser.add_argument('extensions', nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    results = find_files(args.target_dir, args.keyword, args.extensions)
    for path in results:
        print(path)
