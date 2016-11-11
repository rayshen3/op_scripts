""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" install python python-dev cmake YCM(make) vim7.4
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set nocompatible              " required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin()
Plugin 'gmarik/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
Plugin 'scrooloose/nerdtree'
Plugin 'jistr/vim-nerdtree-tabs'
Plugin 'jnurmine/Zenburn'
Plugin 'altercation/vim-colors-solarized'
Plugin 'fugalh/desert.vim'

" html css js
Plugin 'hail2u/vim-css3-syntax'
Plugin 'groenewege/vim-less'
Plugin 'Raimondi/delimitMate'
Plugin 'pangloss/vim-javascript'
Plugin 'nathanaelkane/vim-indent-guides'
Plugin 'marijnh/tern_for_vim'


call vundle#end()            " required

filetype plugin indent on    " required
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


" split navigations
set splitbelow
set splitright
nnoremap <C-J> <C-W><C-J>
nnoremap <C-K> <C-W><C-K>
nnoremap <C-L> <C-W><C-L>
nnoremap <C-H> <C-W><C-H>

" Enable folding
set foldmethod=indent
set foldlevel=99
nnoremap <space> za

au BufNewFile,BufRead *.py set tabstop=4 softtabstop=4 shiftwidth=4 expandtab autoindent fileformat=unix
" au BufNewFile,BufRead *.py set tabstop=4 softtabstop=4 shiftwidth=4 textwidth=79 expandtab autoindent fileformat=unix
" au BufNewFile,BufRead *.js, *.html, *.css set tabstop=2 softtabstop=2 shiftwidth=2

" YCM
set completeopt=longest,menu	                                "让Vim的补全菜单行为与一般IDE一致(参考VimTip1228)
let g:ycm_collect_identifiers_from_tags_files=1                 "注释和字符串中的文字也会被收入补全
let g:ycm_cache_omnifunc=0                                      "开启语义补全
let g:ycm_seed_identifiers_with_syntax=1	                    "在注释输入中也能补全
let g:ycm_complete_in_comments = 1                              "在字符串输入中也能补全
autocmd InsertLeave * if pumvisible() == 0|pclose|endif	        "离开插入模式后自动关闭预览窗口
inoremap <expr> <CR>       pumvisible() ? "\<C-y>" : "\<CR>"	"回车即选中当前项
let g:ycm_autoclose_preview_window_after_completion=1
map <leader>g  :YcmCompleter GoToDefinitionElseDeclaration<CR>
let g:ycm_semantic_triggers = {
    \   'css': [ 're!^\s{4}', 're!:\s+'],
    \   'html': [ '</' ],
    \ }

" NERDTree
autocmd VimEnter * NERDTree
let NERDTreeShowBookmarks=1
let NERDTreeIgnore=['\.pyc$', '\~$'] 
map <F2> :NERDTreeMirror<CR>
map <F2> :NERDTreeToggle<CR>

" define for ray
let python_highlight_all=1
syntax on
" set background=dark
" colorscheme solarized
" colorscheme zenburn
colorscheme desert

" html css js
" autocmd FileType css set omnifunc=csscomplete
" autocmd FileType html set omnifunc=htmlcomplete
autocmd FileType javascript,json,css,scss,html set tabstop=2 shiftwidth=2 expandtab ai
let javascript_enable_domhtmlcss = 1



set encoding=utf-8
set nu
set relativenumber
set sw=4
set ts=4
set lbr
set sm
set selection=inclusive
set smarttab
set smartindent
set cmdheight=1
