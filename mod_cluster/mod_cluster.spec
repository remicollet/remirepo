%if 0%{?fedora} >= 17
%global with_java 1
%else
%global with_java 0
%endif

%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_mmn:        %{expand: %%global _httpd_mmn        %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}

%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Summary:    Apache HTTP load balancer
Name:       mod_cluster
Version:    1.2.1
Release:    1%{?dist}
License:    LGPLv2
URL:        http://jboss.org/mod_cluster
Group:      System Environment/Daemons

# svn export http://anonsvn.jboss.org/repos/mod_cluster/tags/1.2.1.Final/ mod_cluster-1.2.1.Final
# tar cafJ mod_cluster-1.2.1.Final.tar.xz mod_cluster-1.2.1.Final
Source:     mod_cluster-%{namedversion}.tar.xz

Source1:    mod_cluster.conf
Source2:    README.fedora

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:     mod_cluster-%{namedversion}-pom.patch

Requires:      httpd >= 2.2.8
Requires:      httpd-mmn = %{_httpd_mmn}

%if %{with_java}
BuildRequires: maven
BuildRequires: maven-enforcer-plugin
BuildRequires: jboss-parent
BuildRequires: jpackage-utils
BuildRequires: java-devel
BuildRequires: jcip-annotations
BuildRequires: jboss-logging
BuildRequires: jboss-servlet-3.0-api
BuildRequires: jboss-web
%endif
BuildRequires: httpd-devel >= 2.2.8
BuildRequires: autoconf
BuildRequires: make
BuildRequires: gcc
BuildRequires: tomcat-lib

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

%if %{with_java}
%package java
Summary:          Java bindings for %{name}
Group:            Development/Libraries
Requires:         jpackage-utils
Requires:         jcip-annotations
Requires:         jboss-logging
Requires:         jboss-servlet-3.0-api

%description java
This package contains Java part of %{name}.

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.
%endif

%prep
%setup -q -n mod_cluster-%{namedversion}
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS

module_dirs=( advertise mod_manager mod_proxy_cluster mod_slotmem )

for dir in ${module_dirs[@]} ; do
    pushd native/${dir}
        sh buildconf
        ./configure --libdir=%{_libdir} --with-apxs=%{_httpd_apxs}
        make %{?_smp_mflags}
    popd
done

%if %{with_java}
# Build the AS7 required libs
# Tests skipped because of lack of mockito library
mvn-rpmbuild -Dmaven.test.skip=true -P AS7 install javadoc:aggregate
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -d -m 755 $RPM_BUILD_ROOT/etc/httpd/conf.d
%if %{with_java}
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
%endif

module_dirs=( advertise mod_manager mod_proxy_cluster mod_slotmem )

for dir in ${module_dirs[@]} ; do
    pushd native/${dir}
        cp ./*.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules
    popd
done

cp -a %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/

install -m 0644 %{SOURCE2} README

%if %{with_java}
# JAR
cp -p core/target/mod_cluster-core-%{namedversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/core.jar
cp -p container/catalina/target/mod_cluster-container-catalina-%{namedversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/container-catalina.jar
cp -p container/jbossweb/target/mod_cluster-container-jbossweb-%{namedversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/container-jbossweb.jar
cp -p container-spi/target/mod_cluster-container-spi-%{namedversion}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/container-spi.jar

# APIDOCS
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# POM
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-parent.pom
install -pm 644 core/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-core.pom
install -pm 644 container-spi/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-container-spi.pom
install -pm 644 container/catalina/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-container-catalina.pom
install -pm 644 container/jbossweb/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-container-jbossweb.pom

# DEPMAP
%add_maven_depmap JPP.%{name}-parent.pom
%add_maven_depmap JPP.%{name}-core.pom %{name}/core.jar
%add_maven_depmap JPP.%{name}-container-spi.pom %{name}/container-spi.jar
%add_maven_depmap JPP.%{name}-container-jbossweb.pom %{name}/container-jbossweb.jar
%add_maven_depmap JPP.%{name}-container-catalina.pom %{name}/container-catalina.jar
%endif


%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%doc lgpl.txt
%{_libdir}/httpd/modules/mod_advertise.so
%{_libdir}/httpd/modules/mod_manager.so
%{_libdir}/httpd/modules/mod_proxy_cluster.so
%{_libdir}/httpd/modules/mod_slotmem.so
%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf

%if %{with_java}
%files javadoc
%{_javadocdir}/%{name}
%doc lgpl.txt

%files java
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*
%doc lgpl.txt
%endif


%changelog
* Sat May 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repo and httpd 2.4

* Mon May 07 2012 Marek Goldmann <mgoldman@redhat.com> - 1.2.1-1
- Upstream release 1.2.1.Final
- Port to httpd 2.4, RHBZ#813871

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-4
- rebuild for remi repo and httpd 2.4

* Wed Mar 28 2012 Marek Goldmann <mgoldman@redhat.com> - 1.2.0-1
- Upstream release 1.2.0.Final
- Add java subpackage with AS7 required jars

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

