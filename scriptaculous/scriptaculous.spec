Name:         scriptaculous
Version:      1.9.0
Release:      1%{?dist}
Summary:      JavaScript library
Group:        Applications/Internet
License:      MIT
URL:          http://script.aculo.us/

# We cannot use the archive tarball from github
# as we don't have yet requirement for build (rake, sprockets)
Source0:      http://script.aculo.us/dist/%{name}-js-%{version}.zip
Source1:      %{name}.conf

BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:    noarch

Requires:     prototype


%description
script.aculo.us provides you with easy-to-use, 
cross-browser user interface JavaScript libraries
to make your web sites and web applications fly.

%package httpd
Summary:       Apache configuration for %{name}
Group:         Applications/Internet
Requires:      %{name} = %{version}-%{release}
Requires:      httpd

%description   httpd
This package provides the Apache configuration for
applications using an Alias to scriptaculous library.


%prep
%setup -q -n %{name}-js-%{version}

# fix encoding
iconv -f iso-8859-1 -t utf8 CHANGELOG >CHANGELOG.new
touch -r CHANGELOG CHANGELOG.new
mv CHANGELOG.new CHANGELOG


%build
# Nothing to build


%install
rm -rf %{buildroot}

# JavaScript
install -m 0755 -d %{buildroot}%{_datadir}/%{name}
install -m 0644 -p src/*.js %{buildroot}%{_datadir}/%{name}

# Apache
install -m 0755 -d %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGELOG README.rdoc MIT-LICENSE
%{_datadir}/%{name}


%files httpd
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf


%changelog
* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- initial package
