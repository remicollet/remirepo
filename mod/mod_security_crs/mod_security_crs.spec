%global git_short 3f85c76

Summary: ModSecurity Rules
Name: mod_security_crs
Version: 2.2.6
Release: 2%{?dist}
License: ASL 2.0
URL: http://www.modsecurity.org/
Group: System Environment/Daemons

# Use the following command to generate the tarball:
# wget https://github.com/SpiderLabs/owasp-modsecurity-crs/tarball/GIT_SHORT

Source: SpiderLabs-owasp-modsecurity-crs-v%{version}-0-g%{git_short}.tar.gz
BuildArch: noarch
Requires: mod_security >= 2.6.5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0: %{name}-fix-incompatible-rules.patch

%description
This package provides the base rules for mod_security.

%package        extras
Summary:        Supplementary mod_security rules 
Group:          System Environment/Daemons
Requires:       %name = %version-%release

%description    extras
This package provides supplementary rules for mod_security.

%prep
%setup -q -n SpiderLabs-owasp-modsecurity-crs-%{git_short}
%patch0 -p1

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules

install -d %{buildroot}%{_prefix}/lib/modsecurity.d/base_rules

install -d %{buildroot}%{_prefix}/lib/modsecurity.d/optional_rules
install -d %{buildroot}%{_prefix}/lib/modsecurity.d/experimental_rules
install -d %{buildroot}%{_prefix}/lib/modsecurity.d/slr_rules

install -m0644 modsecurity_crs_10_setup.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/modsecurity_crs_10_config.conf
install -m0644 base_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/base_rules/
install -m0644 optional_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/optional_rules/
install -m0644 experimental_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/experimental_rules/
install -m0644 slr_rules/* %{buildroot}%{_prefix}/lib/modsecurity.d/slr_rules

# activate base_rules
for f in `ls %{buildroot}/%{_prefix}/lib/modsecurity.d/base_rules/` ; do 
    ln -s %{_prefix}/lib/modsecurity.d/base_rules/$f %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/$f; 
done

%clean
rm -rf %{buildroot}


%files
%doc CHANGELOG INSTALL LICENSE README.md
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/activated_rules/*
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/modsecurity_crs_10_config.conf
%{_prefix}/lib/modsecurity.d/base_rules

%files extras
%{_prefix}/lib/modsecurity.d/optional_rules
%{_prefix}/lib/modsecurity.d/experimental_rules
%{_prefix}/lib/modsecurity.d/slr_rules

%changelog
* Fri Oct  5 2012 Remi Collet <RPMS@FamilleCollet.com> 2.2.6-2
- backport for remi repo and httpd 2.4

* Mon Oct 01 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.6-2
- Add a patch to fix incompatible rules.
- Update to new git release

* Sat Sep 15 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.6-1
- Update to 2.2.6
- Update spec file since upstream moved to Github.

* Thu Sep 13 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.5-5
- Enable extra rules sub-package for EPEL.

* Tue Aug 28 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.5-4
- Fix spec for el5

* Tue Aug 28 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.5-3
- Add BuildRoot def for el5 compatibility

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Remi Collet <RPMS@FamilleCollet.com> 2.2.5-2
- backport for remi repo and httpd 2.4

* Fri Jun 22 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.5-1
- upgrade

* Wed Jun 20 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-3
- "extras" subpackage is not provided on RHEL

* Sat May 12 2012 Remi Collet <RPMS@FamilleCollet.com> 2.2.4-2
- rebuild for remi repo and httpd 2.4

* Wed May 03 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-2
- fix fedora-review issues (#816975)

* Thu Apr 19 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-1
- initial package


