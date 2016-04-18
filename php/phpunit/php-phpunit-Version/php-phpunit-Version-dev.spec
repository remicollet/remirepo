# remirepo/fedora spec file for php-phpunit-Version
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    58b3a85e7999757d6ad81c787a1fbf5ff6c628c6
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   version
%global php_home     %{_datadir}/php/SebastianBergmann/
%global with_tests   %{?_without_tests:0}%{!?_withou_tests:1}

Name:           php-phpunit-Version
Version:        1.0.6
Release:        1%{?dist}
Summary:        Managing the version number of Git-hosted PHP projects

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab

Requires:       php(language) >= 5.3.3
Requires:       php-spl
Requires:       git

Provides:       php-composer(sebastian/version) = %{version}


%description
Library that helps with managing the version number
of Git-hosted PHP projects.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

: Restore PSR-0 layout
mkdir src/Version


%build
: Generate autoloader
%{_bindir}/phpab \
  --output  src/Version/autoload.php \
  --basedir src/Version \
  src


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{php_home}

cp -pr src/* %{buildroot}%{php_home}


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      pear.phpunit.de/Version >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md
%doc composer.json
%dir %{php_home}
     %{php_home}/Version*


%changelog
* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6
- generate autoloader
- fix PSR-0 layout

* Fri Apr  3 2015 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Sun Jan  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- fix scriptlet
- drop pear compatibility provides
- fix license usage

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- composer dependencies

* Sat Mar  8 2014 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- move from pear channel to github sources because of
  https://github.com/sebastianbergmann/phpunit/wiki/Release-Announcement-for-PHPUnit-4.0.0
- add %%check
- add missing dependency on git

* Thu Feb 13 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Apr  4 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- initial package
