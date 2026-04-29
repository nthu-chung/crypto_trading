# Packaged Strategy Cases

This directory contains curated strategy case bundles that ship with
`cyqnt-trd`.

These bundles are not all executable `standard_bot` plugins yet. They are the
portable bridge between:

- strategy ideas and demo workflows from external case libraries
- `cyqnt_trd.standard_bot` plugins, factors, and backtest capabilities

Each case bundle contains:

- `case.json`: normalized metadata, logic summary, and integration status
- `preset.json`: a package-friendly preset that describes how the case should
  map into `standard_bot`
- `README.md`: short explanation for humans and agents

Use these bundles when you want to:

- discover built-in strategy examples from the package
- route a natural-language strategy idea to the closest existing plugin family
- understand what still needs implementation before a case becomes fully
  executable inside `standard_bot`
