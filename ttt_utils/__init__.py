"""
These constants are used with the --about command line argument or button.
Program will exit here if any check fails when called.
"""
from . import platform_check, vcheck

# Development status standards: https://pypi.org/classifiers/
__author__ = 'Craig S. Echt'
__version__: str = '0.0.18'
__dev_status__ = 'Development Status :: 3 - Alpha'
__copyright__ = 'Copyright (C) 2022 C.S. Echt, under MIT License'

URL = 'https://github.com/csecht/tic-tac-toe-tkinter'

LICENSE = """                                MIT License
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    You should have received a copy of the license
    along with this program distribution (the LICENCE.txt file). If not,
    see https://mit-license.org/
    """

platform_check.check_platform()
vcheck.minversion('3.7')
