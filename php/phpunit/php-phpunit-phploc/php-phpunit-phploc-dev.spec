# remirepo/fedora spec file for php-phpunit-phploc
#
# Copyright (c) 2009-2016 Guillaume Kulakowski, Christof Damian, Remi Collet
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global gh_commit    2917d010fbfd503d9e836cefff249cb3c1b3f17a
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phploc
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    phploc
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-phploc
Version:        3.0.0
Release:        2%{?dist}
Summary:        A tool for quickly measuring the size of a PHP project

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Fix for RPM, use autoload
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.6
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php-composer(sebastian/finder-facade) >= 1.1
BuildRequires:  php-composer(sebastian/finder-facade) <  2
BuildRequires:  php-composer(sebastian/git) >= 2.0
BuildRequires:  php-composer(sebastian/git) <  3
BuildRequires:  php-composer(sebastian/version) >= 1.0.3
BuildRequires:  php-composer(sebastian/version) <  3
BuildRequires:  php-composer(symfony/console) >= 2.5
BuildRequires:  php-composer(symfony/console) <  4
# For our autoloader
BuildRequires:  php-composer(symfony/class-loader)
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "~5"
BuildRequires:  php-composer(phpunit/phpunit) >= 5
%endif

# From composer.json, "require": {
#      "php": ">=5.6",
#      "sebastian/finder-facade": "~1.1",
#      "sebastian/git": "~2.0",
#      "sebastian/version": "~1.0.3",
#      "symfony/console": "~2.5|~3.0"
Requires:       php(language) >= 5.6
Requires:       php-cli
Requires:       php-composer(sebastian/finder-facade) >= 1.1
Requires:       php-composer(sebastian/finder-facade) <  2
Requires:       php-composer(sebastian/git) >= 2.0
Requires:       php-composer(sebastian/git) <  3
Requires:       php-composer(sebastian/version) >= 1.0.3
Requires:       php-composer(sebastian/version) <  3
Requires:       php-composer(symfony/console) >= 2.5
Requires:       php-composer(symfony/console) <  4
# From phpcompatinfo report for version 2.1.3
Requires:       php-dom
Requires:       php-spl
Requires:       php-tokenizer
# For our autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(phploc/phploc) = %{version}
# For compat
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       phploc = %{version}


%description
phploc is a tool for quickly measuring the size of a PHP project.

The goal of phploc is not not to replace more sophisticated tools such as phpcs,
pdepend, or phpmd, but rather to provide an alternative to them when you just
need to get a quick understanding of a project's size.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm


%build
%{_bindir}/phpab \
  --output   src/autoload.php \
  src

cat << 'EOF' | tee -a src/autoload.php
// Dependencies
$vendorDir = '/usr/share/php';
require_once $vendorDir . '/SebastianBergmann/FinderFacade/autoload.php';
require_once $vendorDir . '/SebastianBergmann/Git/autoload.php';
require_once $vendorDir . '/SebastianBergmann/Version/autoload.php';
require_once $vendorDir . '/TheSeer/fDOMDocument/autoload.php';
require_once $vendorDir . '/Symfony/Component/Console/autoloader.php';
EOF


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPLOC

install -D -p -m 755 phploc %{buildroot}%{_bindir}/phploc


%if %{with_tests}
%check
%{_bindir}/phpunit \
   --bootstrap %{buildroot}%{php_home}/PHPLOC/autoload.php \
   --verbose tests

if which php70; then
   php70 %{_bindir}/phpunit \
      --bootstrap %{buildroot}%{php_home}/PHPLOC/autoload.php \
      --verbose tests
fi
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
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%{php_home}/PHPLOC
%{_bindir}/phploc


%changelog
* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-2
- allow sebastian/version 2.0

* Wed Jan 13 2016 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- raise minimal php version to 5.6
- raise dependency on PHPUnit ~5
- allow symfony 3

* Thu Oct 22 2015 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- update to 2.1.5
- simplify autoloader

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- update to 2.1.4

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 2.1.3-2
- switch to $fedoraClassLoader autoloader

* Thu Jun  4 2015 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- update to 2.1.3
- improve autoloader
- lower minimal PHP version to 5.3.3
- fix license handling

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- update to 2.1.2
- ensure compatibility with SCL

* Mon Apr 13 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- update to 2.1.1

* Wed Mar 11 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0
- raise dependencies on sebastian/git 2.0, symfony/console 2.5
- raise minimal PHP version to 5.4

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- update to 2.0.6
- composer dependencies

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- fix scriptlet

* Sat May  3 2014 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- update to 2.0.5
- sources from github
- run test suite during build

* Wed Dec 18 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Nov 05 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Aug 28 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0
- add requires symfony2/Console, phpunit/Git and phpunit/Version
- drop requires ezc/Console

* Mon Nov 12 2012 Remi Collet <remi@fedoraproject.org> - 1.7.4-1
- Version 1.7.4 (stable) - API 1.7.0 (stable)

* Fri Nov  9 2012 Remi Collet <remi@fedoraproject.org> - 1.7.3-1
- Version 1.7.3 (stable) - API 1.7.0 (stable)

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- Version 1.7.2 (stable) - API 1.7.0 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Version 1.7.1 (stable) - API 1.7.0 (stable)
- use FinderFacade instead of File_Iterator
- raise dependecies: php >= 5.3.3

* Tue Nov 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.4-1
- upstream 1.6.4, rebuild for remi repository

* Sun Nov 20 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.4-1
- upstream 1.6.4

* Thu Nov 03 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-1
- upstream 1.6.2, rebuild for remi repository

* Tue Nov  1 2011 Christof Damian <christof@damian.net> - 1.6.2-1
- upstream 1.6.2

* Sat Feb 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.1-1
- rebuild for remi repository

* Sat Feb 12 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.1-1
- upstream 1.6.1

* Fri Feb 12 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.5.1-1
- rebuild for remi repository

* Wed Feb 10 2010 Christof Damian <christof@damian.net> 1.5.1-1
- upstream 1.5.1
- changed requirements
- replaced define macros with global

* Sat Jan 16 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-2
- rebuild for remi repository

* Thu Jan 14 2010 Christof Damian <christof@damian.net> - 1.5.0-2
- add php 5.2.0 dependency
- remove hack to lower pear requirement

* Sun Jan  3 2010 Christof Damian <christof@damian.net> - 1.5.0-1
- upstream 1.5.0

* Fri Dec 18 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.4.0-2
- /usr/share/pear/PHPLOC wasn't owned

* Fri Dec 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-1
- rebuild for remi repository

* Sat Dec 12 2009 Christof Damian <christof@damian.net> - 1.4.0-1
- upstream 1.4.0

* Wed Nov 11 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-2
- rebuild for remi repository

* Sat Nov  7 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.0-2
- F-(10|11) compatibility

* Tue Oct 13 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.0-1
- Initial packaging
