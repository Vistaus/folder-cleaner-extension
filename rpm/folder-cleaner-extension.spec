%global uuid    com.github.Latesil.%{name}

Name:           folder-cleaner-extension
Version:        1.0.1
Release:        1%{?dist}
Summary:        Folder Cleaner extension for Nautilus file manager

License:        GPLv3+
URL:            https://github.com/Latesil/folder-cleaner-extension
Source0:        %{url}/archive/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  nautilus-python-devel
Requires:       nautilus-python

%description
%{summary}.


%prep
%autosetup -p1


%build
%meson
%meson_build


%install
%meson_install
%find_lang %{uuid}


%files -f %{uuid}.lang
%license LICENSE
%doc README.md
%{_datadir}/nautilus-python/extensions/%{name}.py


%changelog
* Sun Feb 23 2020 Latesil <vihilantes@gmail.com> - 1.0.1-1
- Bump to a new version

* Sat Feb 22 2020 Latesil <vihilantes@gmail.com> - 1.0.0-1
- Initial package

