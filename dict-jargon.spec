%define         dictname jargon
Summary:	The On-Line Hacker Jargon File dictionary for dictd
Summary(pl):	S³ownik Hacker Jargon dla dictd
Name:		dict-%{dictname}
Version:	4.2.0
Release:	2
License:	GPL
Group:		Applications/Dictionaries
Source0:	ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
URL:		http://www.dict.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	dictzip
BuildRequires:	autoconf
Requires:	dictd
Requires:	%{_sysconfdir}/dictd

%description
This package contains The On-Line Hacker Jargon File, version 4.2.0,
formatted for use by the dictionary server in the dictd package.

%description -l pl
Ten pakiet zawiera s³ownik The On-Line Hacker Jargon File w wersji
4.2.0, sformatowany do u¿ytku z serwerem s³ownika dictd.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make} db

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd/,%{_sysconfdir}/dictd}
%{__make} install dictdir="$RPM_BUILD_ROOT%{_datadir}/dictd/"

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# The On-Line Hacker Jargon File dictionary
database %{dictname} {
    data  \"$dictprefix.dict.dz\"
    index \"$dictprefix.index\"
}
" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/*.dictconf
%{_datadir}/dictd/%{dictname}*
