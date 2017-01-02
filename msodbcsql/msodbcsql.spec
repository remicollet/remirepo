# remirepo spec file for msodbcsql
#
# Copyright (c) 2016-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global __arch_install_post  /bin/true
%global debug_package        %{nil}
%global __debug_install_post /bin/true

%global vendor  microsoft
%global libname libmsodbcsql-13.0.so.0.0
%global dm_name ODBC Driver 13 for SQL Server
%global descr   Microsoft ODBC Driver for SQL Server

Name:          msodbcsql
Summary:       Tools of %{descr}
Version:       13.0.0.0
Release:       2%{?dist}
License:       Distribuable
Group:         Applications/Databases

URL:           https://msdn.microsoft.com/library/hh568454(v=sql.110).aspx
# See: https://github.com/Microsoft/msphpsql/blob/PHP-7.0-Linux/ODBC%20install%20scripts/installodbc_redhat.sh#L56
Source0:       https://download.microsoft.com/download/B/C/D/BCDD264C-7517-4B7D-8159-C99FC5535680/msodbcsql-13.0.0.0.tar.gz

BuildArch:     x86_64
# Upstream use this exact version, be relax for Fedora (2.3.4)
BuildRequires: unixODBC >= 2.3.1

Requires(preun): %{_bindir}/odbcinst
Requires(post):  %{_bindir}/odbcinst
Requires:        %{name}-libs%{?_isa} = %{version}-%{release}


%description
%{descr}.

This package provides the command line tools:
- sqlcmd
- bcp


%package libs

Summary: Libraries of %{descr}
Group: Applications/Databases

%description libs
%{descr}.

This package provides the libraries and localization files.


%package devel

Summary:  Development files of %{descr}
Group:    Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{descr}.

This package provides the header files and documentation.


%prep
%setup -q

cat <<EOF | tee %{name}.ini
[%{dm_name}]
Description = %{summary}
Driver = /opt/%{vendor}/%{name}/%{_lib}/%{libname}
Threading = 1
EOF


%build
: tarball provides binaries


%install
: Lib
mkdir -p %{buildroot}%{_libdir}
for fic in %{_lib}/%{libname}
do
  install -D -pm 755 $fic %{buildroot}/opt/%{vendor}/%{name}/$fic
done

: Bin
mkdir -p %{buildroot}%{_bindir}
for fic in bin/bcp-%{version} bin/sqlcmd-%{version}
do
  install -D -pm 755 $fic %{buildroot}/opt/%{vendor}/%{name}/$fic
  target=$(basename $fic -%{version})
  ln -s ../../opt/%{vendor}/%{name}/$fic %{buildroot}%{_bindir}/$target
done

: Rll
for fic in bin/bcp.rll bin/SQLCMD.rll bin/BatchParserGrammar.dfa bin/BatchParserGrammar.llr %{_lib}/msodbcsqlr13.rll
do
  target=$(basename $fic)
  install -D -pm 644 $fic %{buildroot}/opt/%{vendor}/%{name}/%{version}/en_US/$target
done

: Include
for fic in include/msodbcsql.h
do
  target=$(basename $fic)
  install -D -pm 644 $fic %{buildroot}/opt/%{vendor}/%{name}/%{version}/include/$target
done

: Template
install -m 644 %{name}.ini %{buildroot}/opt/%{vendor}/%{name}/%{version}/%{name}.ini

: Docs
mkdir -p %{buildroot}/opt/%{vendor}/%{name}/%{version}/docs/en_US
tar --extract \
    --file docs/en_US.tar.gz \
    --directory %{buildroot}/opt/%{vendor}/%{name}/%{version}/docs/en_US


%preun libs
if [ -f /etc/odbcinst.ini ]; then
  %{_bindir}/odbcinst -u -d -n "%{dm_name}" >/dev/null || :
fi

%post libs
if [ -f /etc/odbcinst.ini ]; then
  %{_bindir}/odbcinst -i -d -f /opt/%{vendor}/%{name}/%{version}/%{name}.ini  >/dev/null || :
fi


%files
%{_bindir}/bcp
%{_bindir}/sqlcmd
/opt/%{vendor}/%{name}/bin

%files libs
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir /opt/%{vendor}
%dir /opt/%{vendor}/%{name}
%dir /opt/%{vendor}/%{name}/%{version}
     /opt/%{vendor}/%{name}/%{version}/*ini
     /opt/%{vendor}/%{name}/%{version}/en_US
     /opt/%{vendor}/%{name}/%{_lib}


%files devel
/opt/%{vendor}/%{name}/%{version}/include
/opt/%{vendor}/%{name}/%{version}/docs


%changelog
* Tue Sep 20 2016 Remi Collet <remi@remirepo.net> - 13.0.0.0-2
- create libs and devel sub packages

* Fri Sep 16 2016 Remi Collet <remi@remirepo.net> - 13.0.0.0-1
- initial package

