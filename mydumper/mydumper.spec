%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%global with_doc 1
%else
%global with_doc 0
%endif

# Not suitable for fedora / EPEL because of not exported my_read_net
# See https://bugs.launchpad.net/mydumper/+bug/803982
# And https://bugzilla.redhat.com/show_bug.cgi?id=728634


Name:           mydumper
Version:        0.2.3
Release:        1%{?dist}
Summary:        A high-performance MySQL backup tool

Group:          Applications/Databases
License:        GPLv3+
URL:            http://www.mydumper.org/
Source0:        http://launchpad.net/mydumper/0.2/%{version}/+download/%{name}-%{version}.tar.gz


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  glib2-devel mysql-devel zlib-devel pcre-devel
BuildRequires:  cmake 
%if %{with_doc}
BuildRequires:  python-sphinx
%endif

%description
Mydumper (aka. MySQL Data Dumper) is a high-performance multi-threaded backup
(and restore) toolset for MySQL and Drizzle.

The main developers originally worked as Support Engineers at MySQL
(one has moved to Facebook and another to SkySQL) and this is how they would
envisage mysqldump based on years of user feedback.

%if %{with_doc}
Documentation: /usr/share/doc/mydumper/html/index.html
%endif


%prep
%setup -q


%build
cmake -DCMAKE_INSTALL_PREFIX="%{_prefix}" .
make %{?_smp_mflags} VERBOSE=1


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_datadir}/doc/%{name}/html/.buildinfo


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/mydumper
%{_bindir}/myloader
%if %{with_doc}
%{_mandir}/man1/mydumper.*
%{_mandir}/man1/myloader.*
%doc %{_datadir}/doc/%{name}
%endif


%changelog
* Sun Apr 15 2012 Remi Collet <remi@fedoraproject.org> - 0.2.3-1
- initial package

