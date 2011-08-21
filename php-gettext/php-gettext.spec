Name:      php-gettext
Version:   1.0.11
Release:   1%{?dist}
License:   GPLv2+
Summary:   Gettext emulation in PHP 
Group:     Development/Libraries
URL:       https://launchpad.net/php-gettext
Source:    http://launchpad.net/%{name}/trunk/%{version}/+download/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  php-common
BuildArch: noarch

%description
This library provides PHP functions to read MO files even when gettext is 
not compiled in or when appropriate locale is not present on the system.

%prep
%setup -q
chmod -x *.php
%build
%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/php/%{name}
cp -a *.php gettext.inc %{buildroot}%{_datadir}/php/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README AUTHORS COPYING
%{_datadir}/php/%{name}

%changelog
* Sun Jul 31 2011 Robert Scheck <robert@fedoraproject.org> 1.0.11-1
- Upgrade to 1.0.11

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 06 2009 David Nalley <david@gnsa.us> 1.0.9-2
- corrected license field 

* Sun Dec 06 2009 David Nalley <david@gnsa.us> 1.0.9-1
- Initial Packaging
