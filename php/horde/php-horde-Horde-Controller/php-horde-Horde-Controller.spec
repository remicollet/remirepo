%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Controller

Name:           php-horde-Horde-Controller
Version:        1.0.2
Release:        2%{?dist}
Summary:        Horde Controller libraries

Group:          Development/Libraries
License:        BSD
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php-pear >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Injector) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Log) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Support) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)
Requires:       php-common >= 5.2.0
Requires:       php-mbstring php-zlib

Provides:       php-pear(pear.horde.org/%{pear_name}) = %{version}

%description
This package provides the controller part of an MVC system for Horde.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Controller
%{pear_phpdir}/Horde/Controller.php
%{pear_testdir}/Horde_Controller
%doc %{pear_docdir}/Horde_Controller/COPYING

%changelog
* Mon Jun 25 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-2
- Fix requires

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-1
- Upgrade to 1.0.2

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
