%global github_owner   doctrine
%global github_name    collections
%global github_version 1.2
%global github_commit  b99c5c46c87126201899afe88ec490a25eedd6a2

# "php": ">=5.3.2"
%global php_min_ver    5.3.2

Name:          php-%{github_owner}-%{github_name}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Collections abstraction library

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from v1.2)
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.2)
Requires:      php-spl

# Extracted from Doctrine Common as of version 2.4
Conflicts:     php-pear(pear.doctrine-project.org/DoctrineCommon) < 2.4

%description
%{summary}.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
# Create tests' autoload
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', str_replace('_', '/', $class)).'.php';
    @include_once $src;
});
AUTOLOAD

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Collections


%changelog
* Mon Feb 17 2014 Remi Collet <rpms@famillecollet.com> 1.2-1
- backport 1.2 for remi repo

* Wed Feb 12 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.2-1
- Updated to 1.2 (BZ #1061117)

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.1-3.20131221git8198717
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-3.20131221git8198717
- Minor syntax changes

* Fri Jan 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-2.20131221git8198717
- Conditional %%{?dist}
- Added conflict w/ PEAR-based DoctrineCommon pkg (version < 2.4)

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1-1.20131221git8198717
- Initial package
