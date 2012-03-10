%global   client_tag  fb6fca832fd2
%global   codegen_tag 6fb87d6eb01b

Name:      librabbitmq
Summary:   Client library and command line tools for AMPQ
Version:   0.1
Release:   0.1.hg%{client_tag}%{?dist}
License:   MPLv1.1 or GPLv2+
Group:     System Environment/Libraries
URL:       http://www.rabbitmq.com/

Source0:   http://hg.rabbitmq.com/rabbitmq-c/archive/%{client_tag}.tar.bz2
Source1:   http://hg.rabbitmq.com/rabbitmq-codegen/archive/%{codegen_tag}.tar.bz2


BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool
BuildRequires: python-simplejson
# For tools
%if 0%{?rhel} == 5
BuildRequires: popt
%else
BuildRequires: popt-devel
%endif
# For man page
BuildRequires: xmlto


%description
This is a C-language AMQP client library for use with AMQP servers
speaking protocol versions 0-9-1.

It also provides several command line tools:
amqp-consume        Consume messages from a queue on an AMQP server
amqp-declare-queue  Declare a queue on an AMQP server
amqp-delete-queue   Delete a queue from an AMQP server
amqp-get            Get a message from a queue on an AMQP server
amqp-publish        Publish a message on an AMQP server


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. 


%prep
%setup -qc -a 1

mv rabbitmq-c-%{client_tag}        rabbitmq-c

mv rabbitmq-codegen-%{codegen_tag} rabbitmq-codegen
ln rabbitmq-codegen/amqp-rabbitmq-0.9.1.json rabbitmq-codegen/amqp-0.9.1.json

# Copy sources to be included in -devel docs.
cp -pr rabbitmq-c/examples examples


%build
cd rabbitmq-c
autoreconf -i
%configure
make %{_smp_mflags}


%install
rm -rf %{buildroot}
cd rabbitmq-c
make install  DESTDIR="%{buildroot}"

rm %{buildroot}%{_libdir}/%{name}.{a,la}


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig
 

%files
%defattr (-,root,root,-) 
%doc rabbitmq-c/{AUTHORS,COPYING,README,THANKS,TODO,LICENSE*}
%{_libdir}/%{name}.so.*
%{_bindir}/amqp*
%{_mandir}/man1/amqp*
%{_mandir}/man7/%{name}*


%files devel
%defattr (-,root,root,-) 
%doc examples
%{_libdir}/%{name}.so
%{_includedir}/amqp*


%changelog
* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 0.1-1
- Initial RPM

