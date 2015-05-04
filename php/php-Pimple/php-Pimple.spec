%global github_owner        silexphp
%global github_name         Pimple
%global github_version      3.0.0
%global github_commit       876bf0899d01feacd2a2e83f04641e51350099ef
%global packagist_owner     pimple
%global packagist_name      pimple
%global namespace           %{github_name}

%global php_min_ver    5.3.0

Name:          php-%{github_name}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       A simple dependency injection container for PHP

Group:         Development/Libraries
License:       MIT
URL:           http://pimple.sensiolabs.org
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# for tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit
BuildRequires: %{_bindir}/phpab
# phpcompatinfo (computed from v1.1.1)
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.1.1)
Requires:      php-spl

Provides:       php-composer(%{packagist_owner}/%{packagist_name}) = %{version}

%description
Pimple is a small dependency injection container for PHP that consists of
just one file and one class.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -pr src/%{namespace} %{buildroot}%{_datadir}/php
# clean out tests
rm -r %{buildroot}%{_datadir}/php/%{namespace}/Tests


%check
# roll our own loader to run tests (can't seem to get it to load the fixtures
# with --include-path any more)
%{_bindir}/phpab --output bootstrap.php --exclude *Test.php --basedir . src
%{_bindir}/phpunit --bootstrap bootstrap.php


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst composer.json
%{_datadir}/php/%{namespace}


%changelog
* Tue Dec 30 2014 Adam Williamson <awilliam@redhat.com> - 3.0.0-1
- new release 3.0.0 (changes layout, BC break)

* Mon Feb 17 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- backport 1.1.1 for remi repo

* Sat Feb 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Updated to 1.1.1 (BZ #1061119)

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
