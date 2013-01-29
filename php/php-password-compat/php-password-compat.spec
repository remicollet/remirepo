%global commit 58151cf24e73119576c2a016393120f9c146448b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global real_name password_compat


Name:           php-password-compat
Version:        1.0.0
Release:        4.git%{shortcommit}%{?dist}
Summary:        PHP password_* function for PHP 5.3 and 5.4

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/ircmaxell/password_compat
Source0:        https://github.com/ircmaxell/%{real_name}/archive/%{commit}/%{real_name}-%{version}-%{shortcommit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

Requires:       php(language) >= 5.3.7
Requires:       php-mcrypt
Requires:       php-openssl
Requires:       php-pcre


%description
Forward compatibility with the password_* functions
being worked on for PHP 5.5


%prep
%setup -q -n %{real_name}-%{commit}


%build
# Empty build section


%install
# create needed directories
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php/%{real_name}
install -m 0644 -p lib/password.php $RPM_BUILD_ROOT%{_datadir}/php/%{real_name}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/tests/%{real_name}
cp -pr test $RPM_BUILD_ROOT%{_datadir}/tests/%{real_name}

%check
cd test

# Version 1.0.0-1-git58121cf : OK (30 tests, 30 assertions)
%{_bindir}/phpunit


%files
%defattr(-,root,root,-)
%doc LICENSE.md README.md composer.json
%dir %{_datadir}/php/%{real_name}
%{_datadir}/php/%{real_name}/*
%dir %{_datadir}/tests
%dir %{_datadir}/tests/%{real_name}
%{_datadir}/tests/%{real_name}/*


%changelog
* Tue Jan 29 2013 Remi Collet <rpms@fedoraproject.org> - 1.0.0-4.git5815cf
- backport for remi repo

* Tue Jan 29 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-4.git5815cf
- License was not incorrect...
- Directory not owned

* Mon Jan 28 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-3.git58151cf
- incorrect licence

* Mon Jan 28 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-2.git58151cf
- improve Requires
- drop buildroot removal (not targetted on el-5)
- update description
- fix %%check comment
- move tests in %%{_datadir}/tests instead of %%{_datadir}/php

* Wed Jan 16 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 1.0.0-1.git58151cf
- Initial Release
