%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}

%global release_suffix .Final

Summary:    Apache HTTP load balancer
Name:       mod_cluster
Version:    1.1.1
Release:    4%{?dist}
License:    LGPLv2
URL:        http://jboss.org/mod_cluster
Group:      System Environment/Daemons
Source:     http://downloads.jboss.org/%{name}/%{version}%{release_suffix}/%{name}-%{version}%{release_suffix}-src-ssl.tar.gz
Source1:    mod_cluster.conf
Source2:    README.fedora
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:     mod_cluster-1.1.1-lesswarnings.patch

Requires:      httpd >= 2.2.8
Requires:      httpd-mmn = %{_httpd_mmn}
BuildRequires: httpd-devel >= 2.2.8
BuildRequires: autoconf
# BuildRequires: maven3 # Required to build docs

%description
Mod_cluster is an httpd-based load balancer. Like mod_jk and mod_proxy,
mod_cluster uses a communication channel to forward requests from httpd to one
of a set of application server nodes. Unlike mod_jk and mod_proxy, mod_cluster
leverages an additional connection between the application server nodes and
httpd. The application server nodes use this connection to transmit server-side
load balance factors and lifecycle events back to httpd via a custom set of
HTTP methods, affectionately called the Mod-Cluster Management Protocol (MCMP).
This additional feedback channel allows mod_cluster to offer a level of
intelligence and granularity not found in other load balancing solutions.

%prep
%setup -q -n %{name}-%{version}%{release_suffix}-src-ssl

# Remove unecessary directories
find srclib -mindepth 1 -maxdepth 1 ! -name mod_cluster -print0|xargs -0 -r rm -rf

# Remove a lot of compile-time warnings
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS

module_dirs=( advertise mod_manager mod_proxy_cluster mod_slotmem )

for dir in ${module_dirs[@]} ; do
    pushd srclib/%{name}/native/${dir}
        sh buildconf
        ./configure --libdir=%{_libdir} --with-apxs=%{_httpd_apxs}
        make %{?_smp_mflags}
    popd
done

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/httpd/modules

module_dirs=( advertise mod_manager mod_proxy_cluster mod_slotmem )

for dir in ${module_dirs[@]} ; do
    pushd srclib/%{name}/native/${dir}
        cp ./*.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
    popd
done

install -d -m 755 $RPM_BUILD_ROOT/etc/httpd/conf.d
cp -a %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/

install -m 0644 %{SOURCE2} README

cp -a srclib/mod_cluster/lgpl.txt .

%clean
rm -Rf $RPM_BUILD_ROOT

%files

# There is a docs/ directory which contains documentation in docbook
# format. Unfortunately Maven 3 is needed to build it.

%defattr(-,root,root)
%doc README
%doc lgpl.txt
%{_libdir}/httpd/modules/mod_advertise.so
%{_libdir}/httpd/modules/mod_manager.so
%{_libdir}/httpd/modules/mod_proxy_cluster.so
%{_libdir}/httpd/modules/mod_slotmem.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%changelog
* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-4
- rebuild for remi repo and httpd 2.4

* Tue Mar 27 2012 Marek Goldmann <mgoldman@redhat.com> - 1.1.1-4
- Require httpd-mmn RHBZ#803068

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 11 2011 Marek Goldmann <mgoldman@redhat.com> - 1.1.1-2
- Another round of cleanup in spec file
- Patch that disables compilation-time warnings

* Thu Mar 10 2011 Marek Goldmann <mgoldman@redhat.com> - 1.1.1-1
- Upstream release 1.1.1
- Cleanup in spec file

* Fri Nov 12 2010 Marek Goldmann <mgoldman@redhat.com> - 1.1.0-1
- Initial release

