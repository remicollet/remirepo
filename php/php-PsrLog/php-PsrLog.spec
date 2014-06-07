%global github_owner     php-fig
%global github_name      log
%global github_version   1.0.0
%global github_commit    fe0936ee26643249e916849d48e3a51d5f5e278b

%global composer_vendor  psr
%global composer_project log

Name:      php-PsrLog
Version:   %{github_version}
Release:   5%{?dist}
Summary:   Common interface for logging libraries

Group:     Development/Libraries
License:   MIT
URL:       http://www.php-fig.org/psr/psr-3/
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  php(language) >= 5.3.0
# phpcompatinfo requires (computed from version 1.0.0)
Requires:  php-date
Requires:  php-spl

Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This package holds all interfaces/classes/traits related to PSR-3
(https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-3-logger-interface.md).

Note that this is not a logger of its own. It is merely an interface that
describes a logger. See the specification for more details.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php
cp -rp Psr %{buildroot}%{_datadir}/php/


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%dir %{_datadir}/php/Psr
     %{_datadir}/php/Psr/Log


%changelog
* Sat Jun  7 2014 Remi Collet <remi@fedoraproject.org> 1.0.0-5
- backport rawhide changes.

* Fri Jun 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.0.0-5
- Updated URL
- Requires php-common => php(language)
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> 1.0.0-2
- backport 1.0.0 for remi repo.

* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Updated URL
- Added php-date require

* Thu Jan 10 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
