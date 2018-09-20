## ncm2-elm

> [ncm2-elm](https://github.com/megalithic/ncm2-elm) is an Elm auto-completion plugin for [ncm2](https://github.com/ncm2/ncm2).

### Requirements

- [elm-oracle](https://github.com/elmcast/elm-oracle)
- elm-lang [<=0.18.0](https://github.com/elm/compiler/releases/tag/0.18.0)

`ncm2-elm` depends on
[elm-oracle](https://github.com/elmcast/elm-oracle#installation).
Presently, the `elm-oracle` dependency only supports elm-lang <= 0.18.0.

### Neovim/Vim Plugin Configuration

Assuming you are you using [`vim-plug`](https://github.com/junegunn/vim-plug):

```vim
Plug 'megalithic/ncm2-elm', { 'for': ['elm'], 'do': 'npm i -g elm-oracle' }
```
