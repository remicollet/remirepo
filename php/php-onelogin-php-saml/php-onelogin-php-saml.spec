%global gh_commit    17bfafe301bf21be1827c72f90e33a9c29d58553
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     onelogin
%global gh_project   php-saml
%global php_vendor   OneLogin

%global php_minver 5.3.2

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.9.1
Release:        3%{?dist}
Summary:        SAML support for PHP

License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{url}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Patch the test bootstrap for our autoload.php rather than adjust in %%check to simplify spec
Patch0:         php-saml-bootstrap-autoloader.patch

BuildArch:      noarch

BuildRequires:  php(language) >= %{php_minver}
BuildRequires:  %{_bindir}/phpab
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  php-mcrypt

# For %%check testing
BuildRequires:  php-composer(robrichards/xmlseclibs) >= 1.4.1
BuildRequires:  php-composer(robrichards/xmlseclibs) < 2.0.0

# From composer.json, "require": {
#        "php": ">=5.3.2"
Requires:       php(language) >= %{php_minver}
Requires: php-openssl
Requires: php-dom

# From manual unbundling, needs 1.4 contrary to the bundled 2.0 due to namespace issues
Requires:       php-composer(robrichards/xmlseclibs) >= 1.4.1
Requires:       php-composer(robrichards/xmlseclibs) < 2.0.0

# From phpci analysis
Requires: php-date
Requires: php-filter
Requires: php-hash
Requires: php-libxml
Requires: php-pcre
Requires: php-session
Requires: php-zlib

%if 0%{?rhel}
Requires: php-gettext
%else
Suggests: php-gettext
%endif

# Uses the mcrypt algorithms which is a suggests in xmlseclibs
Requires:       php-mcrypt

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
OneLogin's SAML PHP toolkit let you build a SP (Service Provider) over 
your PHP application and connect it to any IdP (Identity Provider).

Autoloader: %{_datadir}/php/%{php_vendor}/Saml2/autoload.php


%prep
%autosetup -n %{gh_project}-%{gh_commit} -p1


%build
rm -rf extlib
: Generate autoloader
%{_bindir}/phpab -n --output lib/Saml2/autoload.php lib
# Append the xmlseclibs requirement not in composer
cat >> lib/Saml2/autoload.php <<EOF
require_once "%{_datadir}/php/robrichards-xmlseclibs/autoload.php";
EOF


%install
mkdir -p   %{buildroot}%{_datadir}/php/%{php_vendor}
cp -pr lib/* %{buildroot}%{_datadir}/php/%{php_vendor}/


%check
: Run upstream phpunit tests in dev mode
%{_bindir}/php -c %{_docdir}/php/php.ini-development %{_bindir}/phpunit --verbose --debug --bootstrap tests/bootstrap.php --configuration tests/phpunit.xml
: Run upstream phpunit tests in system settings mode
%{_bindir}/php %{_bindir}/phpunit --verbose --debug --bootstrap tests/bootstrap.php --configuration tests/phpunit.xml





%files
%license LICENSE
%doc advanced_settings_example.php settings_example.php README.md composer.json CHANGELOG
%{_datadir}/php/%{php_vendor}


%changelog
* Mon Jul 25 2016 James Hogarth <james.hogarth@gmail.com> - 2.9.1-3
- Switch to a single autoloader after feedback

* Mon Jul 25 2016 James Hogarth <james.hogarth@gmail.com> - 2.9.1-2
- Update spec with comments from review

* Wed Jul 20 2016 James Hogarth <james.hogarth@gmail.com> - 2.9.1-1
- update to 2.9.1

* Wed Jul 13 2016 James Hogarth <james.hogarth@gmail.com> - 2.9.0-1
- initial package

