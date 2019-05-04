
# igcc - a read-eval-print loop for C/C++ programmers
#
# Copyright (C) 2009 Andy Balaam
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

import subprocess
from pygments import highlight
from pygments.lexers.c_cpp import CLexer
from pygments.formatters import Terminal256Formatter

file_boilerplate = ( """\
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* __IGCC_INCLUDES__ */
/* __IGCC_FUNCTIONS__ */
int
main( void )
{
    /* __IGCC_COMMANDS__ */
    return 0;
}
""" )

# To be inserted inside of an existing function
igcc_closure = ( """\
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
/* __IGCC_INCLUDES__ */
/* __IGCC_FUNCTIONS__ */
/* __IGCC_COMMANDS__ */
""" )

# ['default', 'emacs', 'friendly', 'colorful', 'autumn', 'murphy', 'manni',
#  'monokai', 'perldoc', 'pastie', 'borland', 'trac', 'native', 'fruity',
#  'bw', 'vim', 'vs', 'tango', 'rrt', 'xcode', 'igor', 'paraiso-light',
#  'paraiso-dark', 'lovelace', 'algol', 'algol_nu', 'arduino', 'rainbow_dash',
#  'abap']
def color_code( source_code ):
    return highlight(
      source_code, CLexer(),
      Terminal256Formatter( style='trac' )
      )


# Fill your preferred formatting command here.
def format_code( source_code ):
    from distutils.spawn import find_executable
    from getpass import getuser
    from os import environ
    from os.path import isfile

    # Try to detect a suitable formatting program.
    if find_executable('uncrustify') is not None:
        fmt_cmd = ['uncrustify', '-l', 'c', '-q']
        # Detect if the user has an uncrustify config
        cfg_path = environ['HOME'] + '/.uncrustify.cfg'
        if isfile( cfg_path ):
            fmt_cmd += ['-c', cfg_path]
    elif find_executable('indent') is not None:
        fmt_cmd = ['indent']
    else: # Give up
        return source_code

    format_process = subprocess.Popen( fmt_cmd,
      stdin = subprocess.PIPE, stdout = subprocess.PIPE )

    stdoutdata, stderrdata = format_process.communicate(
      source_code.encode( 'utf-8') )

    if stderrdata is not None:
        return source_code
    else:
        return stdoutdata.decode( 'utf-8' )


def get_full_source( runner ):
    with_replacements = ( file_boilerplate
      .replace( "/* __IGCC_ENTRY__ */", igcc_closure )
      .replace( "/* __IGCC_FUNCTIONS__ */", runner.get_user_functions_string() )
      .replace( "/* __IGCC_COMMANDS__ */", runner.get_user_commands_string() )
      .replace( "/* __IGCC_INCLUDES__ */", runner.get_user_includes_string() )
      )
    return format_code( with_replacements )
