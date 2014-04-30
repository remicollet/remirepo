# spec file for php-phpunit-PHPUnit-Story
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    b8579ada6ede4fd2f4b49e8549a8a176606cae68
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   phpunit-story
%global php_home     %{_datadir}/php
%global pear_name    PHPUnit_Story
%global pear_channel pear.phpunit.de
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-PHPUnit-Story
Version:        1.0.2
Release:        4%{?dist}
Summary:        Story extension for PHPUnit to facilitate Behaviour-Driven Development

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3

# From composer.json
Requires:       php(language) >= 5.3.3
Requires:       php-spl
Requires:       php-phpunit-PHPUnit >= 3.6.0

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Story extension for PHPUnit to facilitate Behaviour-Driven Development

%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm PHPUnit/Extensions/Story/Autoload.php.in


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it
#phpab \
#  --output   PHPUnit/Extensions/Story/Autoload.php \
#  --template PHPUnit/Extensions/Story/Autoload.php.in \
#  PHPUnit


%install
rm -rf         %{buildroot}
mkdir -p       %{buildroot}%{php_home}
cp -pr PHPUnit %{buildroot}%{php_home}


%if %{with_tests}
%check
phpunit \
  -d date.timezone=UTC
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null
fi


%files
%defattr(-,root,root,-)
%doc ChangeLog.markdown LICENSE composer.json
%{php_home}/PHPUnit/Extensions/Story


%changelog
* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-4
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- sources from github
- run test suite when build --with tests

* Wed Apr 03 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2 (no change)

* Thu Mar 28 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- initial package
