#!/usr/bin/env python3
# encoding=UTF-8

# Copyright © 2020-2022 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import argparse
import re

import pikepdf

def mangle_pdf(pdf, color):
    for page in pdf.pages:
        mangle_page(pdf, page, color)

def mangle_page(pdf, page, color):
    page.contents_coalesce()
    op_rg = pikepdf.Operator('rg')
    op_BT = pikepdf.Operator('BT')
    op_ET = pikepdf.Operator('ET')
    text_showing_ops = frozenset(map(pikepdf.Operator, {'TJ', 'Tj', '\'', '"'}))
    text_obj = False
    stream = []
    for args, op in pikepdf.parse_content_stream(page):
        if text_obj:
            if op in text_showing_ops:
                stream += [(color, op_rg)]
            elif op == op_ET:
                text_obj = False
        elif op == op_BT:
            text_obj = True
        stream += [(args, op)]
    stream = pikepdf.unparse_content_stream(stream)
    page.Contents = pdf.make_stream(stream)

re_color = re.compile(r'\A[#]?' + '([0-9a-fA-F]{2})' * 3 + r'\Z')
def parse_color(s):
    match = re_color.match(s)
    if match is None:
        raise TypeError
    return tuple(int(x, 16) / 0xFF for x in match.groups())
parse_color.__name__ = 'color'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--color', type=parse_color, metavar='RRGGBB', required=True)
    ap.add_argument('input', metavar='INPUT-FILE')
    ap.add_argument('output', metavar='OUTPUT-FILE')
    options = ap.parse_args()
    pdf = pikepdf.open(options.input)
    mangle_pdf(pdf, options.color)
    pdf.save(options.output)

if __name__ == '__main__':
    main()

# vim:ts=4 sts=4 sw=4 et
