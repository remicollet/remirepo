Name:           mod_auth_token
Version:        1.0.5
Release:        2%{?dist}
Summary:        Token based URI access module for Apache

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://code.google.com/p/mod-auth-token/
Source0:        http://mod-auth-token.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  httpd-devel automake libtool

%description
mod_auth_token allow you to generate URIS for a determined time window,
you can also limit them by IP. This is very useful to handle file
downloads, generated URIS can't be hot-linked (after it expires), also
it allows you to protect very large files that can't be piped trough a
script languages due to memory limitation.

%prep
%setup -q
rm -f configure
autoreconf -fi
automake
./configure

%build
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
apxs  -c mod_auth_token.c
install -m 755 .libs/%{name}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
# Drop empty NEWS-file.
rm -f $RPM_BUILD_ROOT/usr/share/doc/mod_auth_token-1.0.5/NEWS

%files
%{_libdir}/httpd/modules/*.so
%doc README LICENSE COPYING AUTHORS ChangeLog

%changelog
* Tue May 29 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 1.0.5-2
Apply package review patch from Lukáš Zapletal.

* Thu May 24 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 1.0.5-1
Don't use full path for apxs, since it's moved around in later fedoras.

* Thu May 24 2012 Jan-Frode Myklebust <janfrode@tanso.net> - 1.0.5
Initial build.

