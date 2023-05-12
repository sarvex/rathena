# text parts
processed_files = { }

# authors
for filename in ['AUTHORS', 'CONTRIBUTORS']:
  with open(filename) as f:
    text = ''
    for line in f:
      if filename == 'AUTHORS':
        text += f'// fast_float by {line}'
      if filename == 'CONTRIBUTORS':
        text += f'// with contributions from {line}'
    processed_files[filename] = text + '//\n'

# licenses
for filename in ['LICENSE-MIT', 'LICENSE-APACHE']:
  lines = []
  with open(filename) as f:
    lines = f.readlines()

  # Retrieve subset required for inclusion in source
  if filename == 'LICENSE-APACHE':
    lines = [
      '   Copyright 2021 The fast_float authors\n',
      *lines[179:-1]
    ]

  text = ''.join(f'//    {line.strip()}' + '\n' for line in lines)
  processed_files[filename] = text

# code
for filename in [ 'fast_float.h', 'float_common.h', 'ascii_number.h', 
                  'fast_table.h', 'decimal_to_binary.h', 'bigint.h',
                  'ascii_number.h', 'digit_comparison.h', 'parse_number.h']:
  with open(f'include/fast_float/{filename}') as f:
    text = ''.join(line for line in f if not line.startswith('#include "'))
    processed_files[filename] = '\n' + text

# command line
import argparse

parser = argparse.ArgumentParser(description='Amalgamate fast_float.')
parser.add_argument('--license', default='DUAL', choices=['DUAL', 'MIT', 'APACHE'], help='choose license')
parser.add_argument('--output', default='', help='output file (stdout if none')

args = parser.parse_args()

def license_content(license_arg):
  result = []

  if license_arg == 'DUAL':
    result += [
      '// Licensed under the Apache License, Version 2.0, or the\n',
      '// MIT License at your option. This file may not be copied,\n',
      '// modified, or distributed except according to those terms.\n',
      '//\n'
    ]

  if license_arg in ('DUAL', 'MIT'):
    result.extend(('// MIT License Notice\n//\n',
                   processed_files['LICENSE-MIT'], '//\n'))
  if license_arg in ('DUAL', 'APACHE'):
    result.extend((
        '// Apache License (Version 2.0) Notice\n//\n',
        processed_files['LICENSE-APACHE'],
        '//\n',
    ))
  return result

text = ''.join([
  processed_files['AUTHORS'], processed_files['CONTRIBUTORS'], 
  *license_content(args.license),
  processed_files['fast_float.h'], processed_files['float_common.h'], 
  processed_files['ascii_number.h'], processed_files['fast_table.h'],
  processed_files['decimal_to_binary.h'], processed_files['bigint.h'],
  processed_files['ascii_number.h'], processed_files['digit_comparison.h'],
  processed_files['parse_number.h']])

if args.output:
  with open(args.output, 'wt') as f:
    f.write(text)
else:
  print(text)
