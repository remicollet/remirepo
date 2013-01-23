%global github_owner   getsentry
%global github_name    raven-php
%global github_version 0.4.0
%global github_commit  80ff1fec353834de5d6bf57ca6834eddde14aba9

%global lib_name       Raven
%global php_min_ver    5.2.4

Name:          php-%{lib_name}
Version:       %{github_version}
Release:       2%{?dist}
Summary:       A PHP client for Sentry

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{version}-%{github_commit}.tar.gz

BuildArch:     noarch
# Test build requires
BuildRequires: php-common >= %{php_min_ver}
# composer.json lists PHPUnit version 3.7, but tests pass with 3.6+
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test build requires: phpci
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-sockets
BuildRequires: php-spl
BuildRequires: php-zlib

Requires:      php-common >= %{php_min_ver}
# phpci requires
Requires:      php-curl
Requires:      php-date
Requires:      php-hash
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-session
Requires:      php-sockets
Requires:      php-spl
Requires:      php-zlib

%description
%{summary} (http://getsentry.com).


%package tests
Summary:  Test suite for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tests
%{summary}.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Update autoloader require in bin and test bootstrap
sed "/require.*Autoloader/s:.*:require_once 'Raven/Autoloader.php';:" \
    -i bin/raven \
    -i test/bootstrap.php

# Update and move PHPUnit config
sed -e 's:\(\./\)\?test/:./:' \
    -e 's:./lib:%{_datadir}/php:' \
    -i phpunit.xml.dist
mv phpunit.xml.dist test/


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp lib/%{lib_name} %{buildroot}%{_datadir}/php/

mkdir -p -m 755 %{buildroot}%{_bindir}
install -pm 755 bin/raven %{buildroot}%{_bindir}/

mkdir -p -m 755 %{buildroot}%{_datadir}/tests/%{name}
cp -rp test/* %{buildroot}%{_datadir}/tests/%{name}/


%check
%{_bindir}/phpunit \
    -d include_path="./lib:./test:.:/usr/share/pear" \
    -c test/phpunit.xml.dist


%files
%doc LICENSE AUTHORS README.rst composer.json
%{_datadir}/php/%{lib_name}
%{_bindir}/raven

%files tests
%dir %{_datadir}/tests
     %{_datadir}/tests/%{name}


%changelog
* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-2
- Updated bin install from "install" to "install -pm 755"

* Mon Jan 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.4.0-1
- Updated to upstream version 0.4.0
- Fixed license
- Fixed build requires

* Fri Jan 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 0.3.1-1.20130117git60e91ac
- Initial package
