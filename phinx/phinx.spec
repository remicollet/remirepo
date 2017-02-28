# remirepo/fedora spec file for phinx
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    53cc5123c1cba71b26d4e5ab83fa0dd404075d19
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     robmorgan
#global gh_date      20150820
%global gh_project   phinx
%global psr0         Phinx
%if 0%{?rhel} == 5
# 3 failures on EL-5 related to sqlite
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           %{gh_project}
Version:        0.7.2
Release:        1%{?gh_date?%{gh_date}git%{gh_short}}%{?dist}
Summary:        Manage the database migrations for your PHP app

Group:          Development/Libraries
License:        MIT
URL:            https://phinx.org
Source0:        %{name}-%{version}-%{?gh_short}.tgz
Source1:        %{name}-autoload.php
Source2:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(symfony/console) >= 2.8
BuildRequires:  php-composer(symfony/config)  >= 2.8
BuildRequires:  php-composer(symfony/yaml)    >= 2.8
BuildRequires:  php-pdo
BuildRequires:  php-date
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-spl
# For tests, from composer.json "require-dev": {
#        "phpunit/phpunit": "^4.8.26|^5.0"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8.26
%endif
# For autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#        "php": ">=5.4",
#        "symfony/console": "~2.8|~3.0",
#        "symfony/config": "~2.8|~3.0",
#        "symfony/yaml": "~2.8|~3.0"
Requires:       php(language) >= 5.4
Requires:       php-composer(symfony/console) >= 2.8
Requires:       php-composer(symfony/config)  >= 2.8
Requires:       php-composer(symfony/yaml)    >= 2.8
# From phpcompatinfo report for 0.6.4
Requires:       php-pdo
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# For autoloader
Requires:       php-composer(fedora/autoloader)

# Composer
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Phinx makes it ridiculously easy to manage the database migrations
for your PHP app. In less than 5 minutes you can install Phinx and
create your first database migration.

Phinx is just about migrations without all the bloat of a database
ORM system or framework.

Documentation: http://docs.phinx.org


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/%{psr0}/autoload.php

sed -e 's:../data/Phinx:data:' -i src/Phinx/Console/Command/Init.php

: Create the launcher
cat << 'EOF' | tee phinx
#!/usr/bin/env php
<?php
require '/usr/share/php/%{psr0}/autoload.php';
$app = new Phinx\Console\PhinxApplication();
$app->run();
EOF


%build
: Nothing to build


%install
rm -rf     %{buildroot}

: Library
mkdir -p           %{buildroot}%{_datadir}/php
cp -pr src/%{psr0} %{buildroot}%{_datadir}/php/%{psr0}

: Default config file
install -Dpm 644 phinx.yml %{buildroot}%{_datadir}/php/%{psr0}/data/phinx.yml

: The command
install -Dpm 755 phinx %{buildroot}%{_bindir}/phinx


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require '%{buildroot}%{_datadir}/php/%{psr0}/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('Test\\Phinx\\', dirname(__DIR__).'/tests/Phinx');
EOF

sed -e '/_ENABLED/s/true/false/;/SQLITE_ENABLED/s/false/true/' \
    phpunit.xml.dist >phpunit.xml

: Run upstream test suite
ret=0
for cmd in php56 php70 php71 php; do
   if which $cmd; then
      $cmd %{_bindir}/phpunit --verbose || ret=1
   fi
done
exit $ret
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%doc *.md
%doc app/web.php
%{_datadir}/php/%{psr0}
%{_bindir}/phinx


%changelog
* Tue Feb 28 2017 Remi Collet <remi@remirepo.net> - 0.7.2-1
- update to 0.7.2

* Sun Feb 19 2017 Remi Collet <remi@remirepo.net> - 0.7.1-1
- update to 0.7.1

* Fri Feb 10 2017 Remi Collet <remi@remirepo.net> - 0.7.0-1
- update to 0.7.0

* Mon Jan 23 2017 Remi Collet <remi@remirepo.net> - 0.6.6-1
- update to 0.6.6
- use a git snashop to retrieve test suite

* Thu Oct 27 2016 Remi Collet <remi@fedoraproject.org> - 0.6.5-1
- update to 0.6.5
- switch from symfony/class-loader to fedora/autoloader

* Tue Sep 27 2016 Remi Collet <remi@fedoraproject.org> - 0.6.4-1
- initial package

