# remirepo/fedora spec file for php-phpunit-dbunit3
#
# Copyright (c) 2010-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    f2f8bec1d6ad7ad0bcdb47c1ed56d9d42d3e39ab
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   dbunit
%global php_home     %{_datadir}/php
# Packagist
%global pk_vendor    phpunit
%global pk_project   dbunit
# Namespace
%global ns_vendor    PHPUnit6
%global ns_project   DbUnit
%global with_tests   0%{!?_without_tests:1}
%global ver_major    3
%global ver_minor    0
%global ver_patch    0
%global specrel      1

Name:           php-%{pk_vendor}-%{pk_project}%{ver_major}
Version:        %{ver_major}.%{ver_minor}.%{ver_patch}
Release:        %{specrel}%{?dist}
Summary:        PHPUnit extension for database interaction testing

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildArch:      noarch
BuildRequires:  php-fedora-autoloader-devel
%if %{with_tests}
BuildRequires:  php(language) >= 7.0
BuildRequires:  php-pdo
BuildRequires:  php-simplexml
BuildRequires:  phpunit6
BuildRequires:  php-composer(symfony/yaml) <  4
BuildRequires:  php-composer(symfony/yaml) >= 2.8
%endif

# From composer.json
#        "php": "^7.0",
#        "phpunit/phpunit": "^6.0",
#        "symfony/yaml": "^3.0",
#        "ext-pdo": "*",
#        "ext-simplexml": "*"
Requires:       php(language) >= 7.0
Requires:       php-pdo
Requires:       php-simplexml
Requires:       phpunit6
# ignore min version
Requires:       php-composer(symfony/yaml)    <  4
Requires:       php-composer(symfony/yaml)    >= 2.8
# From phpcompatinfo report for version 3.0.0
Requires:       php-reflection
Requires:       php-libxml
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

%if 0%{?fedora} > 99
Obsoletes:      php-phpunit-Dbunit < %{ver_major}
Provides:       php-phpunit-Dbunit = %{version}
Provides:       %{pk_project}       = %{version}
Provides:       php-composer(%{pk_vendor}/%{pk_project}) = %{version}
%endif


%description
PHPUnit extension for database interaction testing.

Autoloader: %{php_home}/%{ns_vendor}/%{ns_project}/autoload.php


%prep
%setup -q -n %{gh_project}-%{gh_commit}



%build
: Generate library autoloader
%{_bindir}/phpab \
   --template fedora \
   --output src/autoload.php \
   src

cat << 'EOF' | tee -a src/autoload.php
// Dependencies
\Fedora\Autoloader\Dependencies::required([
    [
        '%{php_home}/Symfony3/Component/Yaml/autoload.php',
        '%{php_home}/Symfony/Component/Yaml/autoload.php',
    ],
]);
EOF

%install
mkdir -p   %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}


%if %{with_tests}
%check
: Generate tests autoloader
mkdir vendor
ln -s %{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php vendor/autoload.php

: Run tests
%{_bindir}/phpunit6 --verbose
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc ChangeLog.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}


%changelog
* Wed Feb  8 2017 Remi Collet <remi@fedoraproject.org> - 3.0.0-1
- rename to php-phpunit-dbunit3
- change dependency to phpunit6

* Sun Dec  4 2016 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- update to 2.0.3
- switch to fedora/autoloader

* Tue Nov  3 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2 (no change)
- lower dependency on PHP version 5.4
- lower dependency on PHPUnit version 4

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (no change)

* Fri Oct  2 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- raise dependency on PHP version 5.6
- raise dependency on PHPUnit version 5

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- update to 1.4.1

* Fri Jun  5 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0
- raise dependency on PHPUnit 4.0
- disable test suite on EL-5

* Sun Mar 29 2015 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- update to 1.3.2
- switch all dependencies to composer

* Sun Jun 08 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-4
- fix FTBFS, add BR php-pdo
- add composer provides
- add composer.json as doc

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-3
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-2
- sources from github
- run tests during build

* Tue Apr 01 2014 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Fri Nov 01 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- add requires: symfony2/Yaml

* Tue Mar 05 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Version 1.2.3 (stable) - API 1.2.0 (stable)

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Version 1.2.2 (stable) - API 1.2.0 (stable)

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Version 1.2.1 (stable) - API 1.2.0 (stable)

* Thu Sep 20 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependencies: php 5.3.3, PHPUnit 3.7.0,
  Yaml 2.1.0 (instead of YAML from symfony 1)

* Fri Jan 27 2012 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Version 1.1.2 (stable) - API 1.1.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Version 1.1.1 (stable) - API 1.1.0 (stable)

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Fri Aug 19 2011 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Version 1.0.3 (stable) - API 1.0.0 (stable)

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)
- remove PEAR hack (only needed for EPEL)
- raise PEAR dependency to 1.9.2

* Tue May  3 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-2
- rebuild for doc in /usr/share/doc/pear

* Wed Feb 16 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 05 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-2
- lower PEAR dependency to allow el6 build
- fix URL

* Sun Sep 26 2010 Remi Collet <Fedora@famillecollet.com> - 1.0.0-1
- initial generated spec + clean


