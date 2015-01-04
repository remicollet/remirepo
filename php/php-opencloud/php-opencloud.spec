#
# RPM spec file for php-egulias-email-validator
#
# Copyright (c) 2013-2014 Gregor Tätzner <brummbq@fedoraproject.org>
#                         Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     rackspace
%global github_name      php-opencloud
%global github_version   1.12.1
%global github_commit    23105f00eb648c10cc360cbc04231018117b0302

%global composer_vendor  rackspace
%global composer_project php-opencloud

# "php" : ">=5.3.3"
%global php_min_ver      5.3.3
# "guzzle/http" : "~3.8"
%global guzzle_min_ver   3.8
%global guzzle_max_ver   4.0
# "psr/log": "~1.0"
%global psr_log_min_ver  1.0
%global psr_log_max_ver  2.0

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-opencloud
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP SDK for OpenStack/Rackspace APIs
Group:         Development/Libraries

License:       ASL 2.0
URL:           http://php-opencloud.com/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
BuildRequires: php-phpunit-PHPUnit
# composer.json
BuildRequires: php(language)         >= %{php_min_ver}
BuildRequires: php-composer(psr/log) >= %{psr_log_min_ver}
BuildRequires: php-composer(psr/log) <  %{psr_log_max_ver}
BuildRequires: php-guzzle-Guzzle     >= %{guzzle_min_ver}
BuildRequires: php-guzzle-Guzzle     <  %{guzzle_max_ver}
# phpcompatinfo (computed from version 1.12.1)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)         >= %{php_min_ver}
Requires:      php-composer(psr/log) >= %{psr_log_min_ver}
Requires:      php-composer(psr/log) <  %{psr_log_max_ver}
Requires:      php-guzzle-Guzzle     >= %{guzzle_min_ver}
Requires:      php-guzzle-Guzzle     <  %{guzzle_max_ver}
# phpcompatinfo (computed from version 1.12.1)
Requires:      php-date
Requires:      php-hash
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
The PHP SDK should work with most OpenStack-based cloud deployments, though
it specifically targets the Rackspace public cloud. In general, whenever a
Rackspace deployment is substantially different than a pure OpenStack one,
a separate Rackspace subclass is provided so that you can still use the SDK
with a pure OpenStack instance (for example, see the OpenStack class (for
OpenStack) and the Rackspace subclass).


%package doc
Summary: Documentation for PHP SDK for OpenStack/Rackspace APIs
Group:   Development/Libraries


%description doc
Documentation for PHP SDK for OpenStack/Rackspace APIs.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/OpenCloud %{buildroot}%{phpdir}/


%clean
rm -rf %{buildroot}


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

# Create PHPUnit config with no coverage-clover logging
sed -e '/coverage-clover/d' phpunit.xml.dist > phpunit.xml

%{__phpunit} --include-path %{buildroot}%{phpdir}:./tests
%else
: Tests skipped
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
%{phpdir}/OpenCloud


%files doc
%doc samples docs


%changelog
* Fri Jan 02 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.12.1-1
- Updated to 1.12.1 (BZ #1172637)
- Added php-composer(rackspace/php-opencloud) virtual provide

* Sat Nov 22 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.11.0-3
- Removed obsolete of php-cloudfiles

* Sun Nov 02 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.11.0-2
- No BuildRequires unless with tests

* Sun Nov 02 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.11.0-1
- Updated to 1.11.0 (BZ #1159522)
- Spec cleanup

* Thu Jul 31 2014 Remi Collet <rpms@famillecollet.com> - 1.6.0-5
- don't obsolete php-cloudfiles

* Thu Jan 30 2014 Remi Collet <rpms@famillecollet.com> - 1.6.0-4
- backport 1.6.0 for remi repo

* Thu Jan 30 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-4
- obsolete php-cloudfiles

* Sat Jan 25 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-3
- use commit revision in source url

* Fri Jan 03 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-2
- move lib to psr-0 compliant location
- drop autoloader

* Tue Dec 31 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-1
- initial packaging

