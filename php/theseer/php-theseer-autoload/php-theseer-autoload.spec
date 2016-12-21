# remirepo/fedora spec file for php-theseer-autoload
#
# Copyright (c) 2014-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    4466c1d32c2dadb40cbe598b656a485e6175a00d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   Autoload
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    Autoload
%global pear_channel pear.netpirates.net

Name:           php-theseer-autoload
Version:        1.23.0
Release:        1%{?dist}
Summary:        A tool and library to generate autoload code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{?gh_short}.tar.gz

# Autoloader path
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.1
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~4.0|~5.0",
#        "squizlabs/php_codesniffer": "~1.5"
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(theseer/directoryscanner) >= 1.3
BuildRequires:  php-composer(theseer/directoryscanner) <  2
BuildRequires:  php-composer(zetacomponents/console-tools) >= 1.7

# From composer.json, "require": {
#        "theseer/directoryscanner": "~1.3",
#        "zetacomponents/console-tools": "~1.7"
Requires:       php(language) >= 5.3.1
Requires:       php-composer(theseer/directoryscanner) >= 1.3
Requires:       php-composer(theseer/directoryscanner) <  2
Requires:       php-composer(zetacomponents/console-tools) >= 1.7
Requires:       php-composer(zetacomponents/console-tools) <  2
# From phpcompatinfo report for version 1.21
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

: drop composer dependencies
sed -e '\:../vendor/:d'    -i src/autoload.php

: add package dependencies
cat <<EOF | tee            -a src/autoload.php
// Dependencies
require '/usr/share/php/TheSeer/DirectoryScanner/autoload.php';
require '/usr/share/php/ezc/Base/base.php';
spl_autoload_register(array('\\ezcBase','autoload'));
EOF

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
: Fix test suite to use installed library
cat <<EOF | tee tests/init.php
<?php
require '%{buildroot}%{_datadir}/php/TheSeer/Autoload/autoload.php';
EOF

# remirepo:13
run=0
ret=0
if which php56; then
   : Run upstream test suite with PHP 5
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   : Run upstream test suite with PHP 7
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
: Run upstream test suite
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret


%clean
rm -rf %{buildroot}


%pre
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
* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 1.23.0-1
- update to 1.23.0

* Sat Aug 13 2016 Remi Collet <remi@fedoraproject.org> - 1.22.0-1
- update to 1.22.0

* Wed Nov 11 2015 Remi Collet <remi@fedoraproject.org> - 1.21.0-1
- update to 1.21.0

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.20.3-1
- update to 1.20.3

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.20.2-1
- update to 1.20.2

* Sat Oct  3 2015 Remi Collet <remi@fedoraproject.org> - 1.20.1-1
- update to 1.20.1

* Sat Jul 25 2015 Remi Collet <remi@fedoraproject.org> - 1.20.0-1
- update to 1.20.0

* Tue Jul 14 2015 Remi Collet <remi@fedoraproject.org> - 1.19.2-1
- update to 1.19.2

* Mon Jul 13 2015 Remi Collet <remi@fedoraproject.org> - 1.19.1-1
- update to 1.19.1

* Thu Jul  2 2015 Remi Collet <remi@fedoraproject.org> - 1.19.0-1
- update to 1.19.0

* Wed Jul  1 2015 Remi Collet <remi@fedoraproject.org> - 1.18.0-1
- update to 1.18.0
- load dependencies in the autoloader (not in the command)

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
