# spec file for php-theseer-autoload
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name     Autoload
%global pear_channel  pear.netpirates.net

Name:           php-theseer-autoload
Version:        1.14.1
Release:        1%{?dist}
Summary:        A tool and library to generate autoload code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/theseer/Autoload
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})
# For tests
BuildRequires:  php-pear(%{pear_channel}/DirectoryScanner) >= 1.3.0
BuildRequires:  %{_bindir}/phpunit

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.1
Requires:       php-openssl
Requires:       php-phar
Requires:       php-tokenizer
Requires:       php-pear(PEAR)
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/DirectoryScanner) >= 1.3.0
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6
# From phpcompatinfo report for version 1.14.1
Requires:       php-date
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
The PHP AutoloadBuilder CLI tool phpab is a command line application
to automate the process of generating an autoload require file with
the option of creating static require lists as well as phar archives.


%prep
%setup -q -c

cd %{pear_name}-%{version}
# https://github.com/theseer/Autoload/issues/46
sed -e '/phpunit.xml.dist/s/role="doc"/role="test"/' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}
cat <<EOF | tee tests/init.php
<?php
require 'TheSeer/DirectoryScanner/autoload.php';
require 'TheSeer/Autoload/autoload.php';
EOF

phpunit \
  --include-path=%{buildroot}%{pear_phpdir} \
  -d date.timezone=UTC



%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%doc %{pear_testdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml

%{pear_phpdir}/TheSeer/%{pear_name}
%{_bindir}/phpab


%changelog
* Sun Apr  6 2014 Remi Collet <remi@fedoraproject.org> - 1.14.1-1
- initial package, version 1.14.1