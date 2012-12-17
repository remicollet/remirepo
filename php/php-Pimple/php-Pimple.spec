%global libname     Pimple
%global php_min_ver 5.3.0

Name:          php-%{libname}
Version:       1.0.1
Release:       1%{?dist}
Summary:       A simple Dependency Injection Container for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://pimple.sensiolabs.org
Source0:       https://github.com/fabpot/%{libname}/archive/v%{version}.tar.gz


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
# Test requires
BuildRequires: php-common >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# Test requires: phpci
BuildRequires: php-spl

Requires:      php-common >= %{php_min_ver}
# phpci requires
Requires:      php-spl

%description
Pimple is a small Dependency Injection Container for PHP that consists of
just one file and one class.


%prep
%setup -q -n %{libname}-%{version}

# Update and move tests' PHPUnit config
sed 's#tests/##' -i phpunit.xml.dist
mv phpunit.xml.dist tests/

# Update tests' require
sed "s#.*require.*Pimple.php.*#require_once '%{libname}/Pimple.php';#" \
    -i tests/bootstrap.php


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{libname}
cp -pr lib/* %{buildroot}%{_datadir}/php/%{libname}/

mkdir -p -m 755 %{buildroot}%{_datadir}/tests/%{name}
cp -pr tests/* %{buildroot}%{_datadir}/tests/%{name}/


%check
%{_bindir}/phpunit \
    -d include_path=%{buildroot}%{_datadir}/php:.:%{pear_phpdir} \
    -c tests/phpunit.xml.dist


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst composer.json
%{_datadir}/php/%{libname}
%dir %{_datadir}/tests
     %{_datadir}/tests/%{name}


%changelog
* Mon Dec 17 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- backport 1.0.1 for remi repo.

* Sun Dec 16 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.1-1
- Updated to upstream version 1.0.1

* Mon Dec  3 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-2
- backport for remi repo.

* Sun Dec  2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Removed "5.3" from summary and description
- Changed update tests' require path to use standard PHP include_path
- Changed %%check to override include_path in PHPunit call instead of
  updating file

* Fri Nov 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
