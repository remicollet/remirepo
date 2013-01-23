%global github_owner   php-fig
%global github_name    log
%global github_version 1.0.0
%global github_commit  fe0936ee26643249e916849d48e3a51d5f5e278b

Name:      php-PsrLog
Version:   %{github_version}
Release:   2%{?dist}
Summary:   Common interface for logging libraries

Group:     Development/Libraries
License:   MIT
URL:       http://www.php-fig.org
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch: noarch

Requires:  php-common >= 5.3.0
# phpci requires
Requires:  php-date
Requires:  php-spl

%description
This package holds all interfaces/classes/traits related to PSR-3
(https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-3-logger-interface.md).

Note that this is not a logger of its own. It is merely an interface that
describes a logger. See the specification for more details.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php/Psr
cp -rp Psr/Log %{buildroot}%{_datadir}/php/Psr/


%files
%doc LICENSE README.md composer.json
%dir %{_datadir}/php/Psr
     %{_datadir}/php/Psr/Log


%changelog
* Tue Jan 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-2
- Updated URL
- Added php-date require

* Thu Jan 10 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.0-1
- Initial package
