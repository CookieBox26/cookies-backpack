from cookies_backpack.text_editor_interface import TextEditorInterface
from cookies_backpack.find_files import find_files
from cookies_backpack.download_pdf import download_pdf
from cookies_backpack.yukkuri import Yukkuri
from cookies_backpack.openai_wrapper import OpenAIWrapper
import toml
import argparse
import os


def run_find(tei):
    args = {
        'target_dir': '~/workspace/cookipedia/',
        'keyword': 'setButtonOpenClose',
        'extensions': ['.html', '.js'],
    }
    tei.run_with_args(find_files, args, confirm=False)


def run_pdf(tei):
    args = {
        'url': 'https://arxiv.org/pdf/1704.04110',
        'out_dir': os.path.dirname(tei.log_file),
        'title': 'DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks',
        'downloaded': 'xxxxxx.pdf',
    }
    tei.run_with_args(download_pdf, args, show=False)


def run_yukkuri(aquestalkplayer, tei):
    yukkuri = Yukkuri(aquestalkplayer, os.path.dirname(tei.log_file))
    sublog = os.path.join(os.path.dirname(tei.log_file), 'yukkuri.txt')
    tei.prepare_sublog(sublog)
    args = {'identifier': '', 'in_file': sublog}
    tei.run_with_args(yukkuri.synthesize, args, show=False)


def run_openai(tei):
    ai = OpenAIWrapper()
    tei.run(ai.request, template='鶏もも肉はどう料理するとよいですか。')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--find', action='store_true')
    group.add_argument('--pdf', action='store_true')
    group.add_argument('--yukkuri', action='store_true')
    group.add_argument('--openai', action='store_true')
    args = parser.parse_args()

    true_flags = sum([
        args.find,
        args.pdf,
        args.yukkuri,
        args.openai,
    ])
    if true_flags != 1:
        parser.print_help()
        return

    work_dir = os.environ.get('COOKIES_BACKPACK_WORK_DIR')
    if work_dir is None:
        work_dir = '~/.cb/'
    work_dir = os.path.expanduser(work_dir)
    os.makedirs(work_dir, exist_ok=True)

    text_editor = 'C:\\Windows\\System32\\notepad.exe'
    conf_toml = os.path.join(work_dir, 'config.toml')
    if os.path.isfile(conf_toml):
        conf = toml.load(conf_toml)
        if 'text_editor' in conf:
            text_editor = conf['text_editor']

    tei = TextEditorInterface(
        log_file=os.path.join(work_dir, 'log.txt'),
        text_editor=text_editor,
    )
    if args.find:
        run_find(tei)
    if args.pdf:
        run_pdf(tei)
    if args.yukkuri:
        run_yukkuri(
            os.path.expanduser('~/aquestalkplayer/AquesTalkPlayer.exe'),
            tei,
        )
    if args.openai:
        run_openai(tei)
