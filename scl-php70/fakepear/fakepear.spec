%if 0%{?scl:1}
%scl_package fakepear
%endif
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_root_sysconfdir}/rpm; echo $d)

Summary: Fake pear package to allow build of pecl extension
Name:    %{?scl_prefix}fakepear
Version: 1.0
Release: 2%{?dist}
License: GPLv2+
Group:   Development/Languages
URL:     http://pear.php.net/package/PEAR
Source0: macros.pear

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:  %{?scl_prefix}php-pear
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}}


%description
This is fake package, to allow build of PECL extension.

It only provides macros definition.


%prep
sed -e 's/@SCL@/%{?scl:%{scl}_}/' \
    -e 's:@VARDIR@:%{_localstatedir}:' \
    -e 's:@BINDIR@:%{_bindir}:' \
    -e 's:@DATADIR@:%{_datadir}:' \
    %{SOURCE0} | tee macros.pear
grep @ macros.pear && exit 1


%build
# This is an empty build section.


%install
install -m 644 -D macros.pear \
           $RPM_BUILD_ROOT%{macrosdir}/macros.%{?scl_prefix}pear


%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-,root,root,-)
%{macrosdir}/macros.%{?scl_prefix}pear


%changelog
* Mon Mar 30 2015 Remi Collet <remi@fedoraproject.org> 1.0-2
- more fake macros

* Wed Mar 25 2015 Remi Collet <remi@fedoraproject.org> 1.0-1
- initial package