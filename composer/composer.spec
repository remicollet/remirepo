# remirepo/fedora spec file for composer
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    94c2a21fe51016758212fa0aebd8add36757f354
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_branch    1.0-dev
%global gh_owner     composer
%global gh_project   composer
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%global api_version  1.1.0
%global prever       RC

Name:           composer
Version:        1.1.0
Release:        0.1.%{prever}%{?dist}
Summary:        Dependency Manager for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://getcomposer.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php
Source2:        %{name}-bootstrap.php

# Use our autoloader, resources path, fix for tests
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-cli
%if %{with_tests}
BuildRequires:  php-composer(justinrainbow/json-schema) >= 1.6
BuildRequires:  php-composer(composer/spdx-licenses)    >= 1.0
BuildRequires:  php-composer(composer/ca-bundle)        >= 1.0
BuildRequires:  php-composer(composer/semver)           >= 1.0
BuildRequires:  php-composer(seld/jsonlint)             >= 1.4
BuildRequires:  php-composer(seld/phar-utils)           >= 1.0
BuildRequires:  php-composer(seld/cli-prompt)           >= 1.0
BuildRequires:  php-composer(psr/log)                   >= 1.0
BuildRequires:  php-composer(symfony/console)           >= 2.5
BuildRequires:  php-composer(symfony/finder)            >= 2.2
BuildRequires:  php-composer(symfony/filesystem)        >= 2.5
BuildRequires:  php-composer(symfony/process)           >= 2.1
BuildRequires:  php-zip
# From composer.json, "require-dev": {
#        "phpunit/phpunit": "^4.5 || ^5.0.5",
#        "phpunit/phpunit-mock-objects": "2.3.0 || ^3.0"
BuildRequires:  php-composer(phpunit/phpunit)           >= 4.5
# For autoloader
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  php-seld-phar-utils >= 1.0.1
BuildRequires:  php-seld-cli-prompt >= 1.0.0-3
BuildRequires:  php-PsrLog          >= 1.0.0-8
%endif

# From composer.json, "require": {
#        "php": "^5.3.2 || ^7.0",
#        "justinrainbow/json-schema": "^1.6",
#        "composer/ca-bundle": "^1.0",
#        "composer/semver": "^1.0",
#        "composer/spdx-licenses": "^1.0",
#        "seld/jsonlint": "~1.4",
#        "symfony/console": "^2.5 || ^3.0",
#        "symfony/finder": "^2.2 || ^3.0",
#        "symfony/process": "^2.1 || ^3.0",
#        "symfony/filesystem": "^2.5 || ^3.0",
#        "seld/phar-utils": "^1.0",
#        "seld/cli-prompt": "^1.0",
#        "psr/log": "^1.0"
Requires:       php(language)                           >= 5.3.2
Requires:       php-cli
Requires:       php-composer(justinrainbow/json-schema) >= 1.6
Requires:       php-composer(justinrainbow/json-schema) <  2
Requires:       php-composer(composer/spdx-licenses)    >= 1.0
Requires:       php-composer(composer/spdx-licenses)    <  2
Requires:       php-composer(composer/ca-bundle)        >= 1.0
Requires:       php-composer(composer/ca-bundle)        <  2
Requires:       php-composer(composer/semver)           >= 1.0
Requires:       php-composer(composer/semver)           <  2
Requires:       php-composer(seld/jsonlint)             >= 1.4
Requires:       php-composer(seld/jsonlint)             <  2
Requires:       php-composer(seld/phar-utils)           >= 1.0
Requires:       php-composer(seld/phar-utils)           <  2
Requires:       php-composer(seld/cli-prompt)           >= 1.0
Requires:       php-composer(seld/cli-prompt)           <  2
Requires:       php-composer(psr/log)                   >= 1.0
Requires:       php-composer(psr/log)                   <  2
Requires:       php-composer(symfony/console)           >= 2.5
Requires:       php-composer(symfony/console)           <  4
Requires:       php-composer(symfony/finder)            >= 2.2
Requires:       php-composer(symfony/finder)            <  4
Requires:       php-composer(symfony/process)           >= 2.1
Requires:       php-composer(symfony/process)           <  4
Requires:       php-composer(symfony/filesystem)        >= 2.5
Requires:       php-composer(symfony/filesystem)        <  4
# From composer.json, suggest
#        "ext-zip": "Enabling the zip extension allows you to unzip archives, and allows gzip compression of all internet traffic",
#        "ext-openssl": "Enabling the openssl extension allows you to access https URLs for repositories and packages"
Requires:       php-zip
Requires:       php-openssl
# For our autoloader
Requires:       php-composer(symfony/class-loader)
Requires:       php-seld-phar-utils >= 1.0.1
Requires:       php-seld-cli-prompt >= 1.0.0-3
Requires:       php-PsrLog          >= 1.0.0-8
# From phpcompatinfo
Requires:       php-curl
Requires:       php-date
Requires:       php-dom
Requires:       php-filter
Requires:       php-hash
Requires:       php-iconv
Requires:       php-intl
Requires:       php-json
Requires:       php-libxml
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-phar
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-xsl
Requires:       php-zlib

# Composer library
Provides:       php-composer(composer/composer) = %{version}
# Special internal for Plugin API
Provides:       php-composer(composer-plugin-api) = %{api_version}


%description
Composer helps you declare, manage and install dependencies of PHP projects,
ensuring you have the right stack everywhere.

Documentation: https://getcomposer.org/doc/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm
find . -name \*.rpm -exec rm {} \; -print

if grep -r '\.\./res'; then
	: Patch need to fixed
	exit 1
fi

cp -p %{SOURCE1} src/Composer/autoload.php
cp -p %{SOURCE2} tests/bootstrap.php
rm src/bootstrap.php

: fix reported version
%if 0%{?gh_date}
DATE=%{gh_date}
DATE=${DATE:0:4}-${DATE:4:2}-${DATE:6:2}
sed -e '/VERSION/s/@package_version@/%{gh_commit}/' \
    -e '/BRANCH_ALIAS_VERSION/s/@package_branch_alias_version@/%{gh_branch}/' \
    -e "/RELEASE_DATE/s/@release_date@/$DATE/" \
    -i src/Composer/Composer.php
%else
sed -e '/BRANCH_ALIAS_VERSION/s/@package_branch_alias_version@//' \
    -i src/Composer/Composer.php
%endif

: check Plugin API version
php -r '
namespace Composer\Plugin;
include "src/Composer/Plugin/PluginInterface.php";
if (version_compare(PluginInterface::PLUGIN_API_VERSION, "%{api_version}")) {
  printf("Plugin API version is %s, expected %s\n", PluginInterface::PLUGIN_API_VERSION, "%{api_version}");
  exit(1);
}'


%build
# Nothing


%install
rm -rf       %{buildroot}

: Library
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php

: Resources
mkdir -p       %{buildroot}%{_datadir}/%{name}
cp -pr res     %{buildroot}%{_datadir}/%{name}/res
cp -p  LICENSE %{buildroot}%{_datadir}/%{name}/LICENSE

ln -sf %{_datadir}/%{name}/LICENSE LICENSE

: Command
install -Dpm 755 bin/%{name} %{buildroot}%{_bindir}/%{name}


%check
%if %{with_tests}
%if 0%{?rhel} == 5
rm tests/Composer/Test/Downloader/XzDownloaderTest.php
%endif
sed -e 's/testDispatcherCanConvertScriptEventToCommandEventForListener/SKIP1/' \
    -i tests/Composer/Test/EventDispatcher/EventDispatcherTest.php

: Ensure not used
rm -rf res

: Run test suite
export BUILDROOT=%{buildroot}
%{_bindir}/phpunit --include-path %{buildroot}%{_datadir}/php --verbose

if which php70; then
   php70 %{_bindir}/phpunit --include-path %{buildroot}%{_datadir}/php --verbose
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md doc
%doc composer.json
%{_bindir}/%{name}
%{_datadir}/php/Composer
%{_datadir}/%{name}


%changelog
* Sat Apr 30 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.1.RC
- update to 1.1.0-RC
- add dependency on composer/ca-bundle
- add dependency on psr/log
- bump composer-plugin-api to 1.1.0
- drop dependency on ca-certificates

* Sat Apr 30 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3

* Thu Apr 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Tue Apr 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- update to 1.0.1
- add dependency on ca-certificates
- fix patch for RPM path

* Tue Apr  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Tue Mar 29 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.22.beta2
- update to 1.0.0beta2

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.21.beta1
- update to 1.0.0beta1

* Tue Feb 23 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.20.201602git4c0e163
- new snapshot

* Sat Feb 13 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.20.20160213git7420265
- new snapshot

* Fri Feb 12 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.20.20160212git25e089e
- new snapshot
- don't relying on result order which may vary
  open https://github.com/composer/composer/pull/4912
- restore compatiblity with symfony < 2.8
  open https://github.com/composer/composer/pull/4913

* Wed Jan 27 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.19.20160127gitcd21505
- new snapshot

* Sun Jan 10 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.19.20160109gitbda2c0f
- new snapshot
- raise dependency on justinrainbow/json-schema ^1.6

* Fri Jan  8 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.18.20160106git64b0d72
- add patch for json-schema 1.6, FTBFS detected by Koschei
  open https://github.com/composer/composer/pull/4756

* Thu Jan  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.17.20160106git64b0d72
- new snapshot
- cleanup autoloader

* Mon Jan  4 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.16.20151228git72cd6af
- new snapshot

* Tue Dec 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.16.20151215gitf25446e
- new snapshot
- raise dependency on seld/jsonlint ^1.4

* Sat Nov 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.15.alpha1
- update to 1.0.0alpha11
- run test suite with both PHP 5 and 7 when available

* Mon Nov  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.14.20151030git5a5088e
- new snapshot
- allow symfony 3

* Tue Oct 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.13.20151027gita9f7480
- new snapshot

* Wed Oct 14 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.13.20151013gita54f84f
- new snapshot
- use autoloader from all dependencies

* Sun Oct 11 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.12.20151007git7a9eb02
- new snapshot
- provide php-composer(composer-plugin-api)

* Tue Oct  6 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.12.20151004gitfcce52b
- don't check version in diagnose command

* Sun Oct  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.11.20151004gitfcce52b
- new snapshot
- add dependency on composer/semver

* Mon Sep 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.10.20150920git9f2e562
- new snapshot
- add dependency on symfony/filesystem

* Tue Sep  8 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.9.20150907git9f6fdfd
- new snapshot

* Sun Aug 23 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.9.20150820gitf1aa655
- new snapshot
- add LICENSE in application data, as used by the code

* Fri Aug  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.8.20150804gitc83650f
- new snapshot

* Tue Jul 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.8.20150720git00c2679
- new snapshot
- add dependency on composer/spdx-licenses

* Thu Jul 16 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.7.20150714git92faf1c
- new snapshot
- raise dependency on justinrainbow/json-schema 1.4.4

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.6.20150626git943107c
- new snapshot
- review autoloader

* Sun Jun 21 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150620gitd0ff016
- new snapshot
- add missing BR on php-zip
- open https://github.com/composer/composer/pull/4169 for online test

* Mon Jun 15 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150614git8e9659b
- new snapshot

* Sun Jun  7 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150605git9fb2d4f
- new snapshot

* Tue Jun  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150531git0ec86be
- new snapshot

* Tue May 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.5.20150525git69210d5
- new snapshot
- ensure /usr/share/php is in include_path (for SCL)

* Wed May 13 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150511gitbc45d91
- new snapshot

* Mon May  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.4.20150503git42a9561
- new snapshot
- add dependencies on seld/phar-utils and seld/cli-prompt

* Mon Apr 27 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150426git1cb427f
- new snapshot

* Fri Apr 17 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150415git921b3a0
- new snapshot
- raise dependency on justinrainbow/json-schema ~1.4
- keep upstream shebang with /usr/bin/env (for SCL)

* Thu Apr  9 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150408git4d134ce
- new snapshot
- lower dependency on justinrainbow/json-schema ~1.3

* Tue Mar 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.3.20150324gitc5cd184
- new snapshot
- raise dependency on justinrainbow/json-schema ~1.4

* Thu Mar 19 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150316git829199c
- new snapshot

* Wed Mar  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150302giteadc167
- new snapshot

* Sat Feb 28 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.20150227git45b1f35
- new snapshot

* Thu Feb 26 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.20150225gite5985a9
- Initial package
