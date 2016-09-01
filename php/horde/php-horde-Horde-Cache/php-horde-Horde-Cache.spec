# remirepo/fedora spec file for php-horde-Horde-Cache
#
# Copyright (c) 2012-2016 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Cache
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Cache
Version:        2.5.4
Release:        1%{?dist}
Summary:        Horde Caching API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
#BuildRequires:  php-pecl(APC)

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-hash
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress_Fast) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# From package.xml, optional
Requires:       php-pear(%{pear_channel}/Horde_HashTable) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_HashTable) <  2.0.0
%if 0%{?fedora} > 21
Suggests:       php-pear(%{pear_channel}/Horde_Mongo) >= 1.0.0
Suggests:       php-pear(%{pear_channel}/Horde_Mongo) <  2.0.0
%else
Requires:       php-pear(%{pear_channel}/Horde_Mongo) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mongo) <  2.0.0
%endif
# From phpcompatinfo report for version 2.5.0
Requires:       php-date
Requires:       php-spl
# Optional and omitted to avoid circular dep : Horde_Db
# Optional and implicitly requires Horde_Memcache, Horde_Log

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This package provides a simple, functional caching API, with the option to
store the cached data on the filesystem, in one of the PHP opcode cache
systems (APC, eAcclerator, XCache, or Zend Performance Suite's content
cache), memcached, or an SQL table.


%prep
%setup -q -c

cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
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
   php56 -d apc.enable_cli=1 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 -d apc.enable_cli=1 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
php -d apc.enable_cli=1 %{_bindir}/phpunit --verbose .
# remirepo:2
fi
exit $ret


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
%{pear_phpdir}/Horde/Cache
%{pear_phpdir}/Horde/Cache.php
%{pear_datadir}/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Thu Sep 01 2016 Remi Collet <remi@fedoraproject.org> - 2.5.4-1
- Update to 2.5.4 (no change)

* Tue Jun 28 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-2
- Horde_Mongo is optional

* Fri Feb 19 2016 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- Update to 2.5.3
- PHP 7 compatible version

* Mon Feb 01 2016 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2
- add and run upstream test suite
- run test suite with both PHP 5 and 7 when available

* Wed Jan 06 2016 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1

* Wed May 07 2014 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2
- drop optional dependency on Horde_Log (implicit)

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Sat Jan 25 2014 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Tue Oct 08 2013 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0
- switch from Conflicts to Requires
- add (optional) requires for Horde_HashTable

* Sat May 04 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-2
- drop optional dependency on Horde_Db (avoid circular)

* Sat May 04 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- raise dependency for Horde_Db >= 2.0.3

* Tue Apr 09 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4
- Requires Horde_Compress_Fast is now mandatory
- Requires Horde-Memcache (optional)

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3
- requires Horde_Compress_Fast instead of LZF
- fix License

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Update to 2.0.1 for remi repo

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.5-1
- Upgrade to 1.0.5

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-1
- Initial package
