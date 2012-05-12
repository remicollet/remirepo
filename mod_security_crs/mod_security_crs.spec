Summary: ModSecurity Rules
Name: mod_security_crs
Version: 2.2.4
Release: 2%{?dist}
License: ASL 2.0
URL: http://www.modsecurity.org/
Group: System Environment/Daemons
Source: https://sourceforge.net/projects/mod-security/files/modsecurity-crs/0-CURRENT/modsecurity-crs_%{version}.tar.gz
BuildArch: noarch
Requires: mod_security >= 2.6.5

%description
This package provides the base rules for mod_security.

%package        extras
Summary:        Supplementary mod_security rules 
Group:          System Environment/Daemons
Requires:       %name = %version-%release

%description    extras
This package provides supplementary rules for mod_security.

%prep
%setup -q -n modsecurity-crs_%{version}

%build

%install
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules

install -d %{buildroot}%{_prefix}/lib/modsecurity.d/base_rules
install -d %{buildroot}%{_prefix}/lib/modsecurity.d/optional_rules
install -d %{buildroot}%{_prefix}/lib/modsecurity.d/experimental_rules
install -d %{buildroot}%{_prefix}/lib/modsecurity.d/slr_rules

install -m0644 modsecurity_crs_10_config.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/modsecurity_crs_10_config.conf
install -m0644 base_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/base_rules/
install -m0644 optional_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/optional_rules/
install -m0644 experimental_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/experimental_rules/
install -m0644 slr_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/slr_rules

# activate base_rules
for f in `ls %{buildroot}/%{_prefix}/lib/modsecurity.d/base_rules/` ; do 
    ln -s %{_prefix}/lib/modsecurity.d/base_rules/$f %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/$f; 
done


%files
%doc CHANGELOG INSTALL LICENSE README
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/activated_rules/*
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/modsecurity_crs_10_config.conf
%{_prefix}/lib/modsecurity.d/base_rules

%files extras
%{_prefix}/lib/modsecurity.d/optional_rules
%{_prefix}/lib/modsecurity.d/experimental_rules
%{_prefix}/lib/modsecurity.d/slr_rules

%changelog
* Sat May 12 2012 Remi Collet <RPMS@FamilleCollet.com> 2.2.4-2
- rebuild for remi repo and httpd 2.4

* Wed May 03 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-2
- fix fedora-review issues (#816975)

* Thu Apr 19 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-1
- initial package


