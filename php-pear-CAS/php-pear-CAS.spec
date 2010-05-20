%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name CAS
%global channel   __uri
#global prever    RC7


Name:           php-pear-CAS
Version:        1.1.0
Release:        %{?prever:0.}1%{?prever:.}%{?prever}%{?dist}.1
Summary:        Central Authentication Service client library in php

Group:          Development/Libraries
License:        BSD
URL:            http://www.ja-sig.org/wiki/display/CASC/phpCAS
Source0:        http://www.ja-sig.org/downloads/cas-clients/php/%{version}%{?prever}/%{pear_name}-%{version}%{?prever}.tgz

Patch0:         php-pear-CAS-systemlibs.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(DB) >= 1.4.0
Requires:       php-pear(PEAR) >= 1.4.3
Requires:       php-domxml-php4-php5
Provides:       php-pear(%{channel}/%{pear_name}) = %{version}
# this library is mostly known as phpCAS
Provides:       phpCAS = %{version}-%{release}


%description
This package is a PEAR library for using a Central Authentication Service.


%prep
%setup -q -c

# Package is V2
mv package.xml %{pear_name}-%{version}%{?prever}/%{name}.xml
cd %{pear_name}-%{version}%{?prever}

# converting to unix format mandatory for old patch version
sed -i -e 's/\r//' CAS.php
%patch0 -p1 -b .systemlib


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT docdir
cd %{pear_name}-%{version}%{?prever}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml


# Move documentation
mv $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name} ../docdir
for fic in ../docdir/docs/examples/example*.php; do
   sed -i -e 's/\r//' $fic
done

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc docdir/docs/*
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/CAS
%{pear_phpdir}/CAS.php


%changelog
* Thu May 20 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1.1
- fix pacth for EL4 (remi repo only)

* Thu May 20 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1
- update to 1.1.0 finale

* Sun Mar 14 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-0.1.RC7
- initial packaging (using pear make-rpm-spec CAS-1.1.0RC7.tgz)

