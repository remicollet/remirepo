%global modsuffix authnz_external
%global conffile %{modsuffix}.conf

Summary: An Apache module used for authentication
Name: mod_%{modsuffix}
Version: 3.2.6
Release: 1%{?dist}
License: ASL 1.0
Group: System Environment/Libraries
URL: http://code.google.com/p/mod-auth-external/
Source: http://mod-auth-external.googlecode.com/files/%{name}-%{version}.tar.gz
Source1: %{conffile}
Requires: pwauth, httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)
BuildRequires: httpd-devel

%description
Mod_Auth_External can be used to quickly construct secure, reliable
authentication systems.  It can also be mis-used to quickly open gaping
holes in your security.  Read the documentation, and use with extreme
caution.

%global modulesdir %{_libdir}/httpd/modules
%global confdir %{_sysconfdir}/httpd/conf


%prep
%setup -q


%build
apxs -c -I . %{name}.c


%install
mkdir -p %{buildroot}%{modulesdir} %{buildroot}%{confdir}.d
apxs -i -S LIBEXECDIR=%{buildroot}%{modulesdir} -n %{name} %{name}.la
install -p -m 644 -t %{buildroot}%{confdir}.d/ %{SOURCE1}

# in case we're on a 64-bit machine, otherwise a no-op
sed -i \
	-e 's@/usr/lib/@%{_libdir}/@' \
	%{buildroot}%{confdir}.d/%{conffile}


%files
%{modulesdir}/%{name}.so
%config(noreplace) %lang(en) %{confdir}.d/%{conffile}
%doc AUTHENTICATORS CHANGES README TODO UPGRADE


%changelog
* Fri May 05 2012 Philip Prindeville <philipp@fedoraproject.org> 3.2.6-1
- Initial version post packaging review.

* Tue Apr 17 2012 Philip Prindeville <philipp@fedoraproject.org> 3.2.6-0
- Initial RPM packaging.
