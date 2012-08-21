%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTML_Template_PHPLIB

Name:		php-pear-HTML_Template_PHPLIB
Version:	1.5.2
Release:	1%{?dist}
Summary:	PHP template system based on preg_* 
Group:		Development/Libraries
License:	LGPLv2
URL:		http://pear.php.net/package/%{pear_name}
Source0:	http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	php-pear(PEAR)

Requires:	php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-pear(%{pear_name}) = %{version}

%description
This is the PEAR port of the popular PHPLIB template system. It
contains some features not currently found in the original version.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}

sed -e '/README/s/role="data"/role="doc"/' \
    -i %{pear_name}.xml


%build
# Empty build section nothing to do here

%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
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
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/HTML/Template
%{_bindir}/*

%changelog
* Tue Aug 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.5.2-1
- update to 1.5.2

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.4.0-6
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Andrew Colin Kissa <andrew@topdog.za.net> 1.4.0-2
- Fix naming 

* Mon Jul 27 2009 Andrew Colin Kissa <andrew@topdog.za.net> 1.4.0-1
- Initial packaging
