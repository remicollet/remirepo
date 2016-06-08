%global scl_name_base    php
%global scl_name_version 70
%global scl              %{scl_name_base}%{scl_name_version}
%global macrosdir        %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_root_sysconfdir}/rpm; echo $d)
%global install_scl      1
%if 0%{?fedora} >= 20
# Requires scl-utils v2 for SCL integration
%global with_modules     1
%global rh_layout        1
%else
# Works with file installed in /usr/share/Modules/modulefiles/
%global with_modules     0
%global nfsmountable     1
%endif
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs PHP 7.0
Name:          %scl_name
Version:       1.0
Release:       5%{?dist}
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

Requires:      %{?scl_prefix}php-common%{?_isa}
Requires:      %{?scl_prefix}php-cli%{?_isa}
Requires:      %{?scl_name}-runtime%{?_isa}      = %{version}-%{release}

%description
This is the main package for %scl Software Collection,
that install PHP 7.0 language.


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

cat %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

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
semanage fcontext -a -e %{_root_sysconfdir}    %{_sysconfdir}    &>/dev/null || :
semanage fcontext -a -e %{_root_localstatedir} %{_localstatedir} &>/dev/null || :
selinuxenabled && load_policy || :
restorecon -R %{?_scl_root}     &>/dev/null || :
restorecon -R %{_sysconfdir}    &>/dev/null || :
restorecon -R %{_localstatedir} &>/dev/null || :


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
* Wed Jun  8 2016 Remi Collet <remi@fedoraproject.org> 1.0-5
- fix description (PHP 7.0 is stable)

* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> 1.0-4
- add module file for EL

* Mon Mar  7 2016 Remi Collet <remi@fedoraproject.org> 1.0-3
- fix override for pecl_xmldir (F24)

* Tue Jan  5 2016 Remi Collet <remi@fedoraproject.org> 1.0-2
- add missing "sbin" in PATH (Fedora)

* Wed Nov  4 2015 Remi Collet <remi@fedoraproject.org> 1.0-1
- requires semanage and selinuxenabled commands
  instead of packages

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> 1.0-0.5
- F23 rebuild with rh_layout

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> 1.0-0.4
- use rh_layout instead of nfsmountable in Fedora

* Tue Jun 23 2015 Remi Collet <remi@fedoraproject.org> 1.0-0.3
- enable nfsmountable (not to be nfs montable)
- move configuration dir to /etc/opt
- move localstate dir to /var/opt
- fix incorrect selinux contexts

* Wed Mar 25 2015 Remi Collet <remi@fedoraproject.org> 1.0-0.2
- fix licenses location
- own directories for pecl packages

* Wed Mar 25 2015 Remi Collet <remi@fedoraproject.org> 1.0-0.1
- initial packaging
