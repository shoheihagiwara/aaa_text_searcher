#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""aaa.txtを簡単に目的のものを検索する。

複数の単語を入力し、50行中でそれらの単語がいくつ出てくるかをチェックし、
多い順に行番号を出力する。
"""

import tkinter as tk
import os
from functools import reduce

PATH = 'test_data/aaa.txt'
ENCODING = 'utf-8'
SEARCH_STEP = 50
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
        ただし、大文字で検索したときには、区別して検索する。

        :param words: 検索対象の単語
        :param lines: ここから検索対象の単語を探す
        :return: 合計でいくつ見つかったか。
        """

        count = 0
        for word in words:
            for line in lines:
                if word.isupper():
                    count += line.count(word)
                else:
                    count += line.lower().count(word.lower())

        return count

    @staticmethod
    def __calc_math_val(words, lines):
        """calclate match value.

        match value is defined as follows.

        マッチ度 = Π( M(i) )
        M(i) = 検索ワードのi番目についてのテキストのマッチ度を表す。 = 1 + h
            h: ヒット係数。マックス5回で、ヒットするたびに高くなる。5以上は変わらない。
                ヒット回数    0  1  2  3  4  5  6  7 ...  n
                h       -0.2 .1 .2 .3 .4 .5 .5 .5 ... .5

        :param words:
        :param lines:
        :return:
        """


        match_val_for_each_word = []

        for each_word in words:
            word_count = AaaTxtSearcher.__count_words_in_lines([each_word], lines)
            if word_count == 0:
                coefficient = -0.2
            elif word_count > 5:
                coefficient = 0.5
            else:
                coefficient = word_count / 10
            match_val_for_each_word.append(1 + coefficient)

        return reduce(lambda x, y: x*y, match_val_for_each_word)


    def search(self, event=None):
        """検索
        """

        # 単語を読み込んでリストにする
        search_word_list = self.query.get('1.0', tk.END).split()

        if len(search_word_list) == 0: 
            return

        with open(PATH, encoding=ENCODING) as f:

            aaa_txt_lines = f.readlines()

            # マッチ度をだす。
            running_best_score = None
            running_best_score_start_line_num = None
            ranking = []
            for start_line_num in range(0, len(aaa_txt_lines), SEARCH_STEP):
                end_line_num = start_line_num + SEARCH_STEP if start_line_num + SEARCH_STEP < len(aaa_txt_lines) else len(aaa_txt_lines) -1
                match_val = self.__calc_math_val(search_word_list, aaa_txt_lines[start_line_num:end_line_num])

                ranking.append((match_val, "".join(aaa_txt_lines[start_line_num:end_line_num]), start_line_num, end_line_num))

                if match_val > 0 and (running_best_score is None or match_val > running_best_score):
                    running_best_score = match_val
                    running_best_score_start_line_num = start_line_num

            self.answer.delete('1.0', tk.END)

            # 見つけた結果を表示する。
            if running_best_score is None:
                result = ''
            else:
                start = running_best_score_start_line_num
                end = running_best_score_start_line_num + SEARCH_STEP - 1
                result = ''.join(aaa_txt_lines[start:end])

            ranking.sort(key=lambda tup: tup[0], reverse=True)

            for each_ranking_entry in ranking:
                match_val = each_ranking_entry[0]
                start_line_num = each_ranking_entry[2]
                print("match val: [{}] start line number: [{}]".format(match_val, start_line_num))

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


