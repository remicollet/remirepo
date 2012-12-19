%global libname     Faker
%global php_min_ver 5.3.3

Name:          php-%{libname}
Version:       1.1.0
Release:       2%{?dist}
Summary:       A PHP library that generates fake data

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/fzaninotto/%{libname}
Source0:       %{url}/archive/v%{version}.tar.gz

BuildArch:     noarch
# Test build requires
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test build requires: phpci
Requires:      php-date
Requires:      php-hash
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

Requires:      php-common >= %{php_min_ver}
Requires:      php-pear(pear.doctrine-project.org/DoctrineCommon)
# phpci requires
Requires:      php-date
Requires:      php-hash
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

%description
Faker is a PHP library that generates fake data for you. Whether you need
to bootstrap your database, create good-looking XML documents, fill-in your
persistence to stress test it, or anonymize data taken from a production
service, Faker is for you.

Faker is heavily inspired by Perl's Data::Faker
(http://search.cpan.org/~jasonk/Data-Faker/), and by Ruby's Faker
(http://faker.rubyforge.org/).


%prep
%setup -q -n %{libname}-%{version}

# Remove executable bit from all PHP files
# https://github.com/fzaninotto/Faker/pull/84
find . -name '*.php' -executable | xargs chmod a-x


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp src/%{libname} %{buildroot}%{_datadir}/php/


%check
%{_bindir}/phpunit -d date.timezone="UTC" .


%files
%doc LICENSE CHANGELOG readme.md composer.json
%{_datadir}/php/%{libname}


%changelog
* Sun Dec  9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-2
- Added php-pear(pear.doctrine-project.org/DoctrineCommon) require

* Sun Dec  9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
