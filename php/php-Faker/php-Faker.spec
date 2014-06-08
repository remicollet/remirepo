#
# RPM spec file for php-Faker
#
# Copyright (c) 2012-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner   fzaninotto
%global github_name    Faker
%global github_version 1.4.0
%global github_commit  010c7efedd88bf31141a02719f51fb44c732d5a0

# "php": ">=5.3.3"
%global php_min_ver    5.3.3

# Build using "--without tests" to disable tests
%global with_tests     %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A PHP library that generates fake data

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests: composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 1.4.0)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-hash
BuildRequires: php-mbstring
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.4.0)
Requires:      php-curl
Requires:      php-date
Requires:      php-hash
Requires:      php-mbstring
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

Provides:      php-composer(fzaninotto/faker) = %{version}

%description
Faker is a PHP library that generates fake data for you. Whether you need
to bootstrap your database, create good-looking XML documents, fill-in your
persistence to stress test it, or anonymize data taken from a production
service, Faker is for you.

Faker is heavily inspired by Perl's Data::Faker
(http://search.cpan.org/~jasonk/Data-Faker/), and by Ruby's Faker
(http://faker.rubyforge.org/).

Optional:
* Doctrine ORM (php-doctrine-orm)


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -rp src/%{github_name} %{buildroot}%{_datadir}/php/


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

# Skip tests that require downloading content
sed 's/function testDownloadWithDefaults/function SKIP_testDownloadWithDefaults/' \
    -i test/Faker/Provider/ImageTest.php

%{_bindir}/phpunit --include-path="./src:./test" -d date.timezone="UTC"
%else
: Tests skipped
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE CHANGELOG *.md composer.json
%{_datadir}/php/%{github_name}


%changelog
* Sun Jun  8 2014 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- backport 1.3.0 for remi repo.

* Sun Jun 08 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.4.0-1
- Updated to 1.4.0 (BZ #1105815)
- Added php-composer(fzaninotto/faker) virtual provide
- Made Doctrine pkg optional instead of required
- Added option to build without tests

* Mon Dec 30 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-1
- backport 1.3.0 for remi repo.

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3.0-1
- Updated to 1.3.0 (BZ #1044436)
- Spec cleanup

* Wed Jun 12 2013 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- backport 1.2.0 for remi repo.

* Mon Jun 10 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2.0-1
- Updated to 1.2.0
- Added php-mbstring require
- Updates per new Fedora packaging guidelines for Git repos

* Wed Dec 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-2
- backport 1.1.0 for remi repo.

* Sun Dec  9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-2
- Added php-pear(pear.doctrine-project.org/DoctrineCommon) require

* Sun Dec  9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
