This is a fork of @StarlitGhost 's `igcc` program.

Here are the notable changes I have made:
1. The entire project was migrated to Python3
2. C++ was swapped for C.
   * There are minor but notable differences between the languages that made this more
     suitable for my purposes.
   * Standard has been set to `gnu11` by default.
3. A list of `#include` files can be created through CLI params.
   * This makes the tool very suitable for rolling into a makefile to enter a REPL
     environment with an existing project.
4. A list of C expressions may be created with CLI params.
   * This allows you to quickly test some line of C code without any real overhead.
     Ex: `igcc -e 'printf( "%d", ( 1 << 43 ) & 420 )';`
   * By default `igcc` will evaluate the expression list and immediately exit.
     The `-i` flag may be added to force an interactive session when `-e` is also present.
5. The regex used to place `igcc` code was modified, allowing these hooks to be placed
   inside of comments.
   * This allows you to load an existing project and hook into your codebase with fine
     placement of functions, expressions, and includes.
   * A single unified hook was added so that a user only needs to add 1 line if they do
     not desire more fine grained control.
6. Color was added throughout the REPL using the `colorama` module, and `uncrustify` was
   added to reformat the generated code.
   * `uncrustify` will be the first choice by default, and a config will be 
     loaded from `~/.uncrustify.cfg` if it exists. Next `indent` will be used,
     after that it will give up.


TODO
-----

1. Fix history file.
2. Implicitly add missing ';' at end of REPL.
3. Automatically enter "paste" mode if an open syntax block is unclosed.
   (braces, parens, brackets, strings)
4. Automatically print RHS expression's evaluated result using C11's `_Generic`.
   * 99% of the time that I write a line I immediately want to print it. This should
     just happen automatically. (Perhaps with a 1 character symbol?)
   * There are a million C syntax parsers. The one from K&R is actually all I need to
     detect this.
5. Work on loading the embedded hooks.
