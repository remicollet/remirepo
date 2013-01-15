Name:         syntaxhighlighter
Version:      3.0.83
Release:      1%{?dist}
Summary:      JavaScript syntax highlighter
Group:        Applications/Internet
# Dual licensed under the MIT and GPL licenses.
License:	  MIT or GPLv2
URL:          http://alexgorbatchev.com/SyntaxHighlighter/

# http://alexgorbatchev.com/SyntaxHighlighter/download/download.php?sh_current
Source0:	  syntaxhighlighter_%{version}.zip
Source1:      %{name}.conf

BuildRoot:    %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:    noarch


%description
SyntaxHighlighter is a fully functional self-contained code
syntax highlighter developed in JavaScript.


%package httpd
Summary:       Apache configuration for %{name}
Group:         Applications/Internet
Requires:      %{name} = %{version}-%{release}
Requires:      httpd

%description   httpd
This package provides the Apache configuration for
applications using an Alias to SyntaxHighlighter library.


%prep
%setup -q -n %{name}_%{version}

# Create a suitable example, easy to run
sed -e 's:src="scripts:src="/%{name}/scripts:' \
    -e 's:href="styles:href="/%{name}/styles:' \
    index.html >example.html

chmod -x {scripts,styles}/*


%build
# Nothing to build


%install
rm -rf %{buildroot}

# JavaScript
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr scripts %{buildroot}%{_datadir}/%{name}/scripts
cp -pr styles  %{buildroot}%{_datadir}/%{name}/styles

# Apache
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LGPL-LICENSE MIT-LICENSE example.html
%{_datadir}/%{name}


%files httpd
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf


%changelog
* Tue Jan 15 2013 Remi Collet <remi@fedoraproject.org> - 3.0.83-1
- initial package
