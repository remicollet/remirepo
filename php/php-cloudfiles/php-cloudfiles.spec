%global commit	930eb8d

Name:		php-cloudfiles
Version:		1.7.11
Release:		2%{?dist}
Summary:		PHP API for the Cloud Files storage system

License:		MIT
URL:		https://github.com/rackspace/php-cloudfiles
Source0:		https://github.com/rackspace/php-cloudfiles/tarball/v1.7.11/rackspace-%{name}-v%{version}-0-g%{commit}.tar.gz


Requires:	php-curl, php-date, php-fileinfo, php-hash, php-json
Requires:	php-mbstring, php-pcre, php-spl

BuildArch:	noarch

%description
PHP bindings for the Rackspace Cloud Files RESTful API. Features:

  * Enable your application to upload files programmatically
  * Enable Cloud Files CDN integration on any container for public distribution
  * Create Containers programmatically
  * Retrieve lists of containers and files


%package devel-doc
Summary:		Development documentation for %{name}

%description devel-doc
%{summary}


%prep
%setup -q -n rackspace-%{name}-%{commit}

# all lines should be \n terminated
find . -type f -exec sed -i -e 's/[\r\t ]*$//' '{}' ';'


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php/%{name}
install -pm 644 cloudfiles*.php %{buildroot}%{_datadir}/php/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}-devel-%{version}-%{release}
cp -a docs %{buildroot}%{_docdir}/%{name}-devel-%{version}-%{release}


%files
%doc README COPYING Changelog AUTHORS
%{_datadir}/php/%{name}


%files devel-doc
%{_docdir}/%{name}-devel-%{version}-%{release}


%changelog
* Tue Oct 02 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 1.7.11-2
- added all needed php extensions to Requires

* Sun Sep 23 2012 Gregor Tätzner <brummbq@fedoraproject.org> - 1.7.11-1
- Initial packaging

