# spec file for fastlz
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global date   20070619
%global svnrev 12
%global abi    0

Name:      fastlz
Summary:   Portable real-time compression library
Version:   0.1.0
Release:   0.1.%{date}svnrev%{svnrev}%{?dist}
License:   MIT
Group:     System Environment/Libraries
URL:       http://fastlz.org/

# svn export -r 12 http://fastlz.googlecode.com/svn/trunk/ fastlz-12
# tar cjf fastlz-12.tar.bz2 fastlz-12
Source0:   %{name}-%{svnrev}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
FastLZ is a lossless data compression library designed for real-time
compression and decompression. It favors speed over compression ratio.
Decompression requires no memory. Decompression algorithm is very simple,
and thus extremely fast.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%prep
%setup -q -n %{name}-%{svnrev}


%build
# Build the shared library
gcc %optflags -fPIC -c fastlz.c  -o fastlz.o
gcc %optflags -fPIC -shared \
   -Wl,-soname -Wl,lib%{name}.so.%{abi} \
   -o lib%{name}.so.%{abi} fastlz.o
ln -s lib%{name}.so.%{abi} lib%{name}.so

# Build the commands for test
gcc %optflags -fPIC 6pack.c   -L. -l%{name} -o 6pack
gcc %optflags -fPIC 6unpack.c -L. -l%{name} -o 6unpack


%install
rm -rf %{buildroot}

install -D -m 0755 lib%{name}.so.%{abi} %{buildroot}%{_libdir}/lib%{name}.so.%{abi}
ln -s lib%{name}.so.%{abi} %{buildroot}%{_libdir}/lib%{name}.so
install -D -pm 0644 %{name}.h           %{buildroot}%{_includedir}/%{name}.h

# Don't install the commands, as we obviously don't need more compression tools


%check
export LD_LIBRARY_PATH=$PWD
cp %{name}.c tmpin
./6pack -v
./6unpack -v

: Compress
./6pack -1 tmpin tmpout1
./6pack -2 tmpin tmpout2

: Uncompress 1
rm tmpin
./6unpack tmpout1
diff %{name}.c tmpin

: Uncompress 2
rm tmpin
./6unpack tmpout2
diff %{name}.c tmpin


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr (-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/lib%{name}.so.%{abi}

%files devel
%defattr (-,root,root,-)
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h


%changelog
* Fri Sep  5 2014 Remi Collet <remi@fedoraproject.org> - 0.1-0.1.20070619svnrev12
- Initial RPM