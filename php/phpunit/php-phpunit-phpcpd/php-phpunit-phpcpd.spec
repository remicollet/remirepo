%global gh_commit    a9462153f2dd90466a010179901d31fbff598365
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpcpd
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    phpcpd
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-phpcpd
Version:        2.0.1
Release:        1%{?dist}
Summary:        Copy/Paste Detector (CPD) for PHP code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoload template
Source1:        autoload.php.in

# Fix for RPM, use autoload
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language)  >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-phpunit-FinderFacade >= 1.1.0
BuildRequires:  php-phpunit-Version >= 1.0.3
BuildRequires:  php-symfony-console >= 2.2.0
BuildRequires:  php-phpunit-PHP-Timer >= 1.0.4
BuildRequires:  php-theseer-fDOMDocument >= 1.4
%endif

# From composer.json
Requires:       php(language) >= 5.3.3
Requires:       php-phpunit-FinderFacade >= 1.1.0
Requires:       php-phpunit-Version >= 1.0.3
Requires:       php-symfony-console >= 2.2.0
Requires:       php-phpunit-PHP-Timer >= 1.0.4
Requires:       php-theseer-fDOMDocument >= 1.4
# From phpcompatinfo report for version 2.0.1
Requires:       php-dom
Requires:       php-mbstring
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-xml

# For compatibility with pear
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
phpcpd is a Copy/Paste Detector (CPD) for PHP code.

The goal of phpcpd is not not to replace more sophisticated tools such as phpcs,
pdepend, or phpmd, but rather to provide an alternative to them when you just
need to get a quick overview of duplicated code in a project.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm


%build
phpab \
  --output   src/autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPCPD

install -D -p -m 755 phpcpd %{buildroot}%{_bindir}/phpcpd


%if %{with_tests}
%check
phpunit \
   --bootstrap src/autoload.php \
   -d date.timezone=UTC \
   tests
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{php_home}/PHPCPD
%{_bindir}/phpcpd


%changelog
* Sun May  4 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1
- sources from github
- run test suite during build

* Fri Nov 08 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0
- drop dependency on components.ez.no/ConsoleTools
- add dependency on pear.symfony.com/Console >= 2.2.0
- raise dependency on pear.phpunit.de/FinderFacade >= 1.1.0

* Tue Jul 30 2013 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Update to 1.4.2

* Thu Apr 04 2013 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1
- new dependency on pear.phpunit.de/Version

* Thu Oct 11 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- Update to 1.4.0
- use FinderFacade instead of File_Iterator
- raise dependecies: php >= 5.3.3, PHP_Timer >= 1.0.4

* Sat Nov 26 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.5-1
- Update to 1.3.5

* Tue Nov 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.4-1
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

* Wed Nov 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- rebuild for remi repository

* Thu Oct 15 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.0-1
- Initial packaging
