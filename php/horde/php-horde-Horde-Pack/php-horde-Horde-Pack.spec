# remirepo/fedora spec file for php-horde-Horde-Pack
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%{!?php_version:  %global php_version  %(php -r 'echo PHP_VERSION;')}
%global pear_name    Horde_Pack
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Pack
Version:        1.0.7
Release:        1%{?dist}
Summary:        Horde Pack Utility

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Compress_Fast) >= 1.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
BuildRequires:  php-json
BuildRequires:  php-pecl(igbinary) >= 1.2.0
# msgpack not available on all arch

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
# From package.xml, optional: json, msgpack, igbinary
# From phpcompatinfo report for version 1.0.0
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
A replacement for serialize()/json_encode() that will automatically use the
most efficient serialization available based on the input.

The serialization extensions you may want to install are:
- php-json
- php-pecl-igbinary
- php-pecl-msgpack


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


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

: PHP version %{php_version}
%if "%{php_version}" < "5.5"
sed -e 's/function testNonUtf8Pack/function SKIP_testNonUtf8Pack/' \
    -e 's/function testBuggyDriverBackends/function SKIP_testBuggyDriverBackends/' \
    -i PackTest.php
%endif

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose .
# remirepo:2
fi
exit $ret


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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Pack
%{pear_phpdir}/Horde/Pack.php
%{pear_testdir}/%{pear_name}


%changelog
* Tue Dec 20 2016 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Tue Nov 04 2014 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Thu Oct 02 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Sat Aug 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Jun 26 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Sat Jan 18 2014 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
