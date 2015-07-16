%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Text_Diff

Name:           php-pear-Text-Diff
Version:        1.1.1
Release:        10%{?dist}
Summary:        Engine for performing and rendering text diffs

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}


%description
This package provides a text-based diff engine and renderers for multiple diff
output formats.


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_docdir}/* docdir

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

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
%doc %{pear_name}-%{version}/docdir/%{pear_name}/*
%{pear_xmldir}/%{pear_name}.xml
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/Text


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-7
- fix metadata location, FTBFS #914367

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-5
- rebuilt for new pear_testdir

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 18 2010 Xavier Bachelot <xavier@bachelot.org> 1.1.1-1
- Update to 1.1.1.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Xavier Bachelot <xavier@bachelot.org> 1.1.0-1
- Initial build.
