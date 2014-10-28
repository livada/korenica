import os


AddOption('--prefix',
          dest='prefix',
          nargs=1, type='string',
          action='store',
          metavar='DIR',
          help='installation prefix')
env = Environment(PREFIX = GetOption('prefix'))

# Installation paths
idir_prefix  = '$PREFIX'
idir_bin     = '$PREFIX/bin'
idir_pyshare = '$PREFIX/share/pyshared/korenica'
# idir_lib     = '$PREFIX/lib'
# idir_inc     = '$PREFIX/include'
# idir_data    = '$PREFIX/share'
Export('env idir_prefix idir_bin idir_pyshare')

env.Append(CPPPATH=[],
           CPPDEFINES=['dDOUBLE', 'PIC'],
           LIBPATH = ['/usr/lib', 
                      '/usr/local/lib',
                      ],
           )

AddOption('--debug-flags',
          action='store_true',
          dest='debug_flags',
          help='use debug flags')

if GetOption('debug_flags'):
    env.Append(CPPDEFINES=['DEBUG'], CCFLAGS='-O0 -g3')
else:
    env.Append(CCFLAGS='-O3')
    
env.VariantDir('build', 'src')

env.SConscript('src/SConscript', exports={'env': env})

env.Alias('all', 'src')


Import(['_campus'])

env.InstallAs(os.path.join(idir_bin, 'korenica'), env.Entry('#bin/korenica'))

env.Install(idir_pyshare, _campus)

py_files = Glob('./pyshared/korenica/*.py',strings=True)
for pyfile in py_files:
    env.InstallAs(os.path.join(idir_pyshare, os.path.split(pyfile)[-1:][0]), pyfile)

env.Alias('install', idir_prefix)


env.Command("uninstall", None, Delete(FindInstalledFiles()))


