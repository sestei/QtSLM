from cx_Freeze import setup, Executable
import scipy.special._ufuncs_cxx

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
	packages = [],
	includes = ['scipy.special._ufuncs_cxx'],
	excludes = ['tcl', 'scipy.sparse'],
	
)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base, targetName = 'QtSLM.exe')
]

setup(name='QtSLM',
      version = '1.0',
      description = 'QtSLM displays phase patterns for displaying on a SLM.',
      options = dict(build_exe = buildOptions),
      executables = executables)
