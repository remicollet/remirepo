# remirepo/fedora spec file for php-phpunit-PHPUnit-SkeletonGenerator
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    c0eeb18f31893c2f0c387bce84f8a3816a0eacd1
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpunit-skeleton-generator
%global php_home     %{_datadir}/php
%global pear_name    PHPUnit_SkeletonGenerator
%global pear_channel pear.phpunit.de
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           php-phpunit-PHPUnit-SkeletonGenerator
Version:        2.0.1
Release:        5%{?dist}
Summary:        Tool that can generate skeleton test classes

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoloader template
Source1:        autoload.php.in

# Autoloader for RPM - die composer !
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  php-composer(phpunit/php-text-template) >= 1.2
BuildRequires:  php-composer(sebastian/version)         >= 1.0
BuildRequires:  php-composer(symfony/console)           >= 2.4
# From composer.json, requires-dev
#        "mikey179/vfsStream": "~1.2"
#        "phpunit/phpunit": "~4.0",
BuildRequires:  php-composer(mikey179/vfsStream)        >= 1.2
BuildRequires:  %{_bindir}/phpunit
# For our autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# From composer.json, requires
#        "php": ">=5.3.3",
#        "phpunit/php-text-template": "~1.2",
#        "sebastian/version": "~1.0",
#        "symfony/console": "~2.4"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(phpunit/php-text-template) >= 1.2
Requires:       php-composer(phpunit/php-text-template) <  2
Requires:       php-composer(sebastian/version)         >= 1.0
Requires:       php-composer(sebastian/version)         <  3
Requires:       php-composer(symfony/console)           >= 2.4
Requires:       php-composer(symfony/console)           <  3
# Need for our autoloader patch
Requires:       php-composer(symfony/class-loader)
# From phpcompatinfo report from 2.0.0
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tokenizer

Provides:       php-composer(phpunit/phpunit-skeleton-generator) = %{version}


%description
Tool that can generate skeleton test classes from production code classes
and vice versa.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm

find . -type f -name \*.rpm -print | xargs rm


%build
phpab \
  --output   src/autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}/SebastianBergmann/PHPUnit
cp -pr src %{buildroot}%{php_home}/SebastianBergmann/PHPUnit/SkeletonGenerator

install -D -p -m 755 phpunit-skelgen %{buildroot}%{_bindir}/phpunit-skelgen


%clean
rm -rf %{buildroot}


%if %{with_tests}
%check
cd build
%{_bindir}/phpunit \
  --bootstrap %{buildroot}%{php_home}/SebastianBergmann/PHPUnit/SkeletonGenerator/autoload.php \
  --verbose

if which php70; then
  php70 %{_bindir}/phpunit \
    --bootstrap %{buildroot}%{php_home}/SebastianBergmann/PHPUnit/SkeletonGenerator/autoload.php \
    --verbose
fi
%endif


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc README.md LICENSE composer.json
%{_bindir}/phpunit-skelgen
%dir %{php_home}/SebastianBergmann
%dir %{php_home}/SebastianBergmann/PHPUnit
     %{php_home}/SebastianBergmann/PHPUnit/SkeletonGenerator


%changelog
* Mon Apr 18 2016 Remi Collet <remi@fedoraproject.org> - 2.0.1-5
- allow sebastian/version 2.0

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 2.0.1-3
- use $fedoraClassLoader autoloader

* Tue Jul 22 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- composer dependencies

* Fri May 16 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1 (no change)

* Tue May 13 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- add BR on php-mikey179-vfsstream
- enable test during build

* Tue May 13 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- add generated autoloader
- switch from php-ezc-ConsoleTools to php-symfony-Console
- add dependency on php-phpunit-Version

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-3
- sources from github

* Sat Jun 01 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add explicit requires

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)
- raise dependency: php >= 5.3.3

* Sat Mar 03 2012 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Sat Jan 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
