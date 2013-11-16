%global github_owner   fabpot
%global github_name    Pimple
%global github_version 1.1.0
%global github_commit  471c7d7c52ad6594e17b8ec33efdd1be592b5d83

%global php_min_ver    5.3.0

Name:          php-%{github_name}
Version:       %{github_version}
Release:       3%{?dist}
Summary:       A simple dependency injection container for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://pimple.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# phpci
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpci
Requires:      php-spl

%description
Pimple is a small dependency injection container for PHP that consists of
just one file and one class.

NOTE: %{_datadir}/php/%{github_name}/%{github_name}.php is provided for legacy
      (pre PSR-0 packaging guidelines update) compatibility
      and will be removed in version 2.  Please use PSR-0
      compliant %{_datadir}/php/%{github_name}.php instead.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -pm 755 %{buildroot}%{_datadir}/php
cp -p lib/Pimple.php %{buildroot}%{_datadir}/php/

# Legacy (pre PSR-0 packaging guidelines update)
mkdir -pm 755 %{buildroot}%{_datadir}/php/%{github_name}
ln -s ../Pimple.php %{buildroot}%{_datadir}/php/%{github_name}/Pimple.php


%check
%{_bindir}/phpunit -d include_path="./lib:./tests:%{pear_phpdir}"


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst composer.json
%{_datadir}/php/%{github_name}
%{_datadir}/php/Pimple.php


%changelog
* Sat Nov 16 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-3
- backport 1.1.0 for remi repo.

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-3
- Updated description with note about PSR-0 and legacy compatibility

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-2
- Updated file location for PSR-0 compliance

* Fri Nov 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Updated to 1.1.0
- php-common => php(language)

* Sat Mar 09 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- backport 1.0.2 for remi repo.

* Fri Mar 08 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.2-1
- Updated to upstream version 1.0.2
- Updates per new Fedora packaging guidelines for Git repos
- Removed tests

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
