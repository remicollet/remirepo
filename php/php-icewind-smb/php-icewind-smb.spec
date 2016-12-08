# remirepo/fedora spec file for php-icewind-smb
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github information
%global gh_commit    5e073449ee3b4b8142c4eeb265f27ce72ebe3932
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     icewind1991
%global gh_project   SMB
# Packagist information
%global pk_vendor    icewind
%global pk_name      smb
# Namespace information
%global ns_vendor    Icewind
%global ns_name      SMB
# Test suite requires a Samba server and configuration file
#   yum install samba
#   systemctl start smb
#   systemctl start nmb
#   useradd testsmb
#   install -o testsmb -m 755 -d /home/testsmb/test
#   smbpasswd -a testsmb
#   create php-icewind-smb-config.json using config.json from sources
%global with_tests   0%{?_with_tests:1}

Name:           php-%{pk_vendor}-%{pk_name}
Version:        1.1.2
Release:        1%{?dist}
Summary:        php wrapper for smbclient and libsmbclient-php

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{url}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php
%if %{with_tests}
# Can't be provided, contains credential
Source2:        %{name}-config.json
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
BuildRequires:  php(language) >= 5.4
BuildRequires:  php-composer(%{pk_vendor}/streams) >= 0.2
BuildRequires:  php-date
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-posix
# From composer.json, "require-dev": {
#		"satooshi/php-coveralls"  : "v1.0.0",
#		"phpunit/phpunit": "^4.8"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
BuildRequires:  php-composer(theseer/autoload)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)
%endif

# From composer.json, "require": {
#      "php": ">=5.4"
#      "icewind/streams": ">=0.2.0"
Requires:       php(language) >= 5.4
Requires:       php-composer(%{pk_vendor}/streams) >= 0.2
# From phpcompatinfo report for version 1.0.4
Requires:       %{_bindir}/smbclient
Requires:       php-date
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-posix
# Autoloader
Requires:       php-composer(fedora/autoloader)
%if 0%{?fedora} > 21
Recommends:     php-smbclient
%endif

Provides:       php-composer(%{pk_vendor}/%{pk_name}) = %{version}


%description
PHP wrapper for smbclient and libsmbclient-php

* Reuses a single smbclient instance for multiple requests
* Doesn't leak the password to the process list
* Simple 1-on-1 mapping of SMB commands
* A stream-based api to remove the need for temporary files
* Support for using libsmbclient directly trough libsmbclient-php

To use this library, you just have to add, in your project:
  require-once '%{_datadir}/php/%{ns_vendor}/%{ns_name}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
# Restore PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_name}



%if %{with_tests}
%check
cd tests
: Client configuration
cp %{SOURCE2} config.json

: Generate a simple autoloader for test suite
%{_bindir}/phpab --output bootstrap.php .
echo "require '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_name}/autoload.php';" >> bootstrap.php

: Run the test suite
%{_bindir}/phpunit

if which php70; then
   php70 %{_bindir}/phpunit --verbose
fi
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc composer.json
%doc *.md example.php
%{_datadir}/php/%{ns_vendor}/%{ns_name}


%changelog
* Thu Dec  8 2016 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- update to 1.1.2
- raise dependency on PHP 5.4
- add dependency on smbclient command
- switch to fedora/autoloader

* Tue Jun 14 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Thu Mar 17 2016 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8

* Thu Mar 17 2016 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7
- lower dependency on icewind/streams >= 0.2

* Thu Mar 17 2016 Remi Collet <remi@fedoraproject.org> - 1.0.6-1
- update to 1.0.6
- raise dependency on icewind/streams >= 0.3
- add optional dependency on php-smbclient

* Sun Feb 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5

* Sun Sep 20 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-2
- don't own /usr/share/php/Icewind (review #1259172)

* Wed Sep  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- initial package, version 1.0.4
