%global github_owner    getsentry
%global github_name     raven-php
%global github_version  0.8.0
%global github_commit   dac93338d1fe17d665dfdea5f529c89b3a0df7df
# Additional commits after 0.8.0 tag
%global github_release  20131209git%(c=%{github_commit}; echo ${c:0:7})

%global lib_name        Raven

# "php": ">=5.2.4"
%global php_min_ver     5.2.4
# "phpunit/phpunit": "3.7.*"
%global phpunit_min_ver 3.7.0
%global phpunit_max_ver 3.8.0

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       2.%{github_release}%{?dist}
Summary:       A PHP client for Sentry

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit) >= %{phpunit_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit) <  %{phpunit_max_ver}
# For tests: phpcompatinfo (computed from 0.8.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-sockets
BuildRequires: php-spl
BuildRequires: php-zlib

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from 0.8.0)
Requires:      php-curl
Requires:      php-date
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-session
Requires:      php-sockets
Requires:      php-spl
Requires:      php-zlib

%description
%{summary} (http://getsentry.com).


%prep
%setup -q -n %{github_name}-%{github_commit}

# Update autoloader require in bin and test bootstrap
sed "/require.*Autoloader/s:.*:require_once 'Raven/Autoloader.php';:" \
    -i bin/raven \
    -i test/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -rp lib/* %{buildroot}%{_datadir}/php/

mkdir -p %{buildroot}%{_bindir}
install -pm 755 bin/raven %{buildroot}%{_bindir}/


%check
# Create PHPUnit config w/ colors turned off
cat phpunit.xml.dist \
    | sed 's/colors="true"/colors="false"/' \
    > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./test


%files
%defattr(-,root,root,-)
%doc LICENSE AUTHORS *.rst composer.json
%{_datadir}/php/%{lib_name}
%{_bindir}/raven


%changelog
* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> 0.8.0-2.20131209gitdac9333
- backport 0.8.0 for remi repo.

* Mon Dec 30 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.8.0-2.20131209gitdac9333
- Updated to latest snapshot

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.8.0-1
- Updated to 0.8.0 (BZ #1037543)
- Spec cleanup

* Thu Oct  3 2013 Remi Collet <remi@fedoraproject.org> 0.7.1-1
- backport 0.7.1 for remi repo.

* Wed Oct 02 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.7.1-1
- Updated to 0.7.1

* Mon Jul  8 2013 Remi Collet <remi@fedoraproject.org> 0.6.1-1
- backport 0.6.1 for remi repo.

* Fri Jul 05 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.6.1-1
- Updated to 0.6.1 (BZ #981406)

* Fri Jun 07 2013 Remi Collet <remi@fedoraproject.org> 0.6.0-1
- backport 0.6.0 for remi repo.

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.6.0-1
- Updated to 0.6.0
- Removed tests sub-package

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> 0.5.1-1
- backport 0.5.1 for remi repo.

* Sun Feb 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.5.1-1
- Updated to upstream version 0.5.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 0.4.0-2
- backport 0.4.0 for remi repo.

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-2
- Updated bin install from "install" to "install -pm 755"

* Mon Jan 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-1
- Updated to upstream version 0.4.0
- Fixed license
- Fixed build requires

* Fri Jan 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.1-1.20130117git60e91ac
- Initial package
