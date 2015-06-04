# remirepo/fedora spec file for php-theseer-autoload
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b8acc94215571ba71c3128cc3847f2b08c1cc4d1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   Autoload
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    Autoload
%global pear_channel pear.netpirates.net

Name:           php-theseer-autoload
Version:        1.17.0
Release:        3%{?dist}
Summary:        A tool and library to generate autoload code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

# Autoload stuff - die composer !
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.1
# For tests
BuildRequires:  php-composer(theseer/directoryscanner) >= 1.3
BuildRequires:  php-composer(theseer/directoryscanner) <  2
BuildRequires:  %{_bindir}/phpunit

# From composer.json
#        "theseer/directoryscanner": "~1.3",
#        "zetacomponents/console-tools": "~1.7"
Requires:       php(language) >= 5.3.1
Requires:       php-composer(theseer/directoryscanner) >= 1.3
Requires:       php-composer(theseer/directoryscanner) <  2
Requires:       php-composer(zetacomponents/console-tools) >= 1.7
Requires:       php-composer(zetacomponents/console-tools) <  2
# From phpcompatinfo report for version 1.16.1
Requires:       php-cli
Requires:       php-date
Requires:       php-json
Requires:       php-openssl
Requires:       php-phar
Requires:       php-spl
Requires:       php-tokenizer
# Optional xdebug

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(theseer/autoload) = %{version}


%description
The PHP AutoloadBuilder CLI tool phpab is a command line application
to automate the process of generating an autoload require file with
the option of creating static require lists as well as phar archives.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm
# autoload only for this package
sed -e '\:../vendor/:d'          -i src/autoload.php
# set version
sed -e 's/@VERSION@/%{version}/' -i phpab.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/%{gh_project}

install -Dpm 0755 phpab.php %{buildroot}%{_bindir}/phpab


%check
cat <<EOF | tee tests/init.php
<?php
require 'TheSeer/DirectoryScanner/autoload.php';
require 'TheSeer/Autoload/autoload.php';
EOF

phpunit --include-path=%{buildroot}%{_datadir}/php


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
  %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%{php_home}/%{gh_project}
%{_bindir}/phpab


%changelog
* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 1.17.0-3
- missing dependency on php-cli

* Wed Jun  3 2015 Remi Collet <remi@fedoraproject.org> - 1.17.0-2
- swicth from eZ to Zeta Components
- ensure compatibility with SCL

* Fri May 15 2015 Remi Collet <remi@fedoraproject.org> - 1.17.0-1
- Update to 1.17.0

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 1.16.2-1
- Update to 1.16.2

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 1.16.1-1
- Update to 1.16.1
- switch from pear to github sources

* Wed Nov 12 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-2
- define date.timezone in phpab command to avoid warning

* Tue Sep 02 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-1
- Update to 1.16.0

* Thu Aug 14 2014 Remi Collet <remi@fedoraproject.org> - 1.15.1-1
- Update to 1.15.1

* Tue Aug 12 2014 Remi Collet <remi@fedoraproject.org> - 1.15.0-1
- Update to 1.15.0

* Thu Apr 24 2014 Remi Collet <remi@fedoraproject.org> - 1.14.2-1
- Update to 1.14.2

* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.14.1-1
- initial package, version 1.14.1