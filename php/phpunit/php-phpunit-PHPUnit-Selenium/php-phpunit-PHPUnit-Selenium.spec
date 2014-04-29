# spec file for php-phpunit-PHPUnit-Selenium
#
# Copyright (c) 2010-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    e89bfa1080dce9617c9b3e7760d50752974bfbd2
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpunit-selenium
%global php_home     %{_datadir}/php
%global pear_name    PHPUnit_Selenium
%global pear_channel pear.phpunit.de
# No test, as test suite requires a Selenium server

Name:           php-phpunit-PHPUnit-Selenium
Version:        1.3.3
Release:        2%{?dist}
Summary:        Selenium RC integration for PHPUnit

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3

# From composer.json
Requires:       php(language) >= 5.3.3
Requires:       php-pear-PHPUnit >= 3.7.0
Requires:       php-curl
Requires:       php-dom
# From phpcompatinfo report for version 1.3.3
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-zip

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Selenium RC integration for PHPUnit.

This package contains a base Testcase Class that can be used to run end-to-end
tests against Selenium 2 (using its Selenium 1 backward compatible Api).

Optional dependency: XDebug (php-pecl-xdebug)


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm PHPUnit/Extensions/SeleniumCommon/Autoload.php.in


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it.
# Also remember to fix the command to use it.

#phpab \
#  --output   PHPUnit/Extensions/SeleniumCommon/Autoload.php \
#  --template PHPUnit/Extensions/SeleniumCommon/Autoload.php.in \
#  PHPUnit


%install
rm -rf         %{buildroot}
mkdir -p       %{buildroot}%{php_home}
cp -pr PHPUnit %{buildroot}%{php_home}/PHPUnit


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ChangeLog.markdown LICENSE README.md
%{php_home}/PHPUnit/Extensions/Selenium*


%changelog
* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.3.3-2
- sources from github

* Fri Nov 22 2013 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- Update to 1.3.3 (stable)
- improve description

* Mon Aug 26 2013 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Mon Jun 03 2013 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Mon May 06 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Feb 04 2013 Remi Collet <remi@fedoraproject.org> - 1.2.12-1
- Version 1.2.12 (stable) - API 1.2.1 (stable)

* Mon Dec 10 2012 Remi Collet <remi@fedoraproject.org> - 1.2.11-1
- Version 1.2.11 (stable) - API 1.2.1 (stable)

* Mon Oct 22 2012 Remi Collet <remi@fedoraproject.org> - 1.2.10-1
- Version 1.2.10 (stable) - API 1.2.1 (stable)

* Sat Sep 29 2012 Remi Collet <remi@fedoraproject.org> - 1.2.9-1
- Version 1.2.9 (stable) - API 1.2.1 (stable)
- raise dependencies: php 5.3.3, PHPUnit 3.7.0

* Thu Aug  9 2012 Remi Collet <remi@fedoraproject.org> - 1.2.8-1
- Version 1.2.8 (stable) - API 1.2.1 (stable)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- Version 1.2.7 (stable) - API 1.2.1 (stable)

* Sun Apr 01 2012 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Version 1.2.6 (stable) - API 1.2.1 (stable)

* Sat Mar 17 2012 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Version 1.2.5 (stable) - API 1.2.1 (stable)

* Mon Mar 12 2012 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Version 1.2.4 (stable) - API 1.2.1 (stable)

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.1 (stable)

* Mon Jan 23 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.1 (stable)
- add Selenium2TestCase extension

* Mon Jan 16 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Version 1.1.3 (stable) - API 1.1.0 (stable)

* Mon Dec 12 2011 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)

* Wed Nov 30 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.0 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.2-3
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)
- CHANGELOG and LICENSE are now in the tarball

* Wed Nov 17 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-2
- lower PEAR dependency to allow el6 build
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean

