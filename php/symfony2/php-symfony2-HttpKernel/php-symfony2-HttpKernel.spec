%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.symfony.com
%global pear_name    %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')
%global php_min_ver  5.3.3
# Broken: require_once(Symfony/Component/HttpKernel/Tests/some_controller_function.php)
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:             php-symfony2-HttpKernel
Version:          2.1.5
Release:          1%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/components
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
Patch0:           %{name}-tests-bootstrap.patch

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})
%if %{with_tests}
# Test requires
BuildRequires:    php(language) >= %{php_min_ver}
BuildRequires:    php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:    php-pear(%{pear_channel}/BrowserKit) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/ClassLoader) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Config) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Console) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/DependencyInjection) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/EventDispatcher) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Finder) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/HttpFoundation) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Process) >= 2.1.0
BuildRequires:    php-pear(%{pear_channel}/Routing) >= 2.1.0
# Test requires: phpci
BuildRequires:    php-date
BuildRequires:    php-json
BuildRequires:    php-pcre
BuildRequires:    php-pdo
BuildRequires:    php-pdo_mysql
BuildRequires:    php-pdo_sqlite
BuildRequires:    php-reflection
BuildRequires:    php-session
BuildRequires:    php-spl
BuildRequires:    php-tokenizer
%endif

Requires:         php(language) >= %{php_min_ver}
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires:         php-pear(%{pear_channel}/EventDispatcher) >= 2.1.0
Requires:         php-pear(%{pear_channel}/HttpFoundation) >= 2.1.0
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-date
Requires:         php-json
Requires:         php-pcre
Requires:         php-pdo
Requires:         php-pdo_mysql
Requires:         php-pdo_sqlite
Requires:         php-reflection
Requires:         php-session
Requires:         php-spl
Requires:         php-tokenizer
# Optional requires
Requires:         php-pear(%{pear_channel}/BrowserKit) >= 2.1.0
Requires:         php-pear(%{pear_channel}/ClassLoader) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Config) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Console) >= 2.1.0
Requires:         php-pear(%{pear_channel}/DependencyInjection) >= 2.1.0
Requires:         php-pear(%{pear_channel}/Finder) >= 2.1.0

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
HttpKernel provides the building blocks to create flexible and fast
HTTP-based frameworks.

It takes a Request as an input and should return a Response as an output.
Using this interface makes your code compatible with all frameworks using
the Symfony2 components. And this will give you many cool features for free.

Optional dependencies: memcache, memcached, mongo


%prep
%setup -q -c -T
tar xif %{SOURCE0}

# Patches
cd %{pear_name}-%{version}
%patch0 -p0
cd ..

# Modify PEAR package.xml file:
# - Remove .gitattributes file
# - Remove .gitignore file
# - Change role from "php" to "doc" for CHANGELOG.md file
# - Change role from "php" to "test" for all test files
# - Remove md5sum from bootsrap.php file since it was patched
sed -e '/\.gitattributes/d' \
    -e '/\.gitignore/d' \
    -e '/CHANGELOG.md/s/role="php"/role="doc"/' \
    -e '/phpunit.xml.dist/s/role="php"/role="test"/' \
    -e '/Tests/s/role="php"/role="test"/' \
    -e '/bootstrap.php/s/md5sum="[^"]*"\s*//' \
    -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
    cd %{pear_name}-%{version}/Symfony/Component/%{pear_name}
    %{_bindir}/phpunit
%else
: Tests skipped, missing '--with tests' option
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-1
- update to 2.1.5

* Thu Nov 29 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-1
- update to 2.1.4

* Thu Nov 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.3-1
- Updated to upstream version 2.1.3
- Removed .gitattributes file from package.xml

* Tue Oct 30 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- sync with rawhide, update to 2.1.3

* Sat Oct  6 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.2-1
- update to 2.1.2

* Fri Sep 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-1
- Updated to upstream version 2.1.2
- Updated description
- PHP minimum version 5.3.3 instead of 5.3.2
- Require other components ">= 2.1.0" instead of "= %%{version}"
- Added php-json and php-session requires
- Removed php-ctype require
- Added PEAR package.xml modifications
- Added patch for tests' bootstrap.php
- Added tests (%%check)
- Changed RPM_BUILD_ROOT to %%{buildroot}
- Added %%global pear_metadir

* Sat Sep 15 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.17-1
- Update to 2.0.17, backport for remi repository

* Sat Sep 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.17-1
- Updated to upstream version 2.0.17
- Added php-reflection require

* Fri Jul 20 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.16-1
- Update to 2.0.16, backport for remi repository

* Wed Jul 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.16-1
- Updated to upstream version 2.0.16
- Minor syntax updates

* Thu Jun 28 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.15-3
- rebuild for remi repository

* Thu Jun 28 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-3
- Added optional requires php-pdo, php-pdo_mysql and php-pdo_sqlite

* Mon Jun 11 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-2
- Added php-pear(%%{pear_channel}/BrowserKit) require
- Added php-pear(%%{pear_channel}/ClassLoader) require
- Added php-pear(%%{pear_channel}/Config) require
- Added php-pear(%%{pear_channel}/Console) require
- Added php-pear(%%{pear_channel}/DependencyInjection) require
- Added php-pear(%%{pear_channel}/Finder) require

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
  php-ctype, php-date, php-pcre, php-spl, php-tokenizer
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
