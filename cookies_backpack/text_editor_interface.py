"""
テキストエディタへの入力を促し、処理関数に渡した結果を表示します。
"""
import subprocess
import datetime
import toml
from typing import Callable, Optional


class TextEditorInterface:
    def __init__(self):
        self.text_editor = 'C:\\Program Files (x86)\\sakura\\sakura.exe'
        self.log_file = 'log.txt'

    def get_query(self, mark_query, template=''):
        with open(self.log_file, mode='a', encoding='utf8', newline='\n') as ofile:
            ofile.write(mark_query + '\n' + template)
        subprocess.run([self.text_editor, self.log_file])

        user_input = input('Press Enter to continue or type `q` to quit: ')
        if user_input == 'q':
            return ''

        flag = False
        query = ''
        with open(self.log_file, mode='r', encoding='utf8') as ifile:
            for line in ifile:
                if flag:
                    query += line
                elif line.strip() == mark_query.strip():
                    flag = True
        return query

    def write_and_show_response(self, mark_resp, resp):
        with open(self.log_file, mode='a', encoding='utf8', newline='\n') as ofile:
            ofile.write(f'{mark_resp}\n{resp}\n')
        subprocess.Popen([self.text_editor, self.log_file])

    def run(
        self,
        func: Callable,
        template: str = '',
        parser: Optional[Callable[[str], object]] = None,
        kwargs: bool = False
    ) -> None:
        """テキストエディタへの入力を促し、処理関数に渡した結果を表示します。

        Args:
            func: 目的の処理関数。
            template: 入力テンプレート。
            parser: 入力をパースする関数。None の場合は入力文字列をそのまま処理関数に渡します。
            kwargs: True の場合、パース後の入力をキーワード引数として展開して処理関数に渡します。

        Returns:
            None
        """
        dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mark_query = f'# {dt_now} QUERY'
        mark_resp = f'# {dt_now} RESPONSE'
        query = self.get_query(mark_query, template)
        if query == '':
            return
        if parser is not None:
            query = parser(query)
        resp = func(query) if not kwargs else func(**query)
        self.write_and_show_response(mark_resp, resp)

    def run_with_args(self, func, args):
        self.run(func, template=toml.dumps(args), parser=toml.loads, kwargs=True)


if __name__ == '__main__':
    tei = TextEditorInterface()
    def func(apple=200, banana=100):
        return apple + banana
    tei.run_with_args(func, {'apple': 200, 'banana': 100})
