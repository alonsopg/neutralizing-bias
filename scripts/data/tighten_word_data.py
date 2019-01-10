"""
take word data (output of gen_data_from_crawl.py >>> gen_corpus_data.sh) and
only take the examples where a SINGLE phrase or NOTHING is in the post

TODO incorporate this as a filtering step into gen_data_from_crawl.py


python tighten_word_data.py ../../data/v4/word/biased.test.pre ../../data/v4/word/biased.test.post ../../data/v5/word_tight/biased.test

"""


from simplediff import diff
import sys

pre_fp = sys.argv[1]
post_fp = sys.argv[2]
out_prefix = sys.argv[3]

out_pre = open(out_prefix + '.pre', 'w')
out_post = open(out_prefix + '.post', 'w')

skip = 0
dels = 0
nondels = 0
filtered = 0

for pre_l, post_l in zip(open(pre_fp), open(post_fp)):
    pre_l = pre_l.strip().split()
    post_l = post_l.strip().split()
    
    d = diff(pre_l, post_l)
    
    old = [x for x in d if x[0] == '-']
    new = [x for x in d if x[0] == '+']

    if len(old) == 0:
        skip += 1
        continue
    oldi = next((i for i, x in enumerate(d) if x[0] == '-'))

    if not new:
        out_pre.write(' '.join(pre_l) + '\n')
        out_post.write(' '.join(post_l) + '\n')
        dels += 1
    # only accept cases where bias language is directly changed
    elif len(new) == 1 and oldi < len(d)-1 and d[oldi + 1][0] == '+':
        out_pre.write(' '.join(pre_l) + '\n')
        out_post.write(' '.join(post_l) + '\n')
        nondels += 1
    else:
        filtered += 1

print('skip: ', skip)
print('filtered: ', filtered)
print('dels: ', dels)
print('nondels: ', nondels)
print('total: ', dels+nondels)


