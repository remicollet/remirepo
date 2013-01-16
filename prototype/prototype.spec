Name:         prototype
Version:      1.7.1.0
Release:      1%{?dist}
Summary:      JavaScript framework
Group:        Applications/Internet
License:      MIT
URL:          http://www.prototypejs.org/

# We cannot use the archive tarball from github
# as we don't have yet requirement for build (rake, sprockets)
Source0:      https://ajax.googleapis.com/ajax/libs/prototype/%{version}/prototype.js
Source1:      https://raw.github.com/sstephenson/prototype/master/LICENSE
Source2:      prototype.conf

BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:    noarch


%description
Prototype is a JavaScript framework that aims to ease development of dynamic
web applications. It offers a familiar class-style OO framework, extensive
Ajax support, higher-order programming constructs, and easy DOM manipulation.

%package httpd
Summary:       Apache configuration for %{name}
Group:         Applications/Internet
Requires:      %{name} = %{version}-%{release}
Requires:      httpd

%description   httpd
This package provides the Apache configuration for
applications using an Alias to prototype library.


%prep
%setup -qcT

cp -p %{SOURCE1} LICENSE


%build
# Nothing to build


%install
rm -rf %{buildroot}

# JavaScript
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -p %{SOURCE0} %{buildroot}%{_datadir}/%{name}/%{name}.js

# Apache
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE
%{_datadir}/%{name}


%files httpd
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf


%changelog
* Wed Jan 16 2013 Remi Collet <remi@fedoraproject.org> - 1.7.1.0-1
- initial package
