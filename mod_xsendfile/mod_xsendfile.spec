Summary:	Apache module to send files efficiently
Name:		mod_xsendfile
Version:	0.12
Release:	5%{?dist}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		https://tn123.org/%{name}/
Source0:	https://tn123.org/%{name}/%{name}-%{version}.tar.bz2
Source1:	xsendfile.conf
BuildRequires:	httpd-devel
Requires:       httpd-mmn = %{_httpd_mmn}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
%{name} is a small Apache2 module that processes X-SENDFILE headers
registered by the original output handler.

If it encounters the presence of such header it will discard all output and
send the file specified by that header instead using Apache internals
including all optimizations like caching-headers and sendfile or mmap if
configured.

It is useful for processing script-output of e.g. php, perl or any cgi.


%prep
%setup -q


%build
%{_httpd_apxs} -c %{name}.c


%install
rm -rf $%{buildroot}
mkdir -p %{buildroot}/%{_httpd_moddir}
%{_httpd_apxs} -i -S LIBEXECDIR=%{buildroot}/%{_httpd_moddir} -n %{name} %{name}.la
mkdir -p %{buildroot}/%{_httpd_modconfdir}
cp -p %SOURCE1 %{buildroot}/%{_httpd_modconfdir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc docs/*
%config(noreplace) %{_httpd_modconfdir}/xsendfile.conf
%{_httpd_moddir}/%{name}.so


%changelog
* Wed Mar 28 2012 Remi Collet <RPMS@FamilleCollet.com> 0.12-5
- rebuild for remi repo and httpd 2.4

* Tue Mar 27 2012 Orion Poplawski <orion@cora.nwra.com> 0.12-5
- Rebuild for httpd 2.4, update for new module guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr 25 2011 Orion Poplawski <orion@cora.nwra.com> 0.12-3
- Fix license tag

* Wed Dec 1 2010 Orion Poplawski <orion@cora.nwra.com> 0.12-2
- Upstream fixed tar ball packaging

* Mon Oct 25 2010 Orion Poplawski <orion@cora.nwra.com> 0.12-1
- Initial package
