# remirepo/fedora spec file for php-horde-Horde-HashTable
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_HashTable
%global pear_channel pear.horde.org

Name:           php-horde-Horde-HashTable
Version:        1.2.6
Release:        1%{?dist}
Summary:        Horde Hash Table Interface

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

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-hash
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Memcache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Memcache) <  3.0.0
Requires:       php-pear(pear.nrk.io/Predis) >= 0.8.3
# optional and ignore because of build order: Horde_Vfs

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-hashtable) = %{version}


%description
Provides an abstract API to access various hash table implementations.


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
%{pear_phpdir}/Horde/HashTable
%{pear_testdir}/%{pear_name}


%changelog
* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6

* Sun Jul 03 2016 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5 (no change)

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Wed Mar 04 2015 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Wed Feb 11 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Thu Jan 08 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add provides php-composer(horde/horde-hashtable)

* Mon Aug 04 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Wed Jun 04 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2
- add optional dependency on Horde_Log

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Wed Jun  5 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
