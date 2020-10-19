
"""  Run script to parse a vietnamese text

- set variables DEBUG, PLOT, TEST based on your use case.
- set variable file to the filename you want to analyze
- Run:
   - Will create a report of distribution of sounds
   - Will plot if you set PLOT=True
"""
import numpy as np
import time
import os
import matplotlib.pyplot as plt
from datetime import date

today = date.today().strftime("%b-%d-%Y")

DEBUG = True  # Print more information
PLOT = True  # Plot data
TEST = True  # Use test case instead of file

testcase = ['nguyễn, nhanh, giường',
            'nghiêng, hoàng']


idt = ' ' * 2  # Set indent level
# Vowel list: Index  = 6 * vowel + accent
vowels = ['e', 'ẹ', 'ẻ', 'ẽ', 'è', 'é',
          'ê', 'ệ', 'ể', 'ễ', 'ề', 'ế',
          'a', 'ạ', 'ả', 'ã', 'à', 'á',
          'ă', 'ặ', 'ẳ', 'ẵ', 'ằ', 'ắ',
          'â', 'ậ', 'ẩ', 'ẫ', 'ầ', 'ấ',
          'i', 'ị', 'ỉ', 'ĩ', 'ì', 'í',
          'o', 'ọ', 'ỏ', 'õ', 'ò', 'ó',
          'ô', 'ộ', 'ổ', 'ỗ', 'ồ', 'ố',
          'ơ', 'ợ', 'ở', 'ỡ', 'ờ', 'ớ',
          'u', 'ụ', 'ủ', 'ũ', 'ù', 'ú',
          'ư', 'ự', 'ử', 'ữ', 'ừ', 'ứ',
          'y', 'ỵ', 'ỷ', 'ỹ', 'ỳ', 'ý']
# Digraph list.
digraph = ['ch', 'gh', 'gi', 'kh', 'nh',
           'ng', 'ph', 'th', 'tr', 'qu']
# Everything else, log counts into dictionaries (key=character, value=count)
consonants = {}
Nchar = 0  # Keeps track of total character count

# initialize counts into numpy matrix for easy data processing later.
vowel_cnt = np.zeros((int(len(vowels) / 6), 6))
vowel_cnt_reduced = np.sum(vowel_cnt, axis=1)
digraph_cnt = np.zeros(len(digraph))

file = 'anh_hung_xa_dieu_chuong1.txt'  # long text
#file = 'test1.txt'  # Short text, uncomment this for small test

print('=' * 79)
print('\n Running program! Put program name here \n')
print('=' * 79)
if os.path.exists(file):
    fsize = os.path.getsize(file)
    print('Parse text:')
    print(idt + 'Parsing text file: %s (%.3f MB)' % (file, fsize / 1e6))
    with open(file, encoding="utf8") as f:
        tic = time.time()
        # Open text file as utf-8 (unicode) and break down into words
        if TEST:
            # Substitute test case if testing
            f = testcase
        for line in f:
            # convert to lower case
            line = line.strip()
            line = line.lower()
            # Split to words
            words = line.split()
            # Only keep alpha-numeric characters
            words = [''.join(filter(str.isalnum, w)) for w in words]
            # Parse words
            for w in words:
                if DEBUG:
                    print('-' * 79)
                    print('Parsing word "%s"' % w)
                # Parse digraphs first
                if len(w) > 2:
                    # Check if starts with digraph
                    if w[:2] in digraph:
                        digraph_cnt[digraph.index(w[:2])] += 1
                        if DEBUG:
                            print('Found beginning digraph %s' % w[:2])
                        Nchar += 1
                        # Chop off the beginning digraph
                        if w[:3] in ['ngh']:
                            # h is part of ng
                            w = w[3:]
                        else:
                            w = w[2:]
                    # Check if ends with digraph
                    if len(w) >= 2:
                        if w[-2:] in digraph:
                            digraph_cnt[digraph.index(w[-2:])] += 1
                            if DEBUG:
                                print('Found ending digraph %s' % w[-2:])
                            Nchar += 1
                            # Chop off ending digraph
                            w = w[:-2]
                # Parse remaining letters
                for char in w:
                    Nchar += 1
                    if char in vowels:
                        # Get index of vowel, row & column
                        idx_char = vowels.index(char)
                        idx, idy = int(idx_char / 6), idx_char % 6
                        vowel_cnt[idx, idy] += 1
                        if DEBUG:
                            print('vowel %s' % vowels[6 * idx])
                    else:
                        if DEBUG:
                            print('consonant %s' % char)
                        if char in consonants:
                            consonants[char] += 1
                        else:
                            consonants[char] = 1
        toc = time.time()
        print(idt + 'Finished parsing %d characters in %.4f s' %
              (Nchar, toc - tic))
        # Create reduced vowel report by flatting 1 dimension of the matrix
        vowel_cnt_reduced = np.sum(vowel_cnt, axis=1)
        # Print report
        print('-' * 79)
        print('Reporting vowels (% of total sounds)')
        print('(digraphs like %s, etc. count as 1 sound)' % digraph[0])
        for ii, cnt in enumerate(vowel_cnt_reduced):
            print(idt + '%s : %.1f %% (count = %d)' % (vowels[ii * 6],
                                                       cnt / Nchar * 100,
                                                       cnt))
        print('Reporting digraphs & consonants:')
        for ii, cnt in enumerate(digraph_cnt):
            print(idt + '%s : %.1f %% (count = %d)' % (digraph[ii],
                                                       cnt / Nchar * 100,
                                                       cnt))
        for k, v in consonants.items():
            print(idt + '%s : %.1f %% (count = %d)' % (k,
                                                       v / Nchar * 100,
                                                       v))
    if PLOT:
        # Compile labels (characters)
        vowel_raw = [vowels[6 * ii] for ii in range(len(vowel_cnt_reduced))]
        labels = []
        labels += vowel_raw
        labels += digraph
        labels += list(consonants.keys())
        # Compile counts
        cnts = list(vowel_cnt_reduced) + list(digraph_cnt) +\
               list(consonants.values())
        percent = np.array(cnts) / Nchar * 100.0
        # Sort data
        percent, cnts, labels = (list(t) for t in zip(*sorted(zip(percent,
                                                                  cnts,
                                                                  labels),
                                                              reverse=True)))
        # Plot bar graph, sort by frequency
        bar_width = 0.5
        ind = np.arange(len(cnts))
        plt.figure(figsize=(13, 6))
        plt.bar(ind, percent, bar_width, label='distribution')
        plt.title('File analyzed: ' + file)
        plt.xticks(ind, labels, fontsize=7)
        plt.legend()
        plt.grid(alpha=0.3)
        plt.ylabel('% of sounds')
        plt.xlabel('sound')
        mdata = {'today': today,
                 'Num Sounds': Nchar}
        mdata_str = ['%s: %s' % (k, v) for k, v in mdata.items()]
        mdata_str = '\n'.join(mdata_str)
        ax = plt.gca()
        # Add metadatabox
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.7, 0.6, mdata_str, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)

        # Plot 2-d distribution of vowels
        # Create figure
        fig = plt.figure(figsize=(9, 9))
        ax = fig.add_subplot(111, projection='3d')
        percent_vowels = vowel_cnt / np.sum(vowel_cnt_reduced) * 100.0
        # Set up axis labels
        accents = ['none', '.', '?', '~', '`', '´']
        colors = ['y', 'r', 'b', 'g', 'c', 'k']
        # Gather some data
        dx, dy = percent_vowels.shape
        yticks = np.arange(dy)
        yticks = yticks[::-1]
        # For each layer of bar graph, set a color
        for idy, c, k in zip(np.arange(dy), colors, yticks):
            xs = np.arange(dx)  # x-axis length
            ys = percent_vowels[:, idy]  # vowels plotted against x axis
            cs = [c] * len(xs)  # Color of given layer
            # Plot the bar graph given by xs and ys on the plane y=k
            ax.bar(xs, ys, zs=k, zdir='y', color=cs, alpha=0.8)
        # Label your axis
        ax.set_xlabel('vowel')
        ax.set_ylabel('accent')
        ax.set_zlabel('percent of vowels')
        # label accent/vowels on axis
        ax.set_xticks(np.arange(dx))
        ax.set_yticks(np.arange(dy))
        ax.set_yticklabels(accents, fontsize=20)
        ax.set_xticklabels(vowel_raw, fontsize=12)
        ax.set_title('File analyzed: %s' % file)
        ax.grid(alpha=0.3)
else:
    print('!' * 79)
    print('!' * 25 + ' ' * 10 + 'ERROR' + ' ' * 10 + '!' * 29)
    print("file %s does not exist" % file)
    print()
