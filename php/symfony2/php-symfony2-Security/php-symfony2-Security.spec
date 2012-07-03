%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_channel pear.symfony.com
%global pear_name %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')

Name:             php-symfony2-Security
Version:          2.0.15
Release:          3%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/components
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.3.2
Requires:         php-date
Requires:         php-hash
Requires:         php-json
Requires:         php-openssl
Requires:         php-pcre
Requires:         php-pdo
Requires:         php-reflection
Requires:         php-spl
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires:         php-pear(%{pear_channel}/HttpKernel) = %{version}
Requires:         php-pear(%{pear_channel}/HttpFoundation) = %{version}
Requires:         php-pear(%{pear_channel}/EventDispatcher) = %{version}
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# Optional require
Requires:         php-pear(%{pear_channel}/ClassLoader) = %{version}
Requires:         php-pear(%{pear_channel}/Finder) = %{version}
Requires:         php-pear(%{pear_channel}/Form) = %{version}
Requires:         php-pear(%{pear_channel}/Routing) = %{version}

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Security provides an infrastructure for sophisticated authorization systems,
which makes it possible to easily separate the actual authorization logic from
so called user providers that hold the users credentials. It is inspired by
the Java Spring framework.

Optional dependencies: DoctrineCommon and DoctrineDBAL


%prep
%setup -q -c
# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml

# Change PEAR role of *.sql files from doc to php.
# Fixed in upstream version 2.1.0 BETA1.
sed -i \
    's#<file *md5sum="\([^"]\+\)" *name="\([^"]\+.sql\)" *role="doc" */>#<file md5sum="\1" name="\2" role="php" />#' \
    %{pear_name}-%{version}/%{name}.xml


%build
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
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}


%changelog
* Sat Jun 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-3
- Added php-pdo require
- Updated %%description
- Changed PEAR role of *.sql files from doc to php.

* Mon Jun 11 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-2
- Added php-pear(%%{pear_channel}/ClassLoader) require
- Added php-pear(%%{pear_channel}/Finder) require
- Added php-pear(%%{pear_channel}/Form) require
- Added php-pear(%%{pear_channel}/Routing) require

* Wed May 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-1
- Updated to upstream version 2.0.15
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Updated %%prep section
- Removed cleaning buildroot from %%install section
- Removed documentation move from %%install section (fixed upstream)
- Removed %%clean section
- Updated %%doc in %%files section

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-3
- Moved documentation to correct location

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-date, php-hash, php-json, php-openssl, php-pcre, php-reflection,
  php-spl
- Removed %%defattr from %%files section
- Removed ownership for directories already owned by required packages

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-1
- Updated to upstream version 2.0.14
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Wed May 2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.13-1
- Updated to upstream version 2.0.13

* Sat Apr 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.12-1
- Initial package
