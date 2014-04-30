env = Environment()

conf = Configure(env)

# Do checks

env = conf.Finish()

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

env.Install('./', _campus)
env.Alias('install', './')


# env.Command("uninstall", None, Delete(FindInstalledFiles()))


