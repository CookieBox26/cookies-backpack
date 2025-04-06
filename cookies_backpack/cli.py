from cookies_backpack.text_editor_interface import TextEditorInterface
from cookies_backpack.find_files import find_files
from cookies_backpack.openai_wrapper import OpenAIWrapper
import argparse


def run_find_files():
    tei = TextEditorInterface()
    args = {
        'target_dir': '~/space2/cookipedia/',
        'keyword': 'setButtonOpenClose',
        'extensions': ['.html', '.js'],
    }
    tei.run_with_args(find_files, args)


def run_openai():
    ai = OpenAIWrapper()
    tei = TextEditorInterface()
    tei.run(ai.request, template='鶏もも肉はどう料理するとよいですか。')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--find_files', action='store_true')
    group.add_argument('-a', '--openai', action='store_true')
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
    if args.find_files:
        run_find_files()
    if args.openai:
        run_openai()
