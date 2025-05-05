from cookies_backpack.text_editor_interface import TextEditorInterface
from cookies_backpack.find_files import find_files
from cookies_backpack.openai_wrapper import OpenAIWrapper
from cookies_backpack.utils import download_pdf
import argparse
import os


def run_find_files(tei):
    args = {
        'target_dir': '~/workspace/cookipedia/',
        'keyword': 'setButtonOpenClose',
        'extensions': ['.html', '.js'],
    }
    tei.run_with_args(find_files, args, confirm=False)


def run_openai(tei):
    ai = OpenAIWrapper()
    tei.run(ai.request, template='鶏もも肉はどう料理するとよいですか。')


def run_download_pdf(tei):
    args = {
        'url': 'https://arxiv.org/pdf/1704.04110',
        'out_dir': os.path.dirname(tei.log_file),
    }
    tei.run_with_args(download_pdf, args)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--find_files', action='store_true')
    group.add_argument('-a', '--openai', action='store_true')
    group.add_argument('-d', '--download_pdf', action='store_true')
    args = parser.parse_args()

    true_flags = sum([args.find_files, args.openai, args.download_pdf])
    if true_flags != 1:
        parser.print_help()
        return

    work_dir = os.path.expanduser('~/.cb/')
    os.makedirs(work_dir, exist_ok=True)
    tei = TextEditorInterface(
        log_file=os.path.join(work_dir, 'log.txt'),
        text_editor='C:\\Program Files (x86)\\sakura\\sakura.exe',
    )
    if args.find_files:
        run_find_files(tei)
    if args.openai:
        run_openai(tei)
    if args.download_pdf:
        run_download_pdf(tei)
