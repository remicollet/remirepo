%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_DNS2

# Tests are only run with rpmbuild --with tests
# Can't be run in mock / koji because Internet access
%global with_tests       %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-pear-Net-DNS2
Version:        1.2.2
Release:        1%{?dist}.1
Summary:        PHP Resolver library used to communicate with a DNS server

Group:          Development/Libraries
License:        BSD
URL:            http://pear.php.net/package/Net_DNS2
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

# Request for License and tests folder https://pear.php.net/bugs/19562
# https://netdns2.googlecode.com/svn/tags/Net_DNS2-1.2.2/tests/AllTests.php
# https://netdns2.googlecode.com/svn/tags/Net_DNS2-1.2.2/tests/Net_DNS2_ParserTest.php
# https://netdns2.googlecode.com/svn/tags/Net_DNS2-1.2.2/tests/Net_DNS2_ResolverTest.php
Source1:        %{pear_name}-tests-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
%if %{with_tests}
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
# extensions detected by phpci (+ php-filter, not yet available in EL)
Requires:       php-ctype, php-date, php-json, php-openssl, php-mhash
Requires:       php-pcre, php-shmop, php-sockets, php-spl

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
%setup -q -c -a 1
cd %{pear_name}-%{version}
# Package.xml is V2
mv ../package.xml %{name}.xml

sed -e '/include_path/d' \
    -i tests/AllTests.php

sed -e 's:</dir>:<file name="tests/AllTests.php" role="test" />\n</dir>:' \
    -e 's:</dir>:<file name="tests/Net_DNS2_ParserTest.php" role="test" />\n</dir>:' \
    -e 's:</dir>:<file name="tests/Net_DNS2_ResolverTest.php" role="test" />\n</dir>:' \
    -i %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%check
%if %{with_tests}
phpunit \
   -d date.timezone=UTC \
   -d include_path=.:%{buildroot}%{pear_phpdir}:%{pear_phpdir} \
   %{buildroot}%{pear_testdir}/%{pear_name}/tests
%else
: 'Test suite disabled (missing "--with tests" option)'
%endif


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
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Net
%{pear_phpdir}/Net/DNS2
%{pear_phpdir}/Net/DNS2.php
%{pear_testdir}/%{pear_name}


%changelog
* Wed Aug 15 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1.1
- rebuilt for new pear_testdir

* Sun Aug 12 2012 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable), API 1.2.2 (stable)
- Initial package

