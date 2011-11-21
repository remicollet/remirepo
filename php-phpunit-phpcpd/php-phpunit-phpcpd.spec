%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name phpcpd
%global channel pear.phpunit.de

Name:           php-phpunit-phpcpd
Version:        1.3.4
Release:        1%{?dist}
Summary:        Copy/Paste Detector (CPD) for PHP code

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/sebastianbergmann/phpcpd
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.9.4
BuildRequires:  php-channel(%{channel})
Requires:       php-common >= 5.2.7
Requires:       php-tokenizer
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.phpunit.de/File_Iterator) >= 1.3.0
Requires:       php-pear(pear.phpunit.de/PHP_Timer) >= 1.0.2
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6 

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
phpcpd is a Copy/Paste Detector (CPD) for PHP code.

The goal of phpcpd is not not to replace more sophisticated tools such as phpcs,
pdepend, or phpmd, but rather to provide an alternative to them when you just
need to get a quick overview of duplicated code in a project.


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
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


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
%{pear_phpdir}/PHPCPD
%{_bindir}/phpcpd


%changelog
* Mon Nov 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.4-1
- upstream 1.3.4, rebuild for remi repository

* Sun Nov 20 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.3.4-1
- upstream 1.3.4

* Mon Nov 07 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.3-1
- upstream 1.3.3, rebuild for remi repository

* Sat Nov 05 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.3.3-1
- upstream 1.3.3

* Sun Oct 17 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.3.2-1
- rebuild for remi repository

* Sun Oct 17 2010 Christof Damian <christof@damian.net> - 1.3.2-1
- upstream 1.3.2
- new requirement phpunit/PHP_Timer
- increased requirement phpunit/File_Iterator to 1.2.2

* Fri Feb 12 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- rebuild for remi repository

* Wed Feb 10 2010 Christof Damian <christof@damian.net> 1.3.1-1
- upstream 1.3.1
- change define macros to global
- use channel macro in postun
- raise requirements

* Sat Jan 16 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-2
- rebuild for remi repository

* Thu Jan 14 2010 Christof Damian <christof@damian.net> - 1.3.0-2
- forgot tgz file

* Thu Jan 14 2010 Christof Damian <christof@damian.net> - 1.3.0-1
- upstream 1.3.0
- add php 5.2.0 dependency
- raise pear require

* Fri Dec 18 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.2-2
- /usr/share/pear/PHPCPD wasn't owned

* Fri Dec 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-1
- rebuild for remi repository

* Sat Dec 12 2009 Christof Damian <christof@damian.net> - 1.2.2-1
- upstream 1.2.2

* Thu Nov 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- rebuild for remi repository

* Thu Oct 15 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.0-1
- Initial packaging
