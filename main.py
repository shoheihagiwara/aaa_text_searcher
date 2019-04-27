"""aaa.txtを簡単に目的のものを検索する。

複数の単語を入力し、50行中でそれらの単語がいくつ出てくるかをチェックし、
多い順に行番号を出力する。
"""

import tkinter as tk
import os

PATH = 'test_data/aaa.txt'
ENCODING = 'utf-8'
SEARCH_STEP = 30
TOP_N = 3
SEARCH_KEY_BINDING = '<Control-Key-f>'

class AaaTxtSearcher(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("900x400")
        self.query = tk.Text(height=5)
        self.answer = tk.Text()
        self.search_btn = tk.Button(self, text='Search ' + SEARCH_KEY_BINDING, command=self.search)
        self.query.bind(SEARCH_KEY_BINDING, self.search)
        self.clear_btn = tk.Button(self, text='Clear', command=self.clear_query)
        self.query.pack(fill=tk.BOTH, expand=True)
        self.search_btn.pack()
        self.clear_btn.pack()
        self.answer.pack(fill=tk.BOTH, expand=True)
        self.query.focus_set()

    @staticmethod
    def __count_words_in_lines(words, lines):
        """検索対象の単語の出現回数を返す

        大文字小文字は関係なく検索する。

        :param words: 検索対象の単語
        :param lines: ここから検索対象の単語を探す
        :return: 合計でいくつ見つかったか。
        """

        count = 0
        for word in words:
            for line in lines:
                count += line.upper().count(word.upper())

        return count

    def search(self, event=None):

        # 単語を読み込んでリストにする
        search_word_list = self.query.get('1.0', tk.END).split()

        if len(search_word_list) == 0:
            return

        with open(PATH, encoding=ENCODING) as f:

            lines = f.readlines()

            # 検索対象単語が一番多く出現する範囲を見つける
            running_best_score = None
            running_best_score_start_line_num = None
            ranking = []
            for start_line_num in range(0, len(lines), SEARCH_STEP):
                end_line_num = start_line_num + SEARCH_STEP if start_line_num + SEARCH_STEP < len(lines) else len(lines) -1
                tmp_count = self.__count_words_in_lines(search_word_list, lines[start_line_num:end_line_num])

                ranking.append((tmp_count, "".join(lines[start_line_num:end_line_num])))

                if tmp_count > 0 and (running_best_score is None or tmp_count > running_best_score):
                    running_best_score = tmp_count
                    running_best_score_start_line_num = start_line_num

            self.answer.delete('1.0', tk.END)

            # 見つけた結果を表示する。
            if running_best_score is None:
                result = ''
            else:
                start = running_best_score_start_line_num
                end = running_best_score_start_line_num + SEARCH_STEP - 1
                result = ''.join(lines[start:end])

            ranking.sort(key=lambda tup: tup[0], reverse=True)

            result_list = [tuple[1] for tuple in ranking[0:TOP_N]]
            line_delimiter = os.linesep + '*' * 80 + os.linesep * 2
            result = line_delimiter.join(result_list)

            self.answer.insert('1.0', result)

    def clear_query(self):
        print('clearing query.')
        self.query.delete('1.0', tk.END)


if __name__ == '__main__':

    app = AaaTxtSearcher()
    app.mainloop()


