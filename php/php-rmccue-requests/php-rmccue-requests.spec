Name:       php-rmccue-requests
Version:    1.7.0
Release:    2%{?dist}
BuildArch:  noarch

License:    ISC and BSD
Summary:    Requests for PHP is a humble HTTP request library
URL:        https://github.com/rmccue/Requests
Source0:    %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# This is only needed to run the test suite.
Source1:    https://github.com/RequestsPHP/test-server/archive/26334a7583c96ae1f966a5d88af9aafaf279f948/requests-tests-26334a75.tar.gz

BuildRequires: php-composer(fedora/autoloader)
BuildRequires: php-fedora-autoloader-devel
BuildRequires: php-zip
BuildRequires: phpunit 
BuildRequires: procps-ng

Requires:   php(language) >= 5.5.0
Requires:   php-composer(fedora/autoloader)
Requires:   php-curl
Requires:   php-date
Requires:   php-json
Requires:   php-openssl
Requires:   php-pcre
Requires:   php-spl
Requires:   php-zlib

Provides:   php-composer(rmccue/requests) = %{version}


%description
Requests for PHP simplifies how you interact with other sites and takes
away all your worries.

Requests is a HTTP library written in PHP, for human beings. It is
roughly based on the API from the excellent Requests Python library.
Requests is ISC Licensed (similar to the new BSD license) and has no
dependencies, except for PHP 5.2+.

Despite PHP's use as a language for the web, its tools for sending HTTP
requests are severely lacking. cURL has an interesting API, to say the
least, and you can't always rely on it being available. Sockets provide
only low level access, and require you to build most of the HTTP
response parsing yourself.

We all have better things to do. That's why Requests was born.


%prep
%autosetup -n Requests-%{version}

tar xvf %{S:1}

# Remove the bundled CA list and use Fedora's
rm library/Requests/Transport/cacert.pem
ln -s %{_sysconfdir}/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
    library/Requests/Transport/cacert.pem


%build
%{_bindir}/phpab --format fedora --output library/autoload.php library


%install
install -d -p -m 0755 %{buildroot}/%{_datadir}/php
install -d -p -m 0755 %{buildroot}/%{_datadir}/php/rmccue
install -d -p -m 0755 %{buildroot}/%{_datadir}/php/rmccue/Requests

cp -ar library/* %{buildroot}/%{_datadir}/php/rmccue/Requests


%check
sed -i "s:include.*:require('%{buildroot}/%{_datadir}/php/rmccue/Requests/autoload.php');:" \
    tests/bootstrap.php

if [ "$(netstat -ln | grep 8080)" != "" ]
then
    kill php
fi

%{_bindir}/php -S 127.0.0.1:8080 \
    test-server-26334a7583c96ae1f966a5d88af9aafaf279f948/bin/serve.php &
PHPPID=$!

pushd tests
# The request test server doesn't run over TLS so we skip HTTPS tests. The other tests fail if they
# can't resolve domain names, so they are skipped as well.
REQUESTS_TEST_HOST="127.0.0.1:8080" phpunit --bootstrap bootstrap.php \
    --filter \
    ^\(\(?!\(testHTTPS\|testAlternateNameSupport\|testSNISupport\|testAlternatePort\)\).\)*$ || \
    (kill $PHPPID && exit 1)
popd

kill $PHPPID


%files
%license LICENSE
%doc CHANGELOG.md
%doc composer.json
%doc docs
%doc examples
%doc README.md
%{_datadir}/php/rmccue


%changelog
* Sun Mar 05 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.7.0-2
- Change license tag to ISC and BSD.
- Use a better method for killing the test server.

* Sun Feb 19 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.7.0-1
- Initial release.
