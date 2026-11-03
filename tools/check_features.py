# -*- coding: utf-8 -*-
"""Lab 2 自查工具：统计每个 .feature 的场景数与三路径覆盖。"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORY_DIR = os.path.join(os.path.dirname(HERE), 'docs', 'backlog', 'stories')

PATH_TAGS = {'happy': '快乐路径', 'boundary': '边界路径', 'exception': '异常路径'}
WEAK_WORDS = ['友好地', '正确地', '合理地', '流畅地', '较好', '适当', '尽量', '等等']


def check(path):
    text = open(path, encoding='utf-8').read()
    lines = text.splitlines()
    name = os.path.basename(path)

    has_lang = '# language: zh-CN' in text
    scenarios = []          # (行号, 标题, 前面的 tag 集合)
    tags = set()
    cur_tags = set()
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if s.startswith('@'):
            cur_tags = {t[1:] for t in s.split()}
            tags |= cur_tags
            continue
        m = re.match(r'^(场景大纲|场景|Scenario Outline|Scenario)\s*[:：]\s*(.+)$', s)
        if m:
            scenarios.append((i, m.group(2).strip(), set(cur_tags)))
            cur_tags = set()

    happy = sum(1 for _, _, t in scenarios if 'happy' in t)
    boundary = sum(1 for _, _, t in scenarios if 'boundary' in t)
    exception = sum(1 for _, _, t in scenarios if 'exception' in t)

    weak = []
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith(('当 ', '那么 ', '而且 ', '但是 ')):
            for w in WEAK_WORDS:
                if w in ln:
                    weak.append((i, w))

    return {
        'name': name,
        'lang': has_lang,
        'n': len(scenarios),
        'happy': happy,
        'boundary': boundary,
        'exception': exception,
        'weak': weak,
        'scenarios': scenarios,
    }


def main():
    files = sorted(f for f in os.listdir(STORY_DIR) if f.endswith('.feature'))
    if not files:
        print('未找到 .feature 文件'); return 1

    print('%-10s %-5s %-6s %-5s %-5s %-5s %s' % ('文件', '场景', '快乐', '边界', '异常', 'zh-CN', '结论'))
    print('-' * 72)
    total = 0
    bad = 0
    for f in files:
        r = check(os.path.join(STORY_DIR, f))
        total += r['n']
        problems = []
        if not r['lang']:
            problems.append('缺 language 头')
        if r['n'] < 3:
            problems.append('场景<3')
        if r['exception'] == 0:
            problems.append('无异常路径')
        if r['boundary'] == 0:
            problems.append('无边界路径')
        ok = '通过' if not problems else '待修:' + '/'.join(problems)
        if problems:
            bad += 1
        print('%-10s %-5d %-6d %-5d %-5d %-5s %s' % (
            f, r['n'], r['happy'], r['boundary'], r['exception'],
            'Y' if r['lang'] else 'N', ok))
        for i, w in r['weak']:
            print('    ! 第 %d 行出现模糊词「%s」，建议改成可断言的事实' % (i, w))

    print('-' * 72)
    print('共 %d 个文件 / %d 个场景；%d 个文件需要修。' % (len(files), total, bad))
    return 0 if bad == 0 else 2


if __name__ == '__main__':
    sys.exit(main())
