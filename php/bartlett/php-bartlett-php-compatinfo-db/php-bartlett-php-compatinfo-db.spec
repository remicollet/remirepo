# remirepo/fedora spec file for php-bartlett-php-compatinfo-db
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github
%global gh_commit    b65b06ba30abba8e85c6afc40c8c9ea7921dc434
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_date      20151031
%global gh_owner     llaville
%global gh_project   php-compatinfo-db
%global prever       alpha1
# Namespace
%global ns_vendor    Bartlett
%global ns_project   CompatInfoDb
# Composer
%global c_vendor     bartlett
%global c_project    php-compatinfo-db

%global with_tests   0%{!?_without_tests:1}

Name:           php-%{c_vendor}-%{c_project}
Version:        1.0.0
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Reference Database to be used with php-compatinfo library

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}%{?prever}-%{gh_short}.tar.gz

# Autoloader for RPM
Source1:        %{name}-autoload.php

# Autoload and sqlite database path
Patch0:         %{name}-1.0.0-rpm.patch

BuildArch:      noarch
# Needed to build the database from sources
BuildRequires:  php(language) >= 5.4.0
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
#        "ext-curl": "*",
#        "ext-intl": "*",
#        "ext-libxml": "*",
#        "ext-openssl": "*",
#        "ext-pcre": "*",
#        "ext-spl": "*",
#        "ext-json": "*",
#        "ext-pdo_sqlite": "*"
Requires:       php(language) >= 5.4.0
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
cp %{SOURCE1} src/%{ns_vendor}/%{ns_project}/autoload.php

# Cleanup patched files
find src -name \*rpm -delete -print


%build
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
* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.alpha1
- Initial package