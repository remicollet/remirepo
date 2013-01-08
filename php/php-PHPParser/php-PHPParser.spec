%global lib_name    PHPParser
%global github_name PHP-Parser

%global php_min_ver 5.3.0

Name:          php-%{lib_name}
Version:       0.9.3
Release:       2%{?dist}
Summary:       A PHP parser written in PHP

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/nikic/%{github_name}
Source0:       %{url}/archive/v%{version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Test build requires
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test build requires: phpci
BuildRequires: php-ctype
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-tokenizer
BuildRequires: php-filter
BuildRequires: php-xmlreader
BuildRequires: php-xmlwriter

Requires:      php(language) >= %{php_min_ver}
# phpci requires
Requires:      php-ctype
Requires:      php-pcre
Requires:      php-spl
Requires:      php-tokenizer
Requires:      php-filter
Requires:      php-xmlreader
Requires:      php-xmlwriter

%description
A PHP parser written in PHP to simplify static analysis and code manipulation.


%package test
Summary:  Test suite for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description test
%{summary}.


%prep
%setup -q -n %{github_name}-%{version}

# Update and move bootstrap
sed "/require/s:/PHPParser::" \
    -i lib/bootstrap.php
mv lib/bootstrap.php lib/%{lib_name}/

# Update and move PHPUnit config
sed -e 's:./lib/bootstrap.php:%{_datadir}/php/%{lib_name}/bootstrap.php:' \
    -e 's:./lib/%{lib_name}/:%{_datadir}/php/%{lib_name}/:' \
    -e 's:./test/:./:' \
    -i phpunit.xml.dist
mv phpunit.xml.dist test/

# Remove executable bit from composer.json
# https://github.com/nikic/PHP-Parser/pull/46
chmod a-x composer.json


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp lib/%{lib_name} %{buildroot}%{_datadir}/php/

mkdir -p -m 755 %{buildroot}%{_datadir}/tests/%{name}
cp -rp test/* %{buildroot}%{_datadir}/tests/%{name}/


%check
%{_bindir}/phpunit \
    --bootstrap=lib/%{lib_name}/bootstrap.php \
    -c test/phpunit.xml.dist \
    -d include_path="./lib:./test:.:/usr/share/pear"


%files
%defattr(-,root,root,-)
%doc LICENSE *.md doc grammar composer.json
%{_datadir}/php/%{lib_name}

%files test
%defattr(-,root,root,-)
%dir %{_datadir}/tests
     %{_datadir}/tests/%{name}


%changelog
* Tue Jan  8 2013 Remi Collet <remi@fedoraproject.org> 0.9.3-2
- backport 0.9.3 for remi repo.

* Mon Dec 31 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.9.3-2
- Added php_min_ver
- Fixed requires for php_min_ver and non-Fedora

* Thu Dec 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 0.9.3-1
- Initial package
