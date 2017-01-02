# remirepo/fedora spec file for php-pear-Net-LDAP2
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name Net_LDAP2

# Test suite requires a LDAP server, so are not run during build

Name:           php-pear-Net-LDAP2
Version:        2.2.0
Release:        1%{?dist}
Summary:        Object oriented interface for searching and manipulating LDAP-entries

Group:          Development/Libraries
# LGPL doesn't require license file, but ask for it
# https://pear.php.net/bugs/bug.php?id=20504 - please include License file
License:        LGPLv3
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.10.1

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php-pear(PEAR) >= 1.10.1
Requires:       php(language)  >= 5.4
Requires:       php-ldap
# From phpcompatinfo report
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-composer(pear/net_ldap2) = %{version}


%description
Net_LDAP2 is the successor of Net_LDAP (which is a clone of Perls Net::LDAP)
object interface to directory servers. It does contain most of Net::LDAPs
features but has some own too.

With Net_LDAP2 you have:
* A simple object-oriented interface to connections,
  searches entries and filters.
* Support for TLS and LDAP v3.
* Simple modification, deletion and creation of LDAP entries.
* Support for schema handling.

Net_LDAP2 layers itself on top of PHP's existing ldap extensions.


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
%{pear_phpdir}/Net
%{pear_testdir}/%{pear_name}


%changelog
* Sat Oct 31 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0
- provide php-composer(pear/net_ldap2)

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Version 2.1.0 (stable), API 2.0.0 (stable)
- Initial package