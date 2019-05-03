
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

file_boilerplate = ("""\
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
$user_includes
$user_functions
int
main( void )
{
    $user_commands
    return 0;
}
""" )


def format_code( source_code ):
    format_process = subprocess.Popen(
      ['uncrustify', '-l', 'c', '-q', '-c', '/home/camus/.uncrustify.cfg'],
      stdin = subprocess.PIPE, stdout = subprocess.PIPE )

    stdoutdata, stderrdata = format_process.communicate(
      source_code.encode( 'utf-8') )

    if stderrdata is not None:
        return source_code
    else:
        return stdoutdata.decode( 'utf-8' )


def get_full_source( runner ):
    with_replacements = ( file_boilerplate
      .replace( "$user_functions", runner.get_user_functions_string() )
      .replace( "$user_commands", runner.get_user_commands_string() )
      .replace( "$user_includes", runner.get_user_includes_string() )
      )
    return format_code( with_replacements )
