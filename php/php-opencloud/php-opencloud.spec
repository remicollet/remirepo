%global vendor OpenCloud
%global commit 7be280fde422651d0966c70b07f6477b37dd4270
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           php-opencloud
Version:        1.6.0
Release:        4%{?dist}
Summary:        PHP SDK for OpenStack/Rackspace APIs
Group:          Development/Libraries

License:        ASL 2.0
URL:            http://php-opencloud.com/
Source0:        https://github.com/rackspace/php-opencloud/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-phpunit-PHPUnit

Requires:       php-spl php-curl php-date php-fileinfo php-hash php-json
Requires:       php-pcre

BuildArch:      noarch

Obsoletes:      php-cloudfiles


%description
The PHP SDK should work with most OpenStack-based cloud deployments, though it
specifically targets the Rackspace public cloud. In general, whenever a
Rackspace deployment is substantially different than a pure OpenStack one, a
separate Rackspace subclass is provided so that you can still use the SDK with
a pure OpenStack instance (for example, see the OpenStack class (for OpenStack)
and the Rackspace subclass).

%package doc
Summary:       Documentation for OpenStack/Rackspace APIs PHP SDK
Group:         Development/Libraries

%description doc
%{summary}


%prep
%setup -q -n %{name}-%{commit}

# EOL encoding
sed -i 's/\r$//' docs/api/css/jquery.treeview.css


%build
# nothing to build


%install
rm -rf %{buildroot}
INSTALL_DIR=%{buildroot}%{_datadir}/php
mkdir -p $INSTALL_DIR
cp -a lib/%{vendor} $INSTALL_DIR


%clean
rm -rf %{buildroot}


%check
phpunit -d date.timezone=UTC .


%files
%defattr(-,root,root,-)
%doc LICENSE README.md TODO.md composer.json CONTRIBUTORS.md TODO.md
%{_datadir}/php/%{vendor}

%files doc
%doc samples docs


%changelog
* Thu Jan 30 2014 Remi Collet <rpms@famillecollet.com> - 1.6.0-4
- backport 1.6.0 for remi repo

* Thu Jan 30 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-4
- obsolete php-cloudfiles

* Sat Jan 25 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-3
- use commit revision in source url

* Fri Jan 03 2014 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-2
- move lib to psr-0 compliant location
- drop autoloader

* Tue Dec 31 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.6.0-1
- initial packaging

