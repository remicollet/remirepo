# remirepo spec file for php-phpseclib-math-biginteger, from:
#
# Fedora spec file for php-phpseclib-math-biginteger
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%{!?__pear:       %global __pear %{_bindir}/pear}
%global pear_name Math_BigInteger

Name:           php-phpseclib-math-biginteger
Version:        1.0.5
Release:        1%{?dist}
Summary:        Pure-PHP arbitrary precision integer arithmetic library

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(phpseclib.sourceforge.net)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(phpseclib.sourceforge.net)
# phpcompatinfo, generated from 0.3.5
Requires:       php-date
Requires:       php-pcre

Provides:       php-pear(phpseclib.sourceforge.net/Math_BigInteger) = %{version}


%description
Supports base-2, base-10, base-16, and base-256 numbers.  Uses the GMP or
BCMath extensions and the OpenSSL extension, if available, and an internal
implementation, otherwise.


%prep
%setup -q -c
mv package.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


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
        phpseclib.sourceforge.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%{pear_xmldir}/%{name}.xml
# php-pear-Math-Stats also owns the directory, but a dependency on it
# does not seem to make sense
%{pear_phpdir}/Math


%changelog
* Tue Oct 25 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5 (no change)

* Tue Oct 04 2016 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Wed May 11 2016 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Tue Jan 19 2016 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1 (no change)

* Mon Aug 03 2015 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 10 2015 Remi Collet <remi@fedoraproject.org> - 0.3.10-1
- Update to 0.3.10

* Mon Nov 10 2014 Remi Collet <remi@fedoraproject.org> - 0.3.9-1
- Update to 0.3.9

* Sat Sep 13 2014 Remi Collet <remi@fedoraproject.org> - 0.3.8-1
- Update to 0.3.8

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 0.3.7-1
- Update to 0.3.7

* Wed Feb 26 2014 Remi Collet <remi@fedoraproject.org> - 0.3.6-1
- Update to 0.3.6

* Wed Jan 15 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-2
- backport for remi repo

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
