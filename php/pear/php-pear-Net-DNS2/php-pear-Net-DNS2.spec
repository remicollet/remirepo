# spec file for php-pear-Net-DNS2
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_DNS2

Name:           php-pear-Net-DNS2
Version:        1.3.2
Release:        1%{?dist}
Summary:        PHP Resolver library used to communicate with a DNS server

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Net_DNS2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
# for tests
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)

# From phpcompatinfo report for version 1.3.2
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-json
Requires:       php-pcre
Requires:       php-shmop
Requires:       php-sockets
Requires:       php-spl
# Optional
Requires:       php-filter
Requires:       php-mhash
Requires:       php-openssl

Provides:       php-pear(%{pear_name}) = %{version}


%description
Net_DNS2 - Native PHP5 DNS Resolver and Updater

The main features for this package include:
* Increased performance; most requests are 2-10x faster than Net_DNS
* Near drop-in replacement for Net_DNS
* Uses PHP5 style classes and exceptions
* Support for IPv4 and IPv6, TCP and UDP sockets.
* Includes a separate, more intuitive Updater class for handling dynamic update
* Support zone signing using TSIG and SIG(0) for updates and zone transfers
* Includes a local cache using shared memory or flat file to improve performance
* includes many more RR's, including DNSSEC RR's.


%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


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


%clean
rm -rf %{buildroot}


%check
if ping -c 1 google.com &>/dev/null
then
  suite=AllTests.php
else
  : Resolver test disabled
  suite=Net_DNS2_ParserTest.php
fi
phpunit \
   -d date.timezone=UTC \
   -d include_path=.:%{buildroot}%{pear_phpdir}:%{pear_phpdir} \
   %{buildroot}%{pear_testdir}/%{pear_name}/tests/$suite


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Net
%{pear_phpdir}/Net/DNS2
%{pear_phpdir}/Net/DNS2.php
%{pear_testdir}/%{pear_name}


%changelog
* Sun Dec 01 2013 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2 (stable)

* Thu Jun 13 2013 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1
- hack for https://pear.php.net/bugs/19977 (bad role)

* Mon Apr 08 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- hack for https://pear.php.net/bugs/19886 (shortag)

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5

* Sat Aug 18 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable), API 1.2.3 (stable)
- upstream now provides LICENSE and tests
- run all tests if network available, else only parser

* Wed Aug 15 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- rebuilt for new pear_testdir
- use php-pear(PEAR) in BR/R

* Sun Aug 12 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable), API 1.2.2 (stable)
- Initial package

