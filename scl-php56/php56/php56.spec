%global scl_name_base    php
%global scl_name_version 56
%global scl              %{scl_name_base}%{scl_name_version}
%global macrosdir        %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_root_sysconfdir}/rpm; echo $d)
%global install_scl      1
%if 0%{?fedora} >= 26
%global rh_layout        1
%endif
%if 0%{?fedora} >= 20
# Requires scl-utils v2 for SCL integration
%global with_modules     1
%else
# Works with file installed in /usr/share/Modules/modulefiles/
%global with_modules     0
%endif
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs PHP 5.6
Name:          %scl_name
Version:       2.2
Release:       1%{?dist}
Group:         Development/Languages
License:       GPLv2+

Source0:       macros-build
Source1:       README
Source2:       LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes
BuildRequires: environment-modules

Requires:      %{?scl_prefix}php-common%{?_isa} >= 5.6.30
Requires:      %{?scl_prefix}php-cli%{?_isa}
Requires:      %{?scl_prefix}php-pear           >= 1:1.10.3
Requires:      %{?scl_name}-runtime%{?_isa}      = %{version}-%{release}

%description
This is the main package for %scl Software Collection,
that install PHP 5.6 language.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils
Requires:  environment-modules
Requires(post): %{_root_sbindir}/semanage
Requires(post): %{_root_sbindir}/selinuxenabled
Provides:  %{?scl_name}-runtime(%{scl_vendor})
Provides:  %{?scl_name}-runtime(%{scl_vendor})%{?_isa}

%description runtime
Package shipping essential scripts to work with %scl Software Collection.


%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build
Requires:  %{?scl_name}-runtime%{?_isa} = %{version}-%{release}

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages
Requires:  %{?scl_name}-runtime%{?_isa} = %{version}-%{release}

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# Broken: /usr/share/Modules/bin/createmodule.sh enable | tee envmod
# See https://bugzilla.redhat.com/show_bug.cgi?id=1197321
cat << EOF | tee envmod
#%%Module1.0
prepend-path    X_SCLS              %{scl}
prepend-path    PATH                %{_bindir}:%{_sbindir}
prepend-path    LD_LIBRARY_PATH     %{_libdir}
prepend-path    MANPATH             %{_mandir}
prepend-path    PKG_CONFIG_PATH     %{_libdir}/pkgconfig
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_name_base}         %{scl}
%%scl_prefix_%{scl_name_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .

: prefix in %{_prefix}
: config in %{_sysconfdir}
: data in %{_localstatedir}


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
%if %{with_modules}
install -D -m 644 envmod %{buildroot}%{_scl_scripts}/%{scl_name}
%else
install -D -m 644 envmod %{buildroot}%{_root_datadir}/Modules/modulefiles/%{scl_name}
%endif
install -D -m 644 scldev %{buildroot}%{macrosdir}/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

install -d -m 755 %{buildroot}%{_datadir}/licenses
install -d -m 755 %{buildroot}%{_datadir}/doc/pecl
install -d -m 755 %{buildroot}%{_datadir}/tests/pecl
install -d -m 755 %{buildroot}%{_localstatedir}/lib/pear/pkgxml

%scl_install

# Add the scl_package_override macro
sed -e 's/@SCL@/%{scl}/g' %{SOURCE0} \
  | tee -a %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

# Move in correct location, if needed
if [ "%{_root_sysconfdir}/rpm" != "%{macrosdir}" ]; then
  mv  %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config \
      %{buildroot}%{macrosdir}/macros.%{scl}-config
fi


%post runtime
# Simple copy of context from system root to SCL root.
semanage fcontext -a -e /                      %{?_scl_root}     &>/dev/null || :
%if 0%{?fedora} >= 26
semanage fcontext -a -e %{_root_sysconfdir}    %{_sysconfdir}    &>/dev/null || :
semanage fcontext -a -e %{_root_localstatedir} %{_localstatedir} &>/dev/null || :
%endif
selinuxenabled && load_policy || :
restorecon -R %{?_scl_root}     &>/dev/null || :
%if 0%{?fedora} >= 26
restorecon -R %{_sysconfdir}    &>/dev/null || :
restorecon -R %{_localstatedir} &>/dev/null || :
%endif


%{!?_licensedir:%global license %%doc}

%files


%if 0%{?fedora} < 19 && 0%{?rhel} < 7
%files runtime
%else
%files runtime -f filesystem
%endif
%defattr(-,root,root)
%license LICENSE
%doc README
%scl_files
%{_mandir}/man7/%{scl_name}.*
%{?_licensedir:%{_datadir}/licenses}
%{_datadir}/tests
%if ! %{with_modules}
%{_root_datadir}/Modules/modulefiles/%{scl_name}
%endif


%files build
%defattr(-,root,root)
%{macrosdir}/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{macrosdir}/macros.%{scl_name_base}-scldevel


%changelog
* Fri Mar 17 2017 Remi Collet <remi@remirepo.net> - 2.2-1
- use rh_layout on F26

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> 2.1-5
- add module file for EL

* Wed Mar  9 2016 Remi Collet <remi@fedoraproject.org> 2.1-4
- fix override for pecl_xmldir (F24)

* Tue Jan  5 2016 Remi Collet <remi@fedoraproject.org> 2.1-3
- add missing "sbin" in PATH (Fedora)

* Fri Nov 13 2015 Remi Collet <remi@fedoraproject.org> 2.1-2
- fix selinux context

* Wed Mar 25 2015 Remi Collet <remi@fedoraproject.org> 2.1-1
- fix licenses location
- own directories for pecl packages

* Mon Mar  2 2015 Remi Collet <remi@fedoraproject.org> 2.0-3
- add environement module file

* Wed Nov 26 2014 Remi Collet <remi@fedoraproject.org> 2.0-2
- add LD_LIBRARY_PATH in enable script for embedded

* Mon Sep  8 2014 Remi Collet <remi@fedoraproject.org> 2.0-1
- provides php56-runtime(remi)
- add _sclreq macro

* Sun Aug 24 2014 Remi Collet <rcollet@redhat.com> 1.0-1
- initial packaging from php55 from rhscl 1.1
- install macro in /usr/lib/rpm/macros.d
- each package requires runtime (for license)

* Mon Mar 31 2014 Honza Horak <hhorak@redhat.com> - 1.1-7
- Fix path typo in README
  Related: #1061455

* Mon Mar 24 2014 Remi Collet <rcollet@redhat.com> 1.1-6
- own locale and man directories, #1074337

* Wed Feb 12 2014 Remi Collet <rcollet@redhat.com> 1.1-5
- avoid empty debuginfo subpackage
- add LICENSE, README and php55.7 man page #1061455
- add scldevel subpackage #1063357

* Mon Jan 20 2014 Remi Collet <rcollet@redhat.com> 1.1-4
- rebuild with latest scl-utils #1054731

* Tue Nov 19 2013 Remi Collet <rcollet@redhat.com> 1.1-2
- fix scl_package_override

* Tue Nov 19 2013 Remi Collet <rcollet@redhat.com> 1.1-1
- build for RHSCL 1.1

* Tue Sep 17 2013 Remi Collet <rcollet@redhat.com> 1-1.5
- add macros.php55-build for scl_package_override

* Fri Aug  2 2013 Remi Collet <rcollet@redhat.com> 1-1
- initial packaging
