# remirepo/fedora spec file for php-pear-math-biginteger
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name Math_BigInteger

Name:           php-pear-math-biginteger
Version:        1.0.3
Release:        1%{?dist}
Summary:        Pure-PHP arbitrary precision integer arithmetic library

Group:          Development/Libraries
# full license text included in single file.
# see https://github.com/pear/Math_BigInteger/pull/7
License:        MIT
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pcre
Requires:       php-openssl

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-composer(pear/math_biginteger) = %{version}
%if 0%{?fedora} < 26
Conflicts:      php-phpseclib-math-biginteger < 2
%else
Obsoletes:      php-phpseclib-math-biginteger < 2
# Use epoch to avoid self-obsoletion php-phpseclib-math-biginteger
# as phpseclib latest upstream version is 1.0.5 which is > 1.0.3
Provides:       php-phpseclib-math-biginteger = 1:%{version}
Provides:       php-pear(phpseclib.sourceforge.net/%{pear_name}) = %{version}
%endif


%description
Supports base-2, base-10, base-16, and base-256 numbers. Uses the GMP or
BCMath extensions, if available, and an internal implementation, otherwise.


%prep
%setup -q -c
cd %{pear_name}-%{version}
# See https://github.com/pear/Math_BigInteger/pull/5
sed -e '/demo/s/role="php"/role="doc"/' \
    -e '/demo/s/baseinstalldir="[^"]*" //' \
    -e '/benchmark/s/md5sum="[^"]*" //' \
    ../package.xml | tee %{name}.xml | grep '<file'

sed -e 's/\r//' -i demo/benchmark.php


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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Math


%changelog
* Fri Dec  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- cleanup

* Thu Aug 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- initial package, version 1.0.3
- fix documentation files role
  open https://github.com/pear/Math_BigInteger/pull/5 Role
- open https://github.com/pear/Math_BigInteger/pull/6 Typo
- open https://github.com/pear/Math_BigInteger/pull/7 License
