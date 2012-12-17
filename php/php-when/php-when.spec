Name:           php-when
Version:        0.3
Release:        2%{?dist}
Summary:        Date/Calendar recursion library for PHP

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/tplaner/When
# Download from
# https://github.com/tplaner/When/archive/v0.3.tar.gz
Source0:        When-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php-date php-spl

%description
PHP library that handles recursive dates: It determines the next date of
recursion given an iCalendar "rrule" like pattern.

%package tests
Summary:        Test files for %{name}
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}
# phpunit tests
Requires:       php-phpunit-PHPUnit
BuildRequires:  php-phpunit-PHPUnit

%description tests
PHPUnit tests for %{name}.

%prep
%setup -q -n When-%{version}

# remove deprecated include and set prefix
sed -e '/Framework.php/d' \
    -e '/When.php/s:./:when/:' \
    -e '/When_Iterator.php/s:./:when/:' \
    -i Tests/*php

%build

%install
mkdir -p %{buildroot}%{_datadir}/php/when
install -pm 644 When.php %{buildroot}%{_datadir}/php/when
install -pm 644 When_Iterator.php %{buildroot}%{_datadir}/php/when

mkdir -p %{buildroot}%{_datadir}/tests/%{name}
install -pm 644 Tests/*.php %{buildroot}%{_datadir}/tests/%{name}/

%check
cd Tests
phpunit -d include_path=%{buildroot}%{_datadir}/php:.:%{_datadir}/php:%{_datadir}/pear -d date.timezone=UTC .


%files
%defattr(-,root,root,-)
%doc README.md
%{_datadir}/php/when


%files tests
%defattr(-,root,root,-)
%dir %{_datadir}/tests
%{_datadir}/tests/%{name}


%changelog
* Mon Dec 17 2012 Remi Collet <remi@fedoraproject.org> - 0.3-2
- backport for remi repo.

* Sat Dec 15 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 0.3-2
- enabled phpunit tests
- moved tests to %%{_datadir}/tests/%%{name}

* Tue Dec 11 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 0.3-1
- Initial package

