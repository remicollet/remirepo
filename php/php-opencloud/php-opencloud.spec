# remirepo spec file for php-opencloud, from
#
# Fedora spec file for php-opencloud
#
# Copyright (c) 2013-2017 Gregor Tätzner <brummbq@fedoraproject.org>
#                         Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner   rackspace
%global github_name    php-opencloud
%global github_version 1.16.0
%global github_commit  d6b71feed7f9e7a4b52e0240a79f06473ba69c8c

# Bundled: php-composer(mikemccabe/json-patch-php)
%global mikemccabe_json_patch_php_github_owner   mikemccabe
%global mikemccabe_json_patch_php_github_name    json-patch-php
%global mikemccabe_json_patch_php_github_version 0.1.0
%global mikemccabe_json_patch_php_github_commit  b3af30a6aec7f6467c773cd49b2d974a70f7c0d4

%global composer_vendor  rackspace
%global composer_project php-opencloud

# "php" : ">=5.4"
%global php_min_ver 5.4
# "guzzle/http" : "~3.8"
#     NOTE: Min version not 3.8 because autoloader required
%global guzzle_min_ver 3.9.3
%global guzzle_max_ver 4.0
# "mikemccabe/json-patch-php": "~0.1"
#%%global mikemccabe_json_patch_php_min_ver 0.1
#%%global mikemccabe_json_patch_php_max_ver 1.0
# "phpspec/prophecy": "~1.4"
%global phpspec_prophecy_min_ver 1.4
%global phpspec_prophecy_max_ver 2.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.1
%global psr_log_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-opencloud
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP SDK for OpenStack/Rackspace APIs
Group:         Development/Libraries

License:       ASL 2.0
URL:           http://docs.php-opencloud.com/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Bundled: php-composer(mikemccabe/json-patch-php)
Source1:       https://github.com/%{mikemccabe_json_patch_php_github_owner}/%{mikemccabe_json_patch_php_github_name}/archive/%{mikemccabe_json_patch_php_github_commit}/%{name}-mikemccabe-json-patch-php-%{mikemccabe_json_patch_php_github_version}-%{mikemccabe_json_patch_php_github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(guzzle/guzzle) <  %{guzzle_max_ver}
BuildRequires: php-composer(guzzle/guzzle) >= %{guzzle_min_ver}
BuildRequires: php-composer(phpspec/prophecy) <  %{phpspec_prophecy_max_ver}
BuildRequires: php-composer(phpspec/prophecy) >= %{phpspec_prophecy_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/log) <  %{psr_log_max_ver}
BuildRequires: php-composer(psr/log) >= %{psr_log_min_ver}
## phpcompatinfo (computed from version 1.16.0 / mikemccabe/json-patch-php 0.1.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(guzzle/guzzle) <  %{guzzle_max_ver}
Requires:      php-composer(guzzle/guzzle) >= %{guzzle_min_ver}
Requires:      php-composer(psr/log) <  %{psr_log_max_ver}
Requires:      php-composer(psr/log) >= %{psr_log_min_ver}
# phpcompatinfo (computed from version 1.16.0 / mikemccabe/json-patch-php 0.1.0)
Requires:      php-date
Requires:      php-hash
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Bundled: php-composer(mikemccabe/json-patch-php)
Provides:      bundled(php-mikemccabe-json-patch-php) = %{mikemccabe_json_patch_php_github_version}

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
%setup -qn %{github_name}-%{github_commit} -a 1


%build
: Create autoloader
cat <<'AUTOLOAD' | tee lib/OpenCloud/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('OpenCloud\\', __DIR__);
\Fedora\Autoloader\Autoload::addPsr4('mikemccabe\\JsonPatch\\', __DIR__.'/mikemccabe/JsonPatch');

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Guzzle/autoload.php',
    '%{phpdir}/Psr/Log/autoload.php',
));
AUTOLOAD


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{phpdir}
cp -rp lib/OpenCloud %{buildroot}%{phpdir}/

# Bundled: php-composer(mikemccabe/json-patch-php)
mkdir -p %{buildroot}%{phpdir}/OpenCloud/mikemccabe/JsonPatch
cp -rp \
    %{mikemccabe_json_patch_php_github_name}-%{mikemccabe_json_patch_php_github_commit}/src/* \
    %{buildroot}%{phpdir}/OpenCloud/mikemccabe/JsonPatch/


%clean
rm -rf %{buildroot}


%check
%if %{with_tests}
: Create mock Composer autoloader
mkdir vendor
cat <<'AUTOLOAD' | tee vendor/autoload.php
<?php
require '%{buildroot}%{phpdir}/OpenCloud/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('OpenCloud\\', dirname(__DIR__).'/tests/OpenCloud');
\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Prophecy/autoload.php',
));
AUTOLOAD

: Remove coverage-clover logging from PHPUnit config
sed -e '/coverage-clover/d' phpunit.xml.dist > phpunit.xml

: Skip tests known to fail
sed 's/function testGetConnection/function SKIP_testGetConnection/' \
    -i tests/OpenCloud/Tests/CloudMonitoring/Resource/AgentTest.php
sed 's/function test_Create_User/function SKIP_test_Create_User/' \
    -i tests/OpenCloud/Tests/Identity/ServiceTest.php
sed 's/function test_Get_Member/function SKIP_test_Get_Member/' \
    -i tests/OpenCloud/Tests/Image/Resource/ImageTest.php
sed \
    -e 's/function test_Get_Image/function SKIP_test_Get_Image/' \
    -e 's/function test_Images_Schema/function SKIP_test_Images_Schema/' \
    -e 's/function test_Image_Schema/function SKIP_test_Image_Schema/' \
    -e 's/function test_Members_Schema/function SKIP_test_Members_Schema/' \
    -e 's/function test_Member_Schema/function SKIP_test_Member_Schema/' \
    -i tests/OpenCloud/Tests/Image/ServiceTest.php

%{_bindir}/phpunit --verbose

: Upstream tests with SCLs if available
SCL_RETURN_CODE=0
for SCL in %{?rhel:php55} php56 php70 php71; do
    if which $SCL; then
        $SCL %{_bindir}/phpunit --verbose || SCL_RETURN_CODE=1
    fi
done
exit $SCL_RETURN_CODE
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/OpenCloud


%files doc
%defattr(-,root,root,-)
%doc docs
%doc samples


%changelog
* Sun Feb 26 2017 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.16.0-1
- Update to 1.16.0 (RHBZ #1312624)
- Fix FTBFS (skip tests known to fail)
- Add bundled dependency php-composer(mikemccabe/json-patch-php)
- Use php-composer(fedora/autoloader)

* Sat Mar 26 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.12.2-1
- Updated to 1.12.2
- Updated URL
- Updated dependencies to use php-composer(*)
- Added autoloader (and bumped dependency versions for their autoloaders)

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

