# remirepo spec file for phar-gui
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit  bc1177aee3b376ebab87cd91e5c177a8b8107dbf
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date    20150609
%global gh_owner   jgmdev
%global gh_project phar-gui

Name:           %{gh_project}
Summary:        A graphical user interface for phar files
Version:        1.0
%if 0%{?gh_date}
Release:        0.2.%{gh_date}git%{gh_short}%{?dist}
%else
Release:        1%{?dist}
%endif
License:        MIT
Group:          Development/Libraries

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# To ensure we are not going to build where extension is missing
BuildRequires:  php-pecl(wxwidgets)

Requires:       php-cli
Requires:       php-phar
Requires:       php-spl
Requires:       php-pecl(wxwidgets)


%description
A graphical user interface developed with wxPHP to manage, extract and
view the content of PHP phar files.

The interface of the application was developed with wxFormBuilder and its
source code can serve as an example of how to integrate graphical user
interfaces designed with wxFormBuilder in your code.

Features:
- Create phar files
- View the content of a phar
- Extract all the content of a phar file
- Extract single files in the phar
- Add empty directories to a phar file
- Add external files to a phar
- Delete files from a phar
- Modify phar file stub
- Modify phar file alias
- View the code of php files inside the phar by double clicking them.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Not usable as a launcher
chmod -x main.php
sed -e '/^#!/d' -i main.php

# Create the launcher
cat <<EOF | tee phar-gui
#!/bin/sh
exec %{_bindir}/php \
  -d extension=wxwidgets.so \
  -d phar.readonly=0 \
  %{_datadir}/%{name}/main.php "$@"
EOF

# Keep LICENSE.txt as this is used by the GUI
# Create a link in the %%doc
ln -s %{_datadir}/%{name}/LICENSE.txt LICENSE


%build
# nothing to build


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}

cp -pr main.php resources.php lib images LICENSE.txt \
   %{buildroot}%{_datadir}/%{name}

install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%{_datadir}/%{name}
%{_bindir}/%{name}


%changelog
* Tue Jun  9 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150609gitbc1177a
- new snapshot, for pecl/wxWidgets 3.0.2.0
- fix license handling

* Fri Apr 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20140417gitedbd631
- keep LICENSE.txt in /usr/share/phar-gui (used in the GUI)
- open https://github.com/jgmdev/phar-gui/pull/1

* Fri Apr 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20140417gitedbd631
- Initial packaging