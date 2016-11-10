# remirepo spec file for php-simplesamlphp-saml2_1, from:
#
# Fedora spec file for php-simplesamlphp-saml2_1
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     simplesamlphp
%global github_name      saml2
%global github_version   1.10.2
%global github_commit    fbc457e774a1cd57945ca2684a2198a0984497c1

%global composer_vendor  simplesamlphp
%global composer_project saml2

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "mockery/mockery": "~0.9"
%global mockery_min_ver 0.9
%global mockery_max_ver 1.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.1
%global psr_log_max_ver 2.0
# "robrichards/xmlseclibs": "^1.3"
%global robrichards_xmlseclibs_min_ver 1.3
%global robrichards_xmlseclibs_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}_1
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       SAML2 PHP library from SimpleSAMLphp (version 1)

Group:         Development/Libraries
License:       LGPLv2
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                        >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/log)                >= %{psr_log_min_ver}
BuildRequires: php-composer(robrichards/xmlseclibs) <  %{robrichards_xmlseclibs_max_ver}
BuildRequires: php-composer(robrichards/xmlseclibs) >= %{robrichards_xmlseclibs_min_ver}
BuildRequires: php-dom
BuildRequires: php-openssl
BuildRequires: php-composer(mockery/mockery)        >= %{mockery_min_ver}
## phpcompatinfo (computed from version 1.10.2)
BuildRequires: php-date
BuildRequires: php-libxml
BuildRequires: php-mcrypt
BuildRequires: php-pcre
BuildRequires: php-soap
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
%endif
BuildRequires: php-fedora-autoloader-devel

# composer.json
Requires:      php(language)                        >= %{php_min_ver}
Requires:      php-composer(psr/log)                <  %{psr_log_max_ver}
Requires:      php-composer(psr/log)                >= %{psr_log_min_ver}
Requires:      php-composer(robrichards/xmlseclibs) <  %{robrichards_xmlseclibs_max_ver}
Requires:      php-composer(robrichards/xmlseclibs) >= %{robrichards_xmlseclibs_min_ver}
Requires:      php-dom
Requires:      php-openssl
# phpcompatinfo (computed from version 1.10.2)
Requires:      php-date
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-soap
Requires:      php-spl
Requires:      php-zlib
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
A PHP library for SAML2 related functionality. Extracted from SimpleSAMLphp [1],
used by OpenConext [2]. This library started as a collaboration between
UNINETT [3] and SURFnet [4] but everyone is invited to contribute.

Autoloader: %{phpdir}/SAML2_1/autoload.php

[1] https://www.simplesamlphp.org/
[2] https://www.openconext.org/
[3] https://www.uninett.no/
[4] https://www.surfnet.nl/


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
%{_bindir}/phpab --template fedora --output src/SAML2/autoload.php src/SAML2
cat <<'AUTOLOAD' >> src/SAML2/autoload.php

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Psr/Log/autoload.php',
    '%{phpdir}/robrichards-xmlseclibs/autoload.php',
));
AUTOLOAD


%install
rm -rf   %{buildroot}
mkdir -p %{buildroot}%{phpdir}/SAML2_1
cp -rp src/SAML2/* %{buildroot}%{phpdir}/SAML2_1/


%check
%if %{with_tests}
: Create pseudo Composer autoloader
mkdir vendor
%{_bindir}/phpab --template fedora --output vendor/autoload.php tests
cat <<'AUTOLOAD' | tee -a vendor/autoload.php
require_once '%{buildroot}%{phpdir}/SAML2_1/autoload.php';
require_once '%{phpdir}/Mockery/autoload.php';
AUTOLOAD

: Run tests
ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit --configuration=tools/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --configuration=tools/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --configuration=tools/phpunit --verbose
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/SAML2_1


%changelog
* Wed Nov 09 2016 Shawn Iwinski <shawn@iwin.ski> - 1.10.2-1
- Update to 1.10.2 (RHBZ #1379182)
- Use php-composer(fedora/autoloader)

* Wed Nov  9 2016 Remi Collet <remi@remirepo.net> - 1.10.2-1
- update to 1.10.2

* Wed Nov  9 2016 Remi Collet <remi@remirepo.net> - 1.10.1-1
- update to 1.10.1

* Sun Sep 25 2016 Shawn Iwinski <shawn@iwin.ski> - 1.10-1
- Update to 1.10 (RHBZ #1376300)

* Sat Jul 30 2016 Remi Collet <remi@remirepo.net> - 1.9.1
- backport for remirepo

* Sun Jul 10 2016 Shawn Iwinski <shawn@iwin.ski> - 1.9-1
- Initial package
