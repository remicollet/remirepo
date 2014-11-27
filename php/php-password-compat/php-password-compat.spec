%global commit 5c5cde8822a69545767f7c7f3058cb15ff84614c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global real_name password_compat


Name:           php-password-compat
Version:        1.0.4
Release:        1%{?dist}
Summary:        PHP password_* functions for PHP 5.3 and 5.4

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/ircmaxell/password_compat
# Upstream tests are exclude from archive
# git clone https://github.com/ircmaxell/password_compat.git
# cd password_compat;  git checkout v1.0.4
# cd ..; tar cvJf password_compat-1.0.4.tar.xz --exclude .git* password_compat
Source0:        %{real_name}-%{version}.tar.xz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-phpunit-PHPUnit

Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for 1.0.4
Requires:       php-openssl
Requires:       php-pcre
# Option
Requires:       php-mbstring
# Optional and ignored php-mcrypt

Provides:       php-composer(ircmaxell/password-compat) = %{version}


%description
Forward compatibility with the password_* functions
being worked on for PHP 5.5


%prep
%setup -q -n %{real_name}


%build
# Empty build section


%install
# create needed directories
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php/%{real_name}
install -m 0644 -p lib/password.php $RPM_BUILD_ROOT%{_datadir}/php/%{real_name}

%check
# Version 1.0.4: OK (32 tests, 32 assertions)
%{_bindir}/phpunit


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc README.md composer.json
%{_datadir}/php/%{real_name}/


%changelog
* Thu Nov 27 2014 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4 #1168498
- drop test from package
- provide php-composer(ircmaxell/password-compat)
- source from git clone (for tests)
- fix license handling
- drop dependency on php-mcrypt #1091225
- add dependency on optional php-mbstring

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-4.git5815cf
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
