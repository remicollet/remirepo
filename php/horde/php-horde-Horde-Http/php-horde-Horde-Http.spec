%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Http

Name:           php-horde-Horde-Http
Version:        1.1.1
Release:        1%{?dist}
Summary:        Horde HTTP libraries

Group:          Development/Libraries
License:        BSD
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Support) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)

%description
This package provides a set of classes for making HTTP requests.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Http
%{pear_phpdir}/Horde/Http.php
%{pear_testdir}/Horde_Http

%changelog
* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-1
- backport for remi repo

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.1-1
- Upgrade to 1.1.1

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.0-1
- Initial package
