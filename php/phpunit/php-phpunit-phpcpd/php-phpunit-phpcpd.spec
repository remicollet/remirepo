# remirepo/fedora spec file for php-phpunit-phpcpd
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global gh_commit    d7006078b75a34c9250831c3453a2e256a687615
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpcpd
%global php_home     %{_datadir}/php
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
# Packagist
%global pk_vendor    sebastian
%global pk_project   phpcpd
# Namespace
%global ns_vendor    SebastianBergmann
%global ns_project   PHPCPD

Name:           php-phpunit-%{pk_project}
Version:        3.0.0
Release:        1%{?dist}
Summary:        Copy/Paste Detector (CPD) for PHP code

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Fix for RPM, use autoload
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language)  >= 5.6
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(sebastian/finder-facade) >= 1.1
BuildRequires:  php-composer(sebastian/version)       >= 1.0
BuildRequires:  php-composer(symfony/console)         >= 2.7
BuildRequires:  php-composer(phpunit/php-timer)       >= 1.0.6
%endif

# From composer.json, requires
#        "php": "^5.6|^7.0",
#        "sebastian/finder-facade": "^1.1",
#        "sebastian/version": "^2.0",
#        "symfony/console": "^3.0",
#        "phpunit/php-timer": "^1.0.6"
Requires:       php(language) >= 5.6
Requires:       php-composer(sebastian/finder-facade) >= 1.1
Requires:       php-composer(sebastian/finder-facade) <  2
Requires:       php-composer(sebastian/version)       >= 2.0
Requires:       php-composer(sebastian/version)       <  3
# temporarily ignore min version
Requires:       php-composer(symfony/console)         >= 2.8
Requires:       php-composer(symfony/console)         <  4
Requires:       php-composer(phpunit/php-timer)       >= 1.0.6
# From phpcompatinfo report for version 3.0.0
Requires:       php-cli
Requires:       php-dom
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-xml

Provides:       %{pk_project} = %{version}
Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}


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
  --template fedora \
  src

cat << 'EOF' | tee -a src/autoload.php
// Dependencies
\Fedora\Autoloader\Dependencies::required([
    '%{php_home}/%{ns_vendor}/FinderFacade/autoload.php',
    '%{php_home}/%{ns_vendor}/Version/autoload.php',
    [
        '%{php_home}/Symfony3/Component/Console/autoload.php',
        '%{php_home}/Symfony/Component/Console/autoload.php',
    ],
    '%{php_home}/PHP/Timer/Autoload.php',
]);
EOF


%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}

install -D -p -m 755 phpcpd %{buildroot}%{_bindir}/phpcpd


%check
%if %{with_tests}
mkdir vendor
ln -s %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php vendor/autoload.php

ret=0;
for cmd in php56 php70 php71 php; do
   if which $cmd; then
      $cmd %{_bindir}/phpunit --verbose || ret=1
   fi
done
exit $ret
%else
: Test suite skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%{php_home}/%{ns_vendor}/%{ns_project}
%{_bindir}/%{pk_project}


%changelog
* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0
- raise dependency on PHP 5.6
- drop dependency on theseer/fdomdocument
- raise dependency on sebastian/version 2.0
- cleanup update from pear
- switch to fedora/autoloader

* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4  (no change)
- allow sebastian/version 2.0

* Sun Apr 17 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3
- raise dependency on Symfony >= 2.7
- run test suite with both PHP 5 and 7 when available
- allow to run with PHP from SCL
- provide php-composer(sebastian/phpcpd)

* Thu Mar 26 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2
- use composer dependencies
- fix license handling

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
