%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}

%global pear_channel pear.doctrine-project.org
%global pear_name    DoctrineDBAL

Name:             php-doctrine-%{pear_name}
Version:          2.3.4
Release:          4%{?dist}
Summary:          Doctrine Database Abstraction Layer

Group:            Development/Libraries
# License clarification from upstream since both MIT and LGPL are found:
# https://groups.google.com/d/topic/doctrine-dev/BNd84oKdOP0/discussion
License:          MIT
URL:              http://www.doctrine-project.org/projects/dbal.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php(language) >= 5.3.2
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires:         php-pear(%{pear_channel}/DoctrineCommon) >= 2.3.0
Requires:         php-pear(%{pear_channel}/DoctrineCommon) <  2.5.0
Requires:         php-pear(pear.symfony.com/Console) >= 2.0
Requires:         php-pear(pear.symfony.com/Console) <  3.0
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-date
Requires:         php-json
Requires:         php-pcre
Requires:         php-pdo
Requires:         php-spl

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
The Doctrine database abstraction & access layer (DBAL) offers a lightweight
and thin runtime layer around a PDO-like API and a lot of additional,
horizontal features like database schema introspection and manipulation
through an OO API.

The fact that the Doctrine DBAL abstracts the concrete PDO API away through
the use of interfaces that closely resemble the existing PDO API makes it
possible to implement custom drivers that may use existing native or self-made
APIs. For example, the DBAL ships with a driver for Oracle databases that uses
the oci8 extension under the hood.


%prep
%setup -q -c

# Fix package.xml:
# - Remove empty README
# - LICENSE file to have role="doc" instead of role="data"
# *** http://www.doctrine-project.org/jira/browse/DBAL-300
sed -e '/README/d' \
    -e '/LICENSE/s/role="data"/role="doc"/' \
    -i package.xml

# Make a single executable
pushd %{pear_name}-%{version}/bin
rm -f doctrine-dbal
(
    echo '#!%{_bindir}/php'
    cat doctrine-dbal.php
) > doctrine-dbal
chmod +x doctrine-dbal
rm -f doctrine-dbal.php
popd
# Modify PEAR package.xml for above changes
# - Remove doctrine-dbal.php file
# - Remove md5sum from doctrine-dbal file since it was changed
sed -e '/doctrine-dbal.php/d' \
    -e '/doctrine-dbal/s/md5sum="[^"]*"\s*//' \
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
%{pear_phpdir}/Doctrine/DBAL
%{_bindir}/doctrine-dbal


%changelog
* Thu Oct  3 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.3.4-4
- backport for remi repo (drop php-mysqli dep)

* Wed Oct 02 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.4-4
- Removed php-mysqli require (BZ #1011996)

* Thu Jun 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.3.4-2
- backport for remi repo.

* Wed Jun 12 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.4-2
- Remove empty README

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.4-1
- Updated to 2.3.4
- Removed manual fix of Symfony package usage b/c fixed upstream
  (http://www.doctrine-project.org/jira/browse/DBAL-393)
- Made a single executable (removed doctrine-dbal.php)

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.0-1
- Updated to upstream version 2.3.0
- Added "%%global pear_metadir" and usage in %%install
- Added php-json require
- Updated %%description
- PEAR package.xml fixes in %%prep
- Changed RPM_BUILD_ROOT to %%{buildroot}

* Wed Jul 04 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.2-1
- Initial package
