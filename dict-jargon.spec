%define         dictname jargon
Summary:	The On-Line Hacker Jargon File dictionary for dictd
Name:		dict-%{dictname}
Version:	4.2.0
Release:	1
License:	GPL
Group:		Applications/Dictionary
URL:		http://www.dict.org/
Source0:	ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:  dictzip
Requires:       dictd 
BuildArch:      noarch

%description 
This package contains The On-Line Hacker Jargon File, version 4.2.0,
formatted for use by the dictionary server in the dictd package.

%prep
%setup -q

%build
%configure 
%{__make} db 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/dictd/

DICTDIR="$RPM_BUILD_ROOT%{_datadir}/dictd/"
make install dictdir="$DICTDIR" 

%clean
rm -rf $RPM_BUILD_ROOT

%post
prefix=%{_datadir}/dictd/%{dictname}

if ! grep ' %{dictname} ' /etc/dictd.conf >/dev/null; then 
   echo "Edit /etc/dictd.conf to see %{dictname} dictionary under dictd"
echo "# Uncommment this to configure The On-Line Hacker Jargon File dictionary
#database %{dictname} {
#    data  \"$prefix.dict.dz\"
#    index \"$prefix.index\" }
" >> /etc/dictd.conf
fi

%files
%defattr(644,root,root,755)
%{_datadir}/dictd/%{dictname}*
