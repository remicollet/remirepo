%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

Name:     php-thrift_protocol
Version:  0.9.0
Release:  1%{?dist}
Summary:  PHP wrapper to thrift

Group:    Development/Tools
License:  PHP
URL:      http://thrift.apache.org/
Source0:  https://dist.apache.org/repos/dist/release/thrift/%{version}/thrift-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	php-devel
BuildRequires:	php-pear
BuildRequires: automake
BuildRequires: libtool

Requires:	 php(zend-abi) = %{php_zend_api}
Requires:	 php(api) = %{php_core_api}
Requires:	 php-common

%description
This package provides a native PHP extention to thrift, for improved performance.

%prep
%setup -q -n thrift-%{version}

%build
cd lib/php/src/ext/thrift_protocol
phpize
./configure --enable-thrift_protocol
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd lib/php/src/ext/thrift_protocol
%{__make} install INSTALL_ROOT=%{buildroot} INSTALL="install -p"
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/thrift_protocol.ini << 'EOF'
; enable thrift extension
extension="thrift_protocol.so"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/thrift_protocol.ini
%{php_extdir}/thrift_protocol.so


%doc README LICENSE

%changelog
* Thu Feb 21 2013 Arnoud Vermeer <arnoud@tumblr.com> 0.9.0-1.tumblr
- new package built with tito