%global github_owner   fabpot
%global github_name    Pimple
%global github_version 1.1.0
%global github_commit  471c7d7c52ad6594e17b8ec33efdd1be592b5d83

%global php_min_ver    5.3.0

Name:          php-%{github_name}
Version:       %{github_version}
Release:       4%{?dist}
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


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/%{github_name}
cp -pr lib/* %{buildroot}%{_datadir}/php/%{github_name}/



%check
%{_bindir}/phpunit --include-path="./lib:./tests"


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst composer.json
%{_datadir}/php/%{github_name}


%changelog
* Thu Nov 21 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-4
- sync remi repo with rawhide

* Thu Nov 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-4
- Reverted invalid PSR-0
- Updated %%check to use PHPUnit's "--include-path" option

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
