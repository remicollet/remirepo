# remirepo/fedora spec file for php-bartlett-php-compatinfo-db
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# See https://github.com/llaville/php-compatinfo-db/releases
%global gh_commit    92937c4c1b794ae657f384ade75411f6343f86a7
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date      20151031
%global gh_owner     llaville
%global gh_project   php-compatinfo-db
#global prever       alpha1
# Namespace
%global ns_vendor    Bartlett
%global ns_project   CompatInfoDb
# Composer
%global c_vendor     bartlett
%global c_project    php-compatinfo-db

%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.7.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Reference Database to be used with php-compatinfo library

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

# Autoloader for RPM
Source1:        %{name}-1.2.0-autoload.php

# Autoload and sqlite database path
Patch0:         %{name}-1.2.0-rpm.patch
# CURL_SSLVERSION constants have been backported
Patch1:         %{name}-curltls.patch

BuildArch:      noarch
# Needed to build the database from sources
BuildRequires:  php(language) >= 5.4.0
BuildRequires:  php-composer(composer/semver) >= 1.0
BuildRequires:  php-curl
BuildRequires:  php-intl
BuildRequires:  php-libxml
BuildRequires:  php-openssl
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-json
BuildRequires:  php-pdo_sqlite
# For our patch / autoloader
BuildRequires:  php-composer(symfony/class-loader)
# From composer.json, "require-dev": {
#        "symfony/console": "~2.5",
#        "psr/log": "~1.0",
#        "monolog/monolog": "~1.10",
#        "bartlett/phpunit-loggertestlistener": "~1.5"
BuildRequires:  php-cli
BuildRequires:  php-composer(symfony/console) >= 2.5
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
%endif

# From composer.json, "require"
#        "php": ">=5.4.0",
#        "composer/semver": "~1.0",
#        "ext-curl": "*",
#        "ext-intl": "*",
#        "ext-libxml": "*",
#        "ext-openssl": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-json": "*",
#        "ext-pdo_sqlite": "*"
Requires:       php(language) >= 5.4.0
Requires:       php-composer(composer/semver) >= 1.0
Requires:       php-composer(composer/semver) <  2
Requires:       php-curl
Requires:       php-intl
Requires:       php-libxml
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
Requires:       php-json
Requires:       php-pdo_sqlite
# Required by autoloader
Requires:       php-composer(symfony/class-loader)

Provides:       php-composer(%{c_vendor}/%{c_project}) = %{version}
# Extracted from bartlett/php-compatinfo 4
Conflicts:      php-bartlett-PHP-CompatInfo < 5


%description
%{summary}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1 -b .rpm
%patch1 -p0 -b .old

cp %{SOURCE1} src/%{ns_vendor}/%{ns_project}/autoload.php

# Use package version
sed -e 's/@VERSION@/%{version}/' -i data/handleDB.php

# Cleanup patched files
find src -name \*rpm -delete -print


%build
: Ensure current version is known by reference
OPT=$(php -r '
  require "src/%{ns_vendor}/%{ns_project}/autoload.php";

  switch (PHP_MAJOR_VERSION . PHP_MINOR_VERSION) {
    case "54":
      $max = Bartlett\CompatInfoDb\ExtensionFactory::LATEST_PHP_5_4;
      break;
    case "55":
      $max = Bartlett\CompatInfoDb\ExtensionFactory::LATEST_PHP_5_5;
      break;
    case "56":
      $max = Bartlett\CompatInfoDb\ExtensionFactory::LATEST_PHP_5_6;
      break;
    case "70":
      $max = Bartlett\CompatInfoDb\ExtensionFactory::LATEST_PHP_7_0;
      break;
    default:
      exit(0);
  }
  if (version_compare(PHP_VERSION, $max, ">")) {
    fputs(STDERR, "Current: " . PHP_VERSION . " > Known: $max\n\n");
    echo "/LATEST_PHP_" . PHP_MAJOR_VERSION . "_" . PHP_MINOR_VERSION .
         "/s/" . PHP_MAJOR_VERSION . "\." .PHP_MINOR_VERSION . "\.[0-9]*/" . PHP_VERSION . "/";
  } else {
    fputs(STDERR, "Current: " . PHP_VERSION . " = Known: $max\n\n");
  }
')
if [ -n "$OPT" ]; then
  sed -e "$OPT" -i  src/Bartlett/CompatInfoDb/ExtensionFactory.php
fi
grep " LATEST" src/Bartlett/CompatInfoDb/ExtensionFactory.php

: Fix references database
%{_bindir}/php -d date.timezone=Europe/Paris data/handleDB.php db:release:php

: Generate the references database
%{_bindir}/php -d date.timezone=Europe/Paris data/handleDB.php db:init


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr src/%{ns_vendor} %{buildroot}%{_datadir}/php/%{ns_vendor}

install -D -p -m 644 data/compatinfo.sqlite      %{buildroot}%{_datadir}/%{name}/compatinfo.sqlite


%if %{with_tests}
%check
export BARTLETT_COMPATINFO_DB=%{buildroot}%{_datadir}/%{name}/compatinfo.sqlite

%{_bindir}/phpunit \
    --include-path %{buildroot}%{_datadir}/php \
    -d memory_limit=1G
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%dir %{_datadir}/php/%{ns_vendor}
     %{_datadir}/php/%{ns_vendor}/%{ns_project}
     %{_datadir}/%{name}


%changelog
* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0

* Sat Mar  5 2016 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- update to 1.6.0
- use package version as version in database instead of date

* Sat Feb  6 2016 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Sat Jan  9 2016 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Tue Dec 29 2015 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Thu Dec 10 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- fix reference to ensure current version is known
  as we usually build RC version in rawhide.

* Sat Dec  5 2015 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- add dependency on composer/semver

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha1
- Initial package
