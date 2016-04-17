# remirepo/fedora spec file for php-pear-crypt-gpg
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name Crypt_GPG
%if 0%{?rhel}
# All features require GnuPG v1 (under investigation)
%global with_tests 0%{?_with_tests:1}
%else
%global with_tests 0%{!?_without_tests:1}
%endif

Name:           php-pear-crypt-gpg
Version:        1.4.1
Release:        1%{?dist}
Summary:        GNU Privacy Guard (GnuPG)

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
%if %{with_tests}
# for tests
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  %{_bindir}/gpg
BuildRequires:  %{_bindir}/gpg-agent
BuildRequires:  %{_bindir}/ps
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)

Requires:       %{_bindir}/gpg
# From package.pear
Requires:       php(language) >= 5.2.1
Requires:       php-pear(Console_CommandLine) >= 1.1.10
Requires:       php-mbstring
# From phpcompatinfo report for version 1.4.1
Requires:       php-ctype
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-spl
# Optional
Requires:       php-posix

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-composer(pear/crypt_gpg) = %{version}


%description
This package provides an object oriented interface to 
GNU Privacy Guard (GnuPG).

Though GnuPG can support symmetric-key cryptography, this package
is intended only to facilitate public-key cryptography.


%prep
%setup -q -c

%{?_licensedir:sed -e '/LICENSE/d' -i package.xml}

cd %{pear_name}-%{version}
mv  ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%if %{with_tests}
%check
cd %{pear_name}-%{version}/tests

%{_bindir}/phpunit --verbose .

if which php70; then
   php70 %{_bindir}/phpunit --verbose .
fi
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{?_licensedir:%license %{pear_name}-%{version}/LICENSE}
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{_bindir}/crypt-gpg-pinentry
%dir %{pear_phpdir}/Crypt
     %{pear_phpdir}/Crypt/GPG*


%changelog
* Sun Apr 17 2016 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1

* Fri Dec 18 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Initial package, version 1.4.0 (stable)
- open https://github.com/pear/Crypt_GPG/pull/19 for fsf address
