# spec file for php-horde-Horde-Cache
#
# Copyright (c) 2012-2014 Nick Bebout, Remi Collet
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
Version:        2.4.0
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
Requires:       php-pear(%{pear_channel}/Horde_Log) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Log) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mongo) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mongo) <  2.0.0
# From phpcompatinfo report for version 2.4.0
Requires:       php-date
Requires:       php-spl
# Optional and omitted to avoid circular dep : Horde_Db
# Optional and implicitly requires Horde_Memcache

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


%changelog
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
