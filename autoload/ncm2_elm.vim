if get(s:, 'loaded', 0)
  finish
endif
let s:loaded = 1

let g:ncm2_elm#proc = yarp#py3({
      \ 'module': 'ncm2_elm',
      \ 'on_load': { -> ncm2#set_ready(g:ncm2_elm#source)}
      \ })

let g:ncm2_elm#source = extend(
      \ get(g:, 'ncm2_elm#source', {}), {
      \ 'name': 'elm',
      \ 'ready': 0,
      \ 'priority': 9,
      \ 'mark': 'rs',
      \ 'early_cache': 1,
      \ 'subscope_enable': 1,
      \ 'scope': ['rust'],
      \ 'word_pattern': '[\w/]+',
      \ 'complete_pattern': ['\.', '::'],
      \ 'on_complete': 'ncm2_elm#on_complete',
      \ 'on_warmup': 'ncm2_elm#on_warmup',
      \ }, 'keep')

func! ncm2_elm#init()
  call ncm2#register_source(g:ncm2_elm#source)
endfunc

func! ncm2_elm#on_warmup(ctx)
  call g:ncm2_elm#proc.jobstart()
endfunc

func! ncm2_elm#on_complete(ctx)
  call g:ncm2_elm#proc.try_notify('on_complete',
        \ a:ctx,
        \ getline(1, '$'))
endfunc

func! ncm2_elm#error(msg)
  call g:ncm2_elm#proc.error(a:msg)
endfunc
