# remirepo/fedora spec file for composer
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    00c26791faeb83da8476b54bcc20596cf754362e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_branch    1.0-dev
%global gh_date      20150720
%global gh_owner     composer
%global gh_project   composer
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}

Name:           composer
Version:        1.0.0
Release:        0.8.%{gh_date}git%{gh_short}%{?dist}
Summary:        Dependency Manager for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://getcomposer.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php
Source2:        %{name}-bootstrap.php

# Use our autoloader, resources path, fix for tests
Patch0:         %{name}-rpm.patch
# https://github.com/composer/composer/pull/4169
# skip online tests
Patch1:         %{name}-pr4169.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(justinrainbow/json-schema) >= 1.4.4
BuildRequires:  php-composer(composer/spdx-licenses)    >= 1.0
BuildRequires:  php-composer(seld/jsonlint)             >= 1.0
BuildRequires:  php-composer(symfony/console)           >= 2.5
BuildRequires:  php-composer(symfony/finder)            >= 2.2
BuildRequires:  php-composer(symfony/process)           >= 2.1
BuildRequires:  php-composer(symfony/class-loader)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-zip
%endif

# From composer.json, requires
#        "php": ">=5.3.2",
#        "justinrainbow/json-schema": "^1.4.4",
#        "composer/spdx-licenses": "~1.0",
#        "seld/jsonlint": "~1.0",
#        "symfony/console": "~2.5",
#        "symfony/finder": "~2.2",
#        "symfony/process": "~2.1",
#        "seld/phar-utils": "~1.0",
#        "seld/cli-prompt": "~1.0"
Requires:       php(language)                           >= 5.3.2
Requires:       php-cli
Requires:       php-composer(justinrainbow/json-schema) >= 1.4.4
Requires:       php-composer(justinrainbow/json-schema) <  2
Requires:       php-composer(composer/spdx-licenses)    >= 1.0
Requires:       php-composer(composer/spdx-licenses)    <  2
Requires:       php-composer(seld/jsonlint)             >= 1.0
Requires:       php-composer(seld/jsonlint)             <  2
Requires:       php-composer(seld/phar-utils)           >= 1.0
Requires:       php-composer(seld/phar-utils)           <  2
Requires:       php-composer(seld/cli-prompt)           >= 1.0
Requires:       php-composer(seld/cli-prompt)           <  2
Requires:       php-composer(symfony/console)           >= 2.5
Requires:       php-composer(symfony/console)           <  3
Requires:       php-composer(symfony/finder)            >= 2.2
Requires:       php-composer(symfony/finder)            <  3
Requires:       php-composer(symfony/process)           >= 2.1
Requires:       php-composer(symfony/process)           <  3
# From composer.json, suggest
#        "ext-zip": "Enabling the zip extension allows you to unzip archives, and allows gzip compression of all internet traffic",
#        "ext-openssl": "Enabling the openssl extension allows you to access https URLs for repositories and packages"
Requires:       php-zip
Requires:       php-openssl
# For our autoloader
Requires:       php-composer(symfony/class-loader)
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

Provides:       php-composer(composer/composer) = %{version}


%description
Composer helps you declare, manage and install dependencies of PHP projects,
ensuring you have the right stack everywhere.

Documentation: https://getcomposer.org/doc/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1
%patch1 -p1

cp -p %{SOURCE1} src/Composer/autoload.php
cp -p %{SOURCE2} tests/bootstrap.php
rm src/bootstrap.php

: fix reported version
DATE=%{gh_date}
DATE=${DATE:0:4}-${DATE:4:2}-${DATE:6:2}
sed -e '/VERSION/s/@package_version@/%{gh_commit}/' \
    -e '/BRANCH_ALIAS_VERSION/s/@package_branch_alias_version@/%{gh_branch}/' \
    -e "/RELEASE_DATE/s/@release_date@/$DATE/" \
    -i src/Composer/Composer.php


%build
# Nothing


%install
rm -rf       %{buildroot}

: Library
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr src/* %{buildroot}%{_datadir}/php

: Resources
mkdir -p     %{buildroot}%{_datadir}/%{name}
cp -pr res   %{buildroot}%{_datadir}/%{name}/res

: Command
install -Dpm 755 bin/%{name} %{buildroot}%{_bindir}/%{name}


%check
%if %{with_tests}
: Run test suite
export BUILDROOT=%{buildroot}
%{_bindir}/phpunit --include-path %{buildroot}%{_datadir}/php --verbose
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