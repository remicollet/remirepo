# remirepo spec file for php-phpoffice-phpexcel, from
#
# Fedora spec file for php-phpoffice-phpexcel
#
# Copyright (c) 2015-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     PHPOffice
%global github_name      PHPExcel
%global github_version   1.8.1
%global github_commit    372c7cbb695a6f6f1e62649381aeaa37e7e70b32

%global composer_vendor  phpoffice
%global composer_project phpexcel

# php": ">=5.2.0"
%global php_min_ver      5.2.0

# Build using "--without tests" to disable tests
%global with_tests       0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       3%{?github_release}%{dist}
Summary:       A pure PHP library for reading and writing spreadsheet files

Group:         Development/Libraries
# Everything is LGPLv2 except for PHPExcel/Shared/OLE* which are PHP
# See:
#     * https://github.com/PHPOffice/PHPExcel/issues/364
#     * https://github.com/PHPOffice/PHPExcel/issues/407
License:       LGPLv2 and PHP
URL:           http://phpoffice.github.io/phpexcel_features.html
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

# Fix test for PHP < 5.4
# https://github.com/PHPOffice/PHPExcel/pull/695
# NOTE: Custom patch for 1.8.1 because pull request patch does not apply cleanly
Patch0:        %{name}-pr695-1-8-1-custom.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
BuildRequires: php-composer(phpunit/phpunit)
# composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-gd
BuildRequires: php-mbstring
BuildRequires: php-pecl(zip)
BuildRequires: php-xml
BuildRequires: php-xmlwriter
# phpcompatinfo (computed from version 1.8.1)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-iconv
BuildRequires: php-libxml
BuildRequires: php-pcre
BuildRequires: php-pecl(igbinary)
BuildRequires: php-posix
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
%if 0%{?rhel} != 5
BuildRequires: php-sqlite3
%endif
BuildRequires: php-xmlreader
BuildRequires: php-zlib
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-mbstring
Requires:      php-xml
Requires:      php-xmlwriter
# composer.json (optional)
Requires:      php-gd
Requires:      php-pecl(zip)
# phpcompatinfo (computed from version 1.8.1)
Requires:      php-ctype
Requires:      php-date
Requires:      php-dom
Requires:      php-iconv
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-pecl(igbinary)
Requires:      php-posix
Requires:      php-reflection
Requires:      php-simplexml
Requires:      php-spl
%if 0%{?rhel} != 5
Requires:      php-sqlite3
%endif
Requires:      php-xmlreader
Requires:      php-zlib
# Unbundled
Requires:      php-pclzip

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Bundled
#
# https://pear.php.net/package/OLE
# See:
#     * https://github.com/PHPOffice/PHPExcel/issues/364
#     * https://github.com/PHPOffice/PHPExcel/issues/407
Provides:      bundled(php-pear-OLE)

%description
Project providing a set of classes for the PHP programming language, which
allow you to write to and read from different spreadsheet file formats, like
Excel (BIFF) .xls, Excel 2007 (OfficeOpenXML) .xlsx, CSV, Libre/OpenOffice
Calc .ods, Gnumeric, PDF, HTML, ... This project is built around Microsoft's
OpenXML standard and PHP.

Optional:
* APC (php-pecl-apc)
* Memcache (php-pecl-memcache)


%prep
%setup -qn %{github_name}-%{github_commit}

%patch0 -p0

: Fix wrong-file-end-of-line-encoding
find Examples -type f -exec sed -i 's/\r$//' {} \;

: Remove unneeded files
find . -name '\.git*' | xargs rm -f

: Remove bundled pclzip
rm -rf Classes/PHPExcel/Shared/PCLZip




%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp Classes/* %{buildroot}%{phpdir}/

: Symlink to system pclzip
ln -s %{phpdir}/pclzip %{buildroot}%{phpdir}/PHPExcel/Shared/PCLZip

: Locales
for LOCALE in %{buildroot}%{phpdir}/PHPExcel/locale/*
do
    LOCALE_LANG=`basename $LOCALE`
    echo "%%lang(${LOCALE_LANG}) $LOCALE"
done | sed 's#%{buildroot}##' | tee %{name}.lang

: Autoloader
ln -s ../PHPExcel.php %{buildroot}%{phpdir}/PHPExcel/autoload.php


%check
%if %{with_tests}
cd unitTests

: Remove tests known to fail
rm -f \
    Classes/PHPExcel/Calculation/DateTimeTest.php \
    Classes/PHPExcel/Calculation/EngineeringTest.php \
    Classes/PHPExcel/Calculation/FinancialTest.php \
    Classes/PHPExcel/Calculation/LookupRefTest.php \
    Classes/PHPExcel/Calculation/MathTrigTest.php \
    Classes/PHPExcel/Calculation/MathTrigTest.php \
    Classes/PHPExcel/Calculation/TextDataTest.php \
    Classes/PHPExcel/Shared/DateTest.php \
    Classes/PHPExcel/Shared/PasswordHasherTest.php \
    Classes/PHPExcel/Shared/StringTest.php \
    Classes/PHPExcel/Style/NumberFormatTest.php testFormatValueWithMask \
    Classes/PHPExcel/Worksheet/AutoFilter/Column/RuleTest.php \
    Classes/PHPExcel/Worksheet/CellCollectionTest.php \
    Classes/PHPExcel/Worksheet/ColumnIteratorTest.php \
    Classes/PHPExcel/Worksheet/RowIteratorTest.php

%{_bindir}/phpunit --verbose
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license license.md
%doc Examples
%doc changelog.txt
%doc composer.json
     %{phpdir}/PHPExcel.php
%dir %{phpdir}/PHPExcel
%dir %{phpdir}/PHPExcel/locale
     %{phpdir}/PHPExcel/*.php
     %{phpdir}/PHPExcel/CachedObjectStorage
     %{phpdir}/PHPExcel/CalcEngine
     %{phpdir}/PHPExcel/Calculation
     %{phpdir}/PHPExcel/Cell
     %{phpdir}/PHPExcel/Chart
     %{phpdir}/PHPExcel/Helper
     %{phpdir}/PHPExcel/Reader
     %{phpdir}/PHPExcel/RichText
     %{phpdir}/PHPExcel/Shared
     %{phpdir}/PHPExcel/Style
     %{phpdir}/PHPExcel/Worksheet
     %{phpdir}/PHPExcel/Writer


%changelog
* Mon May 30 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.8.1-3
- Skip additional tests known to fail
- See https://github.com/PHPOffice/PHPExcel/issues/910

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 1.8.1-1
- backport for remi repo, add EL-5 stuff

* Sun Oct 11 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.8.1-1
- Updated to 1.8.1
- Spec cleanup

* Thu May 29 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.8.0-1.20140526git4ab61ad
- Initial package
