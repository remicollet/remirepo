%global github_owner      schmittjoh
%global github_name       parser-lib
%global github_version    1.0.0
%global github_commit     c509473bc1b4866415627af0e1c6cc8ac97fa51d

%global php_min_ver       5.3.0
%global phpoption_min_ver 0.9
%global phpoption_max_ver 2.0

Name:          php-JMSParser
Version:       %{github_version}
Release:       3%{?dist}
Summary:       Library for writing recursive-descent parsers

Group:         Development/Libraries
License:       ASL 2.0
URL:           http://jmsyst.com/libs/%{github_name}
# To create source:
# wget https://github.com/schmittjoh/parser-lib/archive/%%{github_commit}.tar.gz
# php-JMSParser-strip.sh %%{github_version} %%{github_commit}
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-strip.sh

BuildArch:     noarch
# Test build requires
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-PhpOption >= %{phpoption_min_ver}
BuildRequires: php-PhpOption <  %{phpoption_max_ver}
# Test build requires: phpci
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
Requires:      php-PhpOption >= %{phpoption_min_ver}
Requires:      php-PhpOption <  %{phpoption_max_ver}
# phpci requires
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

%description
%{summary}.


%prep
%setup -q -n %{github_name}-%{github_commit}

# Rewrite tests' bootstrap (which uses Composer autoloader) with simple
# autoloader that uses include path
( cat <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
AUTOLOAD
) > tests/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/JMS
cp -rp src/JMS/Parser %{buildroot}%{_datadir}/php/JMS/


%check
%{_bindir}/phpunit \
    -d include_path="./src:./tests:.:%{pear_phpdir}:%{_datadir}/php" \
    -c phpunit.xml.dist


%files
%doc LICENSE README.md composer.json
%dir %{_datadir}/php/JMS
     %{_datadir}/php/JMS/Parser


%changelog
* Mon Mar 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-3
- Added %%{name}-strip.sh as Source1

* Sat Mar 16 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Added phpoption_min_ver and phpoption_max_ver globals
- Bad licensed files stripped from source
- php-common => php(language)
- Removed tests sub-package

* Thu Jan 24 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
