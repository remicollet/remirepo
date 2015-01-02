# spec file for php-theseer-autoload
#
# Copyright (c) 2014-2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    2a47cae1efaf0b395f72e748cfbcbd2f54399616
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     theseer
%global gh_project   Autoload
%global php_home     %{_datadir}/php/TheSeer
%global pear_name    Autoload
%global pear_channel pear.netpirates.net

Name:           php-theseer-autoload
Version:        1.16.2
Release:        1%{?dist}
Summary:        A tool and library to generate autoload code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoload stuff - die composer !
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.1
# For tests
BuildRequires:  php-composer(theseer/directoryscanner) >= 1.3.0
BuildRequires:  php-composer(theseer/directoryscanner) <  1.4
BuildRequires:  %{_bindir}/phpunit

# From composer.json
#        "theseer/directoryscanner": "~1.3.0",
#        "zetacomponents/console-tools": "dev-master"
Requires:       php(language) >= 5.3.1
Requires:       php-composer(theseer/directoryscanner) >= 1.3.0
Requires:       php-composer(theseer/directoryscanner) <  1.4
# Use ezc instead of zetacomponent (no release, no package)
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6
# From phpcompatinfo report for version 1.16.1
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