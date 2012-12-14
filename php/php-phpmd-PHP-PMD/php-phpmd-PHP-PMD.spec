%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    PHP_PMD
%global pear_channel pear.phpmd.org

Name:           php-phpmd-PHP-PMD
Version:        1.4.1
Release:        1%{?dist}
Summary:        PHPMD - PHP Mess Detector

Group:          Development/Libraries
License:        BSD
URL:            http://www.phpmd.org/
Source0:        http://pear.phpmd.org/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear
BuildRequires:  php-channel(%{pear_channel})

Requires:       php-channel(%{pear_channel})
Requires:       php(language) >= 5.2.3
Requires:       php-dom
Requires:       php-pcre
Requires:       php-simplexml
Requires:       php-spl
# phpci detected
Requires:       php-date
Requires:       php-libxml
Requires:       php-pear(pear.pdepend.org/PHP_Depend) >= 1.1.0
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This is the project site of PHPMD. It is a spin-off project of PHP Depend 
and aims to be a PHP equivalent of the well known Java tool PMD. PHPMD can 
be seen as an user friendly front-end application for the raw metrics 
stream measured by PHP Depend.


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
    %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHP/PMD.php
%{pear_phpdir}/PHP/PMD
%{pear_datadir}/PHP_PMD
%{_bindir}/phpmd

%changelog
* Fri Dec 14 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.1-1
- upstream 1.4.1 for remi repo
- spec cleanups

* Sat Sep  8 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- upstream 1.4.0

* Sat Mar 03 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.3-1
- upstream 1.3.3

* Tue Feb 28 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.2-1
- upstream 1.3.2

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- upstream 1.3.1

* Sat Feb 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-1
- upstream 1.3.0, rebuild for remi repository

* Thu Feb  9 2012 Christof Damian <christof@damian.net> - 1.3.0-1
- upstream 1.3.0

* Tue Nov 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- upstream 1.2.0, rebuild for remi repository
- doc in /usr/share/doc/pear

* Fri Oct 28 2011 Christof Damian <christof@damian.net> - 1.2.0-1
- upstream 1.2.0

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-1
- rebuild for remi repository

* Fri Jul 15 2011 Christof Damian <christof@damian.net> - 1.1.1-1
- upstream 1.1.1

* Fri Mar 25 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- rebuild for remi repository

* Thu Mar 24 2011 Christof Damian <christof@damian.net> - 1.1.0-1
- upstream 1.1.0

* Wed Feb 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- upstream 1.0.1 - bugfixes
- rebuild for remi repository

* Tue Feb 15 2011 Christof Damian <christof@damian.net> - 1.0.1-1
- upstream 1.0.1 - bugfixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- upstream stable release 1.0.0
- rebuild for remi repository

* Sun Feb  6 2011 Christof Damian <christof@damian.net> - 1.0.0-1
- upstream stable release 1.0.0

* Sun Oct  3 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.7-1
- new upstream
- rebuild for remi repository

* Sat Oct  2 2010 Christof Damian <christof@damian.net> - 0.2.7-1
- new upstream

* Mon Jul  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.6-1
- rebuild for remi repository

* Sun Jul  4 2010 Christof Damian <christof@damian.net> - 0.2.6-1
- upstream 0.2.6

* Mon Apr  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.5-1
- rebuild for remi repository

* Sun Apr  4 2010 Christof Damian <christof@damian.net> - 0.2.5-1
- upsteam 0.2.5: bugfixes

* Thu Mar  9 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.4-1
- rebuild for remi repository

* Tue Mar  9 2010 Christof Damian <christof@damian.net> - 0.2.4-1
- upstream 0.2.4 : Small bugfix release which closes an E_NOTICE issue introduced with release 0.2.3

* Sat Mar  6 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.3-1
- rebuild for remi repository

* Thu Mar  4 2010 Christof Damian <christof@damian.net> - 0.2.3-1
- upstream 0.2.3
- increased php and pdepend requirements 

* Mon Feb 01 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.2.2-2
- rebuild for remi repository

* Sun Jan 31 2010 Christof Damian <christof@damian.net> - 0.2.2-2
- use pear_datadir in filesection

* Sat Jan 30 2010 Christof Damian <christof@damian.net> 0.2.2-1
- upstream 0.2.2
- changed define to global
- moved docs to /usr/share/doc
- use channel macro in postun

* Tue Jan 12 2010 Christof Damian <christof@damian.net> - 0.2.1-1
- upstream 0.2.1

* Fri Jan 1 2010 Christof Damian <christof@damian.net> 0.2.0-1
- initial release

