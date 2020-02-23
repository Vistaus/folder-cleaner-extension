project(
	'folder-cleaner-extension',
	version: '0.1.0',
	meson_version: '>= 0.50.0',
)

pkg = import('pkgconfig')
nautilus_python = dependency('nautilus-python', version:  '>=1.2.3')
lib = library('foo', dependencies : [bar])
pkg.generate(lib)

appname = 'com.gitlab.Latesil.folder-cleaner-extension'

i18n  = import('i18n')

subdir('script')
subdir('po')
