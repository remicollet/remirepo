# spec file for php-phpunit-phploc
#
# Copyright (c) 2009-2015 Guillaume Kulakowski, Christof Damian, Remi Collet
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%global gh_commit    a47a7c4758bdfb7cebbb1ccaa2c9df882b10db7f
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phploc
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    phploc
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-phploc
Version:        2.1.1
Release:        1%{?dist}
Summary:        A tool for quickly measuring the size of a PHP project

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
BuildRequires:  php(language) >= 5.4
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-composer(sebastian/finder-facade) >= 1.1
BuildRequires:  php-composer(sebastian/finder-facade) <  2
BuildRequires:  php-composer(sebastian/git) >= 2.0
BuildRequires:  php-composer(sebastian/git) <  3
BuildRequires:  php-composer(sebastian/version) >= 1.0.3
BuildRequires:  php-composer(sebastian/version) <  2
BuildRequires:  php-symfony-console >= 2.5
BuildRequires:  php-symfony-console <  3
%endif

# From composer.json
#      "php": ">=5.3.3",
#      "sebastian/finder-facade": "~1.1",
#      "sebastian/git": "~2.0",
#      "sebastian/version": "~1.0.3",
#      "symfony/console": "~2.5"
Requires:       php(language) >= 5.4
Requires:       php-composer(sebastian/finder-facade) >= 1.1
Requires:       php-composer(sebastian/finder-facade) <  2
Requires:       php-composer(sebastian/git) >= 2.0
Requires:       php-composer(sebastian/git) <  3
Requires:       php-composer(sebastian/version) >= 1.0.3
Requires:       php-composer(sebastian/version) <  2
Requires:       php-symfony-console >= 2.5
Requires:       php-symfony-console <  3
# From phpcompatinfo report for version 2.0.5
Requires:       php-dom
Requires:       php-spl
Requires:       php-tokenizer

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
phpab \
  --output   src/autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPLOC

install -D -p -m 755 phploc %{buildroot}%{_bindir}/phploc


%if %{with_tests}
%check
phpunit \
   --bootstrap src/autoload.php \
   --verbose tests
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
%{php_home}/PHPLOC
%{_bindir}/phploc


%changelog
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
