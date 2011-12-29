%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}

%{?filter_setup:
%filter_provides_in %{python_sitearch}.*\.so$
%filter_provides_in %{php_extdir}.*\.so$
%filter_provides_in %{ruby_sitearch}.*\.so$
%filter_provides_in %{_docdir} 
%filter_requires_in %{_docdir}
%filter_setup
}

Name:    zorba
Version: 2.1.0
Release: 1%{?dist}
Summary: General purpose XQuery processor implemented in C++
Group:   System Environment/Libraries

# binaries/XQuery modules: ASL 2.0 and BSD
# xsd schema files: W3C
# modules/functx/functx.xq: LGPLv2
License: ASL 2.0 and BSD and W3C and LGPLv2

URL:     http://www.zorba-xquery.com
Source0: http://launchpad.net/zorba/trunk/2.0/+download/%{name}-%{version}.tar.gz

BuildRequires: bison
BuildRequires: boost-devel
BuildRequires: chrpath
BuildRequires: cmake 
BuildRequires: doxygen
BuildRequires: flex
BuildRequires: graphviz
BuildRequires: java-devel >= 1:1.6.0
BuildRequires: jpackage-utils
BuildRequires: libcurl-devel
BuildRequires: libicu-devel
BuildRequires: libxml2-devel
BuildRequires: php-cli 
BuildRequires: php-devel
BuildRequires: python-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: swig
BuildRequires: tex(dvips)
BuildRequires: tex(latex)
BuildRequires: xerces-c-devel
BuildRequires: xqc


%description
Zorba is a general purpose XQuery processor implementing in C++ the W3C family 
of specifications. It is not an XML database. The query processor has been 
designed to be embeddable in a variety of environments such as other 
programming languages extended with XML processing capabilities, browsers,
database servers, XML message dispatchers, or smart phones. Its architecture 
employs a modular design, which allows customizing the Zorba query processor to 
the environment's needs. In particular the architecture of the query processor 
allows a pluggable XML store (e.g. main memory, DOM stores, persistent 
disk-based large stores, S3 stores).


%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake
Requires: xqc

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package python
Summary:  Python language binding for %{name}
Group:    Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}


%description python
This package provides the Python module to use the %{name} API.


%package php
Summary:  PHP language binding for %{name}
Group:    Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}

%description php
This package provides the PHP module to use the %{name} API.


%package ruby
Summary:  Ruby language binding for %{name}
Group:    Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: ruby

%description ruby
This package provides the Ruby module to use the %{name} API.


%package java
Summary:  Java language binding for %{name}
Group:    Development/Languages
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: java >= 1:1.6.0
Requires: jpackage-utils

%description java
This package provides the Java module to use the %{name} API.

%package doc
Summary:   Documentation for the Zorba XQuery processor
Group:     Documentation
BuildArch: noarch

%description doc
This package provides documentation for the %{name} command-line client and 
the programming APIs.
 

%prep
%setup -q

# xqc.h is provided by xqc package
rm -f src/include/xqc.h

find \( -name "*.h" -o -name "*.cpp" \) -exec chmod 644 {} \;


%build
mkdir -p build
cd build
%cmake -DZORBA_LIB_DIRNAME:STRING='%{_lib}' ..

make VERBOSE=1 %{?_smp_mflags}

# create zorba.jar
pushd swig/java
javac -d . *.java
jar cf zorba.jar org/
popd

make doc


%install
make install DESTDIR=%{buildroot} INSTALL="install -p" -C build

# move cmake files to cmake module directory
mkdir -p %{buildroot}%{_datadir}/cmake/Modules/
mv %{buildroot}%{_datadir}/cmake/zorba-%{version}/* %{buildroot}%{_datadir}/cmake/Modules/

# move Java extension module to proper directory
mkdir -p %{buildroot}%{_libdir}/zorba-java/
cp -p build/swig/java/zorba.jar %{buildroot}%{_libdir}/zorba-java/
mv %{buildroot}%{_datadir}/java/*.so %{buildroot}%{_libdir}/zorba-java/
rm -f %{buildroot}%{_datadir}/java/*.java

# move PHP extension module to proper directories
mkdir -p %{buildroot}%{php_extdir}
mkdir -p %{buildroot}%{_datadir}/php/zorba
mv %{buildroot}%{_datadir}/php5/zorba_api_wrapper.php %{buildroot}%{_datadir}/php/zorba
mv %{buildroot}%{_datadir}/php5/zorba_api.so %{buildroot}%{php_extdir}

# move Python extension module to proper directory
mkdir -p %{buildroot}%{python_sitearch}
mv %{buildroot}%{_datadir}/python/* %{buildroot}%{python_sitearch}

# move Ruby extension module to proper directory
mkdir -p %{buildroot}%{ruby_sitearch}
mv %{buildroot}%{_datadir}/ruby/zorba_api.so %{buildroot}%{ruby_sitearch}

chrpath --delete %{buildroot}%{_bindir}/zorba
chrpath --delete %{buildroot}%{_bindir}/testdriver
find %{buildroot} -name "*.so" -exec chrpath --delete {} \;
find %{buildroot} -name "*.so" -exec chmod 755 {} \;

rm -f %{buildroot}%{_includedir}/xqc.h

# move docs to temporary directory used in -doc package
mkdir doc.tmp
mv %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/* doc.tmp
rm -rf %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/
rm -f doc.tmp/*.txt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc ChangeLog AUTHORS.txt LICENSE.txt NOTICE.txt README.txt
%{_bindir}/zorba
%{_bindir}/testdriver
%{_libdir}/libzorba_simplestore.so.*
%{_libdir}/zorba/
%{_datadir}/zorba/
%dir %{_datadir}/zorba-%{version}/
%{_datadir}/zorba-%{version}/xqdoc/

%files devel
%{_libdir}/libzorba_simplestore.so
%{_includedir}/zorba/
%{_datadir}/cmake/Modules/*

%files python
%{python_sitearch}/_zorba_api.so
%{python_sitearch}/zorba_api.py*

%files php
%dir %{_datadir}/php/zorba/
%{_datadir}/php/zorba/zorba_api_wrapper.php
%{php_extdir}/zorba_api.so

%files ruby
%{ruby_sitearch}/zorba_api.so

%files java
%{_libdir}/zorba-java/

%files doc
%doc LICENSE.txt
%doc doc.tmp/*


%changelog
* Sat Dec 10 2011 Martin Gieseking <martin.gieseking@uos.de> 2.1.0-1
- updated to new upstream release

* Sun Nov 13 2011 Martin Gieseking <martin.gieseking@uos.de> 2.0.3-1
- updated to new upstream release
- updated Source0 as the upstream repository moved to launchpad

* Mon Sep 19 2011 Martin Gieseking <martin.gieseking@uos.de> 2.0.2-2
- rebuilt for broken dependencies

* Sat Sep 10 2011 Martin Gieseking <martin.gieseking@uos.de> 2.0.2-1
- updated to new upstream release
- dropped patches applied upstream

* Mon Sep 05 2011 Martin Gieseking <martin.gieseking@uos.de> 2.0.1-1
- updated to new upstream release
- the new release no longer provides and depends on jsonxx, thus removed the virtual Provides for the bundled library

* Thu Mar 03 2011 Martin Gieseking <martin.gieseking@uos.de> 1.4.0-3
- added virtual Provides for bundled jsonxx library
- added patch to replace calls of deprecated Boost functions in Fedora >= 15

* Fri Jan 28 2011 Martin Gieseking <martin.gieseking@uos.de> 1.4.0-2
- explicitely BR java/java-devel epoch/version >= 1:1.6.0
- removed BR: php
- move Provides filters to the top
- changed license to ASL 2.0 and BSD
- removed -O3 from CFLAGS/CXXFLAGS
- preserve timestamps of zorba.jar and css files
- link private json library statically
- added missing %%defattr in php subpackage

* Tue Nov 30 2010 Martin Gieseking <martin.gieseking@uos.de> 1.4.0-1
- initial Fedora package 
