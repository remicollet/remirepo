%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}

%global pear_channel    pear.doctrine-project.org
%global pear_name       DoctrineORM

%global symfony_min_ver 2.0
%global symfony_max_ver 3.0

Name:             php-doctrine-%{pear_name}
Version:          2.3.3
Release:          1%{?dist}
Summary:          Doctrine Object Relational Mapper

Group:            Development/Libraries
# License clarification from upstream since both MIT and LGPL are found:
# https://groups.google.com/d/topic/doctrine-dev/BNd84oKdOP0/discussion
License:          MIT
URL:              http://www.doctrine-project.org/projects/orm.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.3.0
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires:         php-pear(%{pear_channel}/DoctrineCommon) >= 2.3.0
Requires:         php-pear(%{pear_channel}/DoctrineCommon) <  2.4.0
Requires:         php-pear(%{pear_channel}/DoctrineDBAL) >= 2.3.0
Requires:         php-pear(%{pear_channel}/DoctrineDBAL) <  2.4.0
Requires:         php-pear(pear.symfony.com/Console) >= %{symfony_min_ver}
Requires:         php-pear(pear.symfony.com/Console) <  %{symfony_max_ver}
Requires:         php-pear(pear.symfony.com/Yaml) >= %{symfony_min_ver}
Requires:         php-pear(pear.symfony.com/Yaml) <  %{symfony_max_ver}
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-ctype
Requires:         php-dom
Requires:         php-pcre
Requires:         php-pdo
Requires:         php-reflection
Requires:         php-simplexml
Requires:         php-spl
Requires:         php-tokenizer

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Object relational mapper (ORM) for PHP that sits on top of a powerful
database abstraction layer (DBAL). One of its key features is the option
to write database queries in a proprietary object oriented SQL dialect
called Doctrine Query Language (DQL), inspired by Hibernate's HQL. This
provides developers with a powerful alternative to SQL that maintains
flexibility without requiring unnecessary code duplication.


%prep
%setup -q -c

# Modify package.xml
# - Fix role for README, LICENSE, and UPGRADE files (role="data" => role="doc")
# - Remove doctrine.bat
# *** http://www.doctrine-project.org/jira/browse/DDC-1913
sed -i \
    -e '/README.markdown/s/role="data"/role="doc"/' \
    -e '/LICENSE/s/role="data"/role="doc"/' \
    -e '/UPGRADE/s/role="data"/role="doc"/' \
    -e '/<file.*doctrine.bat/,/<\/file>/d' \
    -e '/<install.*doctrine.bat/d' \
    package.xml

# Make a single executable
pushd %{pear_name}-%{version}/bin
rm -f doctrine
(
    echo '#!@php_bin@'
    cat doctrine-pear.php
) > doctrine
chmod +x doctrine
rm -f doctrine-pear.php
popd
# Modify PEAR package.xml for above changes
# - Remove doctrine-pear.php file
# - Remove md5sum from doctrine file since it was changed
sed -e '/doctrine-pear.php/d' \
    -e '/name="bin\/doctrine"/s/md5sum="[^"]*"\s*//' \
    -i package.xml

# Remove doctrine.bat

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
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/Doctrine/ORM
%{_bindir}/doctrine


%changelog
* Sun Jun 30 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.3.3-1
- backport for remi repo.

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.3-1
- Updated to 2.3.3
- Fixed license
- Added php-dom require
- Made a single executable (removed doctrine-pear.php)
- Removed doctrine.bat
- Added "%%global pear_metadir" and usage in %%install
- Changed RPM_BUILD_ROOT to %%{buildroot}

* Wed Jul 4 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.2-1
- Initial package
