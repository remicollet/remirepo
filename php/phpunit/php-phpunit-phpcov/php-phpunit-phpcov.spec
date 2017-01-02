# spec file for php-phpunit-phpcov
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    9ef291483ff65eefd8639584d61bbfb044d747f3
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpcov
%global php_home     %{_datadir}/php/SebastianBergmann
%global pear_name    phpcov
%global pear_channel pear.phpunit.de
# not Ready
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}


Name:           php-phpunit-phpcov
Version:        2.0.2
Release:        1%{?dist}
Summary:        TextUI front-end for PHP_CodeCoverage

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Autoload template
Source1:        autoload.php.in

# Fix autoload for RPM
Patch0:         %{gh_project}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit) >= 4.1
BuildRequires:  php-composer(phpunit/php-code-coverage) >= 2.0
BuildRequires:  php-composer(sebastian/diff) >= 1.1
BuildRequires:  php-composer(sebastian/diff) <  2
BuildRequires:  php-composer(sebastian/finder-facade) >= 1.1
BuildRequires:  php-composer(sebastian/finder-facade) <  2
BuildRequires:  php-composer(sebastian/version) >= 1.0.3
BuildRequires:  php-composer(sebastian/version) <  1.1
BuildRequires:  php-symfony-console >= 2.2
%endif

# from composer.json
#        "php": ">=5.3.3",
#        "phpunit/phpunit": ">=4.1",
#        "phpunit/php-code-coverage": "~2.0",
#        "sebastian/diff": "~1.1",
#        "sebastian/finder-facade": "~1.1",
#        "sebastian/version": "~1.0",
#        "symfony/console": "~2.2"
Requires:       php(language) >= 5.3.3
Requires:       php-composer(phpunit/phpunit) >= 4.1
Requires:       php-composer(phpunit/php-code-coverage) >= 2.0
Requires:       php-composer(phpunit/php-code-coverage) <  3
Requires:       php-composer(sebastian/diff) >= 1.1
Requires:       php-composer(sebastian/diff) <  2
Requires:       php-composer(sebastian/finder-facade) >= 1.1
Requires:       php-composer(sebastian/finder-facade) <  2
Requires:       php-composer(sebastian/version) >= 1.0
Requires:       php-composer(sebastian/version) <  2
Requires:       php-symfony-console >= 2.2
# from phpcompatinfo report for version 1.1.0
Requires:       php-reflection
Requires:       php-spl

Provides:       php-composer(phpunit/phpcov) = %{version}

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
# Project name
Provides:       phpcov = %{version}


%description
TextUI front-end for PHP_CodeCoverage.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm


%build
phpab \
  --output   src/autoload.php \
  --template %{SOURCE1} \
  src


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr src %{buildroot}%{php_home}/PHPCOV

install -D -p -m 755 phpcov %{buildroot}%{_bindir}/phpcov


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
%{php_home}/PHPCOV
%{_bindir}/phpcov


%changelog
* Mon Oct  5 2015 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- update to 2.0.2
- allow PHPUnit 5

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- update to 2.0.1
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0
- sources from github

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
