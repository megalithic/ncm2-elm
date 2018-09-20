# -*- coding: utf-8 -*-

import vim
from ncm2 import Ncm2Source, getLogger, Popen
import os
import glob
import subprocess

logger = getLogger(__name__)


class Source(Ncm2Source):
    def check(self):
        from distutils.spawn import find_executable
        if not find_executable("elm-oracle"):
            self.nvim.call(
                'ncm2_elm#error',
                ('Unable to find elm-oracle for completion, '
                 'please visit https://github.com/elmcast/elm-oracle#installation for installation details.'))

    def _project_root(self, filepath):
        ret = path.dirname(filepath)
        while ret != '/' and not path.exists(path.join(ret, 'elm-package.json')):
            ret = path.dirname(ret)

        if ret == '/':
            return path.dirname(filepath)

        return ret

    def on_complete(self, ctx, lines):
        src = "\n".join(lines)
        src = self.get_src(src, ctx)
        src = src.encode('utf-8')
        lnum = ctx['lnum']
        ccol = ctx['ccol']
        bcol = ctx['bcol']
        typed = ctx['typed']
        filepath = ctx['filepath']
        startccol = ctx['startccol']

        query = typed.lstrip(" \t\'\"")
        # args = ['elm-oracle', filepath, query]

        args = [
            'elm-oracle',
            str(lnum),
            str(bcol - 1),
            filepath,
            '-',
            query
        ]

        proj_dir = self._project_root(filepath)
        proc = Popen(
            args=args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
            cwd=proj_dir)

        result, errs = proc.communicate(src, timeout=30)
        result = json.loads(result.decode('utf-8'))

        logger.debug("args: %s, result: [%s]", args, result.decode())

        if not result:
            return

        matches = []

        # for line in lines:
        #     fields = line.split(";")
        #     tword = fields[0].split(' ')

        #     if tword[0] != "MATCH":
        #         if tword == "prefix":
        #             startccol = ccol - len(fields[2])
        #         continue

        #     t, word = tword

        #     match = dict(word=word)

        #     menu = fields[6]

        #     match['menu'] = menu
        #     match = self.match_formalize(ctx, match)

        #     snippet = fields[1]
        #     if snippet != word:
        #         ud = match['user_data']
        #         ud['is_snippet'] = 1
        #         ud['snippet'] = snippet

        #     matches.append(match)

        for item in result:
            word = item['name']
            menu = item.get('signature', item.get('fullName',''))
            m = { 'word': word, 'menu': menu, 'info': item['comment'] }

            matches.append(m)


        logger.info("matches: [%s]", matches)

        self.complete(ctx, startccol, matches)


source = Source(vim)

on_complete = source.on_complete

source.check()
