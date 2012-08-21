%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name HTML_Javascript

Name:		php-pear-HTML_Javascript
Version:	1.1.2
Release:	1%{?dist}
Summary:	Class for creating simple JS scripts	 
Group:		Development/Libraries
License:	PHP
URL:		http://pear.php.net/package/HTML_Javascript
Source0:	http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2

Requires:	php-pear(PEAR)
Requires:	php-pear(HTML_Common)
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-pear(%{pear_name}) = %{version}

%description
The PEAR::HTML_Javascript package provides methods for 
creating simple JS scripts

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
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
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/HTML/Javascript
%{pear_phpdir}/HTML/Javascript.*


%changelog
* Tue Aug 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.2-1
- update to 1.1.2
- doc in /usr/share/doc/pear

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-8
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Andrew Colin Kissa - 1.1.1-3
- Add HTML_Common dependency

* Thu Jun 25 2009 Andrew Colin Kissa - 1.1.1-2
- Fix directory ownership

* Thu Jun 25 2009 Andrew Colin Kissa - 1.1.1-1
- Initial creation
