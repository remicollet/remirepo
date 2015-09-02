# remirepo spec/Fedora file for php-icewind-smb
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github information
%global gh_commit    9277bd20262a01b38a33cc7356e98055f2262d32
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
#   service start smb
#   service start nmb
#   useradd testsmb
#   install -o testsmb -m 755 -d /home/testsmb/test
#   smbpasswd -a testsmb
#   create php-icewind-smb-config.json using config.json from sources
%global with_tests   0%{?_with_tests:1}

Name:           php-%{pk_vendor}-%{pk_name}
Version:        1.0.4
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
BuildRequires:  php(language) >= 5.3
BuildRequires:  php-composer(%{pk_vendor}/streams) >= 0.2
BuildRequires:  php-date
BuildRequires:  php-mbstring
BuildRequires:  php-pcre
BuildRequires:  php-posix
# From composer.json, "require-dev": {
#       "satooshi/php-coveralls": "dev-master"
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(theseer/autoload)
# Autoloader
BuildRequires:  php-composer(symfony/class-loader)
%endif

# From composer.json, "require": {
#      "php": ">=5.3"
#      "icewind/streams": "0.2.*"
Requires:       php(language) >= 5.3
Requires:       php-composer(%{pk_vendor}/streams) >= 0.2
Requires:       php-composer(%{pk_vendor}/streams) <  0.3
# From phpcompatinfo report for version 1.0.4
Requires:       php-date
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-posix
# Autoloader
Requires:       php-composer(symfony/class-loader)

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
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc composer.json
%doc *.md example.php
%dir %{_datadir}/php/%{ns_vendor}
     %{_datadir}/php/%{ns_vendor}/%{ns_name}


%changelog
* Wed Sep  2 2015 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- initial package, version 1.0.4