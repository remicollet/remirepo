Name:           php-phpass
Version:        0.3
Release:        2%{?dist}
Summary:        Portable password hashing framework for use in PHP applications

License:        Public Domain
URL:            http://www.openwall.com/phpass/
Source0:        http://www.openwall.com/phpass/phpass-0.3.tar.gz
Source1:        phpass-README.devel

BuildArch:      noarch

BuildRequires:  php-cli

Requires:       php-common

%description
phpass (pronounced "pH pass") is a portable public domain password hashing
framework for use in PHP applications. It is meant to work with PHP 3 and
above.

The preferred (most secure) hashing method supported by phpass is the
OpenBSD-style Blowfish-based bcrypt and known in PHP as CRYPT_BLOWFISH, with
a fallback to BSDI-style extended DES-based hashes, known in PHP as
CRYPT_EXT_DES, and a last resort fallback to MD5-based salted and variable
iteration count password hashes implemented in phpass
itself (also referred to as portable hashes).


%prep
%setup -q -n phpass-%{version}

cp -a %{SOURCE1} README.devel


%build

%install
mkdir -p %{buildroot}/%{_datadir}/php/phpass
install -pm 644 PasswordHash.php %{buildroot}%{_datadir}/php/phpass


%check
php test.php | grep PASSED


%files
%doc test.php c README.devel
%dir %{_datadir}/php/phpass
%{_datadir}/php/phpass/PasswordHash.php


%changelog
* Sun Dec 16 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 0.3-2
- enabled tests

* Tue Dec 11 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 0.3-1
- Initial package

