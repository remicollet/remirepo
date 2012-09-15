%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.symfony.com
%global pear_name    %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')

Name:             php-symfony2-Locale
Version:          2.0.17
Release:          1%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/doc/current/components/locale.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.3.2
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-ctype
Requires:         php-date
Requires:         php-intl
Requires:         php-pcre
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
# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml

# Fix package.xml for "Symfony/Component/Locale/Resources/data/UPDATE.txt" file
# incorrectly being identified with role="php" instead of role="doc"
# *** NOTE: This needs to be fixed upstream (was fine in 2.0.15, but changed
#           in 2.0.16)
sed -i \
    's#<file *md5sum="\([^"]*\)" *name="\(Symfony/Component/Locale/Resources/data/UPDATE.txt\)" *role="php" */>#<file md5sum="\1" name="\2" role="doc" />#' \
    %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Lang files
for res_file in \
    $RPM_BUILD_ROOT%{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/*/*.res
do
    res_file_lang=$(basename $res_file | sed 's#\(_.*\)*\.res##')
    echo "%lang($res_file_lang) $res_file"
done > ../%{name}.lang
sed -i "s#) $RPM_BUILD_ROOT#) #" ../%{name}.lang

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
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/lang
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/locales
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/names
%dir %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/region
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/stub
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/data/update-data.php
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Resources/stubs
     %{pear_phpdir}/Symfony/Component/%{pear_name}/Stub


%changelog
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
