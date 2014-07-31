#
# RPM spec file for php-doctrine-dbal
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Adam Williamson <awilliam@redhat.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      dbal
%global github_version   2.4.2
%global github_commit    fec965d330c958e175c39e61c3f6751955af32d0

%global composer_vendor  doctrine
%global composer_project dbal

# "php": ">=5.3.2"
%global php_min_ver             5.3.2
# "doctrine/common": "~2.4"
%global doctrine_common_min_ver 2.4
%global doctrine_common_max_ver 3.0
# "symfony/console": "~2.0"
%global symfony_console_min_ver 2.0
%global symfony_console_max_ver 3.0

Name:      php-%{composer_vendor}-%{composer_project}
Version:   %{github_version}
Release:   6%{?github_release}%{?dist}
Summary:   Doctrine Database Abstraction Layer (DBAL)

Group:     Development/Libraries
License:   MIT
URL:       http://www.doctrine-project.org/projects/dbal.html
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz
# From OwnCloud. Committed upstream as
# https://github.com/doctrine/dbal/commit/075c68b7518e27d46d7f700a1d42ebf43f6ebdfd
# but immediately reverted in
# https://github.com/doctrine/dbal/commit/894493b285c71a33e6ed29994ba415bad5e0a457
Patch0:    %{name}-2.4.2-primary_index.patch
# From upstream master (2.5), not yet backported to 2.4 upstream. Required for
# OwnCloud (pgsql-backed OC 6.x upgrades to 7.x fail without it.) Rediffed
# https://github.com/doctrine/dbal/commit/f8c1d77efa988974026189bf8214ef0fecaf1522
Patch1:    f8c1d77efa988974026189bf8214ef0fecaf1522.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  php(language)                 >= %{php_min_ver}
Requires:  php-composer(doctrine/common) >= %{doctrine_common_min_ver}
Requires:  php-composer(doctrine/common) <  %{doctrine_common_max_ver}
Requires:  php-symfony-console           >= %{symfony_console_min_ver}
Requires:  php-symfony-console           <  %{symfony_console_max_ver}
# phpcompatinfo (computed from v2.4.2)
Requires:  php-date
Requires:  php-json
Requires:  php-pcre
Requires:  php-pdo
Requires:  php-spl

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:  php-pear(pear.doctrine-project.org/DoctrineDBAL) = %{version}
# Rename
Obsoletes: php-doctrine-DoctrineDBAL < %{version}
Provides:  php-doctrine-DoctrineDBAL = %{version}

%description
The Doctrine database abstraction & access layer (DBAL) offers a lightweight
and thin runtime layer around a PDO-like API and a lot of additional, horizontal
features like database schema introspection and manipulation through an OO API.

The fact that the Doctrine DBAL abstracts the concrete PDO API away through the
use of interfaces that closely resemble the existing PDO API makes it possible
to implement custom drivers that may use existing native or self-made APIs. For
example, the DBAL ships with a driver for Oracle databases that uses the oci8
extension under the hood.


%prep
%setup -qn %{github_name}-%{github_commit}
%patch0 -p3 -b .primary_index
%patch1 -p1 -b .escape_column

# Make a single executable
echo '#!%{_bindir}/php' > bin/doctrine-dbal
sed 's#Doctrine/Common/ClassLoader.php#%{_datadir}/php/Doctrine/Common/ClassLoader.php#' \
    bin/doctrine-dbal.php >> bin/doctrine-dbal

# Remove empty file
rm -f lib/Doctrine/DBAL/README.markdown

# Remove executable bits
chmod a-x \
    lib/Doctrine/DBAL/Types/JsonArrayType.php \
    lib/Doctrine/DBAL/Types/SimpleArrayType.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/Doctrine %{buildroot}/%{_datadir}/php/

mkdir -p %{buildroot}/%{_bindir}
install -pm 0755 bin/doctrine-dbal %{buildroot}/%{_bindir}/


%check
# No upstream tests provided in source


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md UPGRADE composer.json
%{_datadir}/php/Doctrine/DBAL
%{_bindir}/doctrine-dbal


%changelog
* Thu Jul 31 2014 Remi Collet <rpms@famillecollet.com> 2.4.2-6
- backport for remi repo
- fix license handling

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-6
- really apply the patch

* Tue Jul 29 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-5
- backport another OwnCloud-related pgsql fix from upstream master

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.2-4
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Updated Doctrine dependencies to use php-composer virtual provides

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 2.4.2-2
- backport for remi repo

* Tue Jan 07 2014 Adam Williamson <awilliam@redhat.com> - 2.4.2-2
- primary_index: one OwnCloud patch still isn't in upstream

* Sat Jan 04 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.2-1
- Updated to 2.4.2
- Conditional %%{?dist}

* Tue Dec 31 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-2.20131231gitd08b11c
- Updated to latest snapshot
- Removed patches (pulled into latest snapshot)

* Sun Dec 29 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.4.1-1
- Initial package
