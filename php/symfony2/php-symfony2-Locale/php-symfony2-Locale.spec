%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.symfony.com
%global pear_name    %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')
%global php_min_ver  5.3.3
# Lot of failures, need investigation
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:             php-symfony2-Locale
Version:          2.1.6
Release:          1%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/doc/current/components/locale.html
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
# Test requires: phpci
BuildRequires:    php-ctype
BuildRequires:    php-date
BuildRequires:    php-intl
BuildRequires:    php-pcre
BuildRequires:    php-reflection
BuildRequires:    php-simplexml
BuildRequires:    php-spl
%endif

Requires:         php(language) >= %{php_min_ver}
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-ctype
Requires:         php-date
Requires:         php-intl
Requires:         php-pcre
Requires:         php-reflection
Requires:         php-simplexml
Requires:         php-spl

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Locale component provides fallback code to handle cases when the intl extension
is missing. Additionally it extends the implementation of a native Locale
(http://php.net/manual/en/class.locale.php) class with several handy methods.

Replacement for the following functions and classes is provided:

* intl_is_failure
* intl_get_error_code
* intl_get_error_message
* Collator
* IntlDateFormatter
* Locale
* NumberFormatter

Stub implementation only supports the en locale.


%prep
%setup -q -c

# Patches
cd %{pear_name}-%{version}
%patch0 -p0
cd ..

# Modify PEAR package.xml file:
# - Remove .gitattributes file
# - Remove .gitignore file
# - Change role from "php" to "doc" for UPDATE.txt file
# - Change role from "php" to "doc" for CHANGELOG.md file
# - Change role from "php" to "test" for all test files
# - Remove md5sum from bootsrap.php file since it was patched
sed -e '/\.gitattributes/d' \
    -e '/\.gitignore/d' \
    -e '/UPDATE.txt/s/role="php"/role="doc"/' \
    -e '/CHANGELOG.md/s/role="php"/role="doc"/' \
    -e '/phpunit.xml.dist/s/role="php"/role="test"/' \
    -e '/Tests/s/role="php"/role="test"/' \
    -e '/bootstrap.php/s/md5sum="[^"]*"\s*//' \
    -e '/.git/d' \
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

# Lang files
for res_file in \
    %{buildroot}%{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/*/*.res
do
    res_file_lang=$(basename $res_file | sed 's#\(_.*\)*\.res##')
    echo "%lang($res_file_lang) $res_file"
done > ../%{name}.lang
sed -i "s#) %{buildroot}#) #" ../%{name}.lang

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


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Symfony
%dir %{pear_phpdir}/Symfony/Component
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Exception
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Locale.php
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/lang
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/locales
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/names
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/region
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/stub
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/49/*.*
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/*.*
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/stubs
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Stub
%{pear_testdir}/%{pear_name}


%changelog
* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.6-1
- update to 2.1.6 (no change)

* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-1
- update to 2.1.5

* Thu Nov 29 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-1
- update to 2.1.4

* Tue Nov 13 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.3-2
- Removed .gitattributes and .gitignore files from package.xml

* Sun Nov 11 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.3-1
- Updated to upstream version 2.1.3

* Tue Oct 30 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- sync with rawhide, update to 2.1.3

* Mon Oct 29 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-2
- Added "%%global pear_metadir" and usage in %%install
- Changed RPM_BUILD_ROOT to %%{buildroot}
- Added %%{with_tests} for build requires

* Sat Oct 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-1
- Updated to upstream version 2.1.2
- PHP minimum version 5.3.3 instead of 5.3.2
- Added php-reflection and php-simplexml requires
- Added PEAR package.xml modifications
- Added patch for tests' bootstrap.php
- Added tests (%%check)

* Sat Sep 15 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.17-1
- Update to 2.0.17, backport for remi repository

* Sat Sep 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.17-1
- Updated to upstream version 2.0.17
- Added php-spl require

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.16-1
- Update to 2.0.16, backport for remi repository

* Sun Jul 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.16-1
- Updated to upstream version 2.0.16
- Removed package.xml fix for *.res files (fixed upstream)
- Added package.xml fix for an UPDATE.txt file
- Minor syntax updates

* Thu Jun 28 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.15-3
- rebuild for remi repository

* Sun Jun 23 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-3
- Added %%lang directive flags for *.res files
- Modified %%files because of separate *.res file listings

* Tue Jun 12 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-2
- Fix package.xml for *.res files issue

* Wed May 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-1
- Updated to upstream version 2.0.15
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Updated %%prep section
- Removed cleaning buildroot from %%install section
- Removed documentation move from %%install section (fixed upstream)
- Removed %%clean section
- Updated %%doc in %%files section

* Wed May 23 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-4
- Added missing php-intl require

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-3
- Moved documentation to correct location

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-ctype, php-date, php-pcre
- Removed %%defattr from %%files section

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-1
- Updated to upstream version 2.0.14
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Wed May 2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.13-1
- Updated to upstream version 2.0.13

* Sat Apr 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.12-1
- Initial package
