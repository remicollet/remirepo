%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Cache

Name:           php-horde-Horde-Cache
Version:        1.0.5
Release:        1%{?dist}
Summary:        Horde Caching API

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) <= 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/Horde_Cache) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
This package provides a simple, functional caching API, with the option to
store the cached data on the filesystem, in one of the PHP opcode cache
systems (APC, eAcclerator, XCache, or Zend Performance Suite's content
cache), memcached, or an SQL table.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi

%files
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Cache
%{pear_phpdir}/Horde/Cache.php
%{pear_datadir}/Horde_Cache
%doc %{pear_docdir}/Horde_Cache/COPYING

%changelog
* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.5-1
- Upgrade to 1.0.5

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.4-1
- Initial package
