%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Auth_HTTP

Name:		php-pear-Auth_HTTP
Version:	2.1.8
Release:	1%{?dist}
Summary:	Class providing HTTP authentication methods
Group:		Development/Libraries
License:	PHP
URL:		http://pear.php.net/package/Auth_HTTP
Source0:	http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2 php-pear(Auth) >= 1.2.0

Requires:	php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:	php-pear(Auth) >= 1.2.0

Provides:	php-pear(%{pear_name}) = %{version}


%description
The PEAR::Auth_HTTP class provides methods for creating an HTTP
authentication system using PHP, that is similar to Apache's
realm-based .htaccess authentication.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}

sed -e '/README/s/role="data"/role="doc"/' \
    -i %{pear_name}.xml


%build
cd %{pear_name}-%{version}


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
	%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/Auth/HTTP.php


%changelog
* Tue Aug 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.1.8-1
- update to 2.1.8

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 2.1.6-7
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 2.1.6-2
- Renamed to match upstream

* Thu Jun 25 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 2.1.6-1
- Initial creation
