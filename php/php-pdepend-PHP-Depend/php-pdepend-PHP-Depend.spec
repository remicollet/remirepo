%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_Depend
%global channel pear.pdepend.org

Name:           php-pdepend-PHP-Depend
Version:        1.1.0
Release:        1%{?dist}
Summary:        PHP_Depend design quality metrics for PHP package

Group:          Development/Libraries
License:        BSD
URL:            http://www.pdepend.org/
Source0:        http://pear.pdepend.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.6.0
BuildRequires:  php-channel(%{channel})

Requires:       php-channel(%{channel})
Requires:       php-xml >= 5.2.3
Requires:       php-pecl(imagick) >= 2.2.0b2
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
PHP_Depend is an adaption of the Java design quality metrics software JDepend 
and the NDepend metric tool.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir} -p $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
  %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
  %{__pear} uninstall --nodeps --ignore-errors --register-only \
    %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHP
%{_bindir}/pdepend
%doc %{pear_docdir}/%{pear_name}

%changelog
* Wed Sep 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- upstream 1.0.7, backport for remi repo

* Wed Sep 12 2012 Christof Damian <christof@damian.net> - 1.1.0-1
- upstream 1.1.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
 - Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.7-1
- upstream 1.0.7, backport for remi repo

* Tue May  1 2012 Christof Damian <christof@damian.net> - 1.0.7-1
- upstream 1.0.7

* Thu Apr 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.5-1
- upstream 1.0.5

* Wed Apr 11 2012 Christof Damian <christof@damian.net> - 1.0.5-1
- upstream 1.0.5

* Sat Mar 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.4-1
- upstream 1.0.4

* Tue Feb 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.3-1
- upstream 1.0.3

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-1
- upstream 1.0.2

* Sat Feb 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- upstream 1.0.1, rebuild for remi repository

* Thu Feb  9 2012 Christof Damian <christof@damian.net> - 1.0.1-1
- upstream 1.0.1

* Tue Nov 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.6-1
- upstream 0.10.6, rebuild for remi repository

* Sun Oct 30 2011 Christof Damian <christof@damian.net> - 0.10.6-1
- upstream 0.10.6

* Fri May 27 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.5-1
- upstream 0.10.5
- rebuild for remi repository

* Fri May 20 2011 Christof Damian <christof@damian.net> - 0.10.5-1
- upstream 0.10.5

* Fri Mar  4 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.3-1
- upstream 0.10.3
- rebuild for remi repository

* Fri Mar  4 2011 Christof Damian <christof@damian.net> - 0.10.3-1
- upstream 0.10.3

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.2-1
- upstream 0.10.2
- rebuild for remi repository

* Mon Feb 28 2011 Christof Damian <cdamian@robin.gotham.krass.com> - 0.10.2-1
- upstream 0.10.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 0.10.1-1
- upstream stable release 0.10.1 
- rebuild for remi repository

* Sun Feb  6 2011 Christof Damian <christof@damian.net> - 0.10.1-1
- upstream stable release 0.10.1 

* Sat Sep 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.19-1
- upstream 0.9.19
- rebuild for remi repository

* Fri Sep 17 2010 Christof Damian <christof@damian.net> - 0.9.19-1
- upstream 0.9.19

* Sat Sep 04 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.18-1
- rebuild for remi repository

* Fri Sep  3 2010 Christof Damian <christof@damian.net> - 0.9.18-1
- upstream 0.9.18

* Fri Jul 30 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.17-1
- rebuild for remi repository

* Fri Jul 30 2010 Christof Damian <christof@damian.net> - 0.9.17-1
- upstream 0.9.17

* Mon Jun 21 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.16-1
- rebuild for remi repository

* Sun Jun 20 2010 Christof Damian <christof@damian.net> - 0.9.16-1
- upstream 0.9.16: bugfixes

* Sun May 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.14-1
- rebuild for remi repository

* Sat May 22 2010 Christof Damian <christof@damian.net> - 0.9.14-1
- upstream 0.9.14

* Tue May 10 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.13-1
- rebuild for remi repository

* Mon May 10 2010 Christof Damian <christof@damian.net> - 0.9.13-1
- upstream 0.9.13 important bugfixes

* Thu Apr 29 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.12-1
- rebuild for remi repository

* Tue Apr 27 2010 Christof Damian <christof@damian.net> - 0.9.12-1
- upstream 0.9.12
- upstream removed all tests

* Thu Mar  4 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.11-1
- rebuild for remi repository

* Wed Mar  3 2010 Christof Damian <christof@damian.net> - 0.9.11-1
- upstream 0.9.11

* Thu Feb 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.10-1
- rebuild for remi repository

* Tue Feb 23 2010 Christof Damian <christof@damian.net> - 0.9.10-1
- upstream 0.9.10
- replaced define macro with global

* Mon Feb 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.9-2
- rebuild for remi repository

* Tue Jan 26 2010 Christof Damian <christof@damian.net> 0.9.9-2
- require pecl imagick, which is an optional requirement
- require php-xml for dom
- change postun to use channel macro for consistency
- own /usr/share/pear/PHP
- include test files (which currently don't work)

* Fri Jan 1 2010 Christof Damian <christof@damian.net> 0.9.9-1
- initial release
