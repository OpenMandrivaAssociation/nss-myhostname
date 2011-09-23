Name:		nss-myhostname
Summary:	glibc plugin for local system host name resolution
Version:	0.3
Release:	%mkrel 1
License:	LGPLv2+
Group:		System/Base
URL:		http://0pointer.de/lennart/projects/nss-myhostname/
Source0:	http://0pointer.de/lennart/projects/nss-myhostname/nss-myhostname-%{version}.tar.gz
Requires(pre):	glibc
Requires:	/bin/sh
Requires(pre):	sed
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
nss-myhostname is a plugin for the GNU Name Service Switch (NSS)
functionality of the GNU C Library (glibc) providing host name
resolution for the locally configured system hostname as returned by
gethostname(2). Various software relies on an always resolvable local
host name. When using dynamic hostnames this is usually achieved by
patching /etc/hosts at the same time as changing the host name. This
however is not ideal since it requires a writable /etc file system and
is fragile because the file might be edited by the administrator at
the same time. nss-myhostname simply returns all locally configure
public IP addresses, or -- if none are configured -- the IPv4 address
127.0.0.2 (wich is on the local loopback) and the IPv6 address ::1
(which is the local host) for whatever system hostname is configured
locally. Patching /etc/hosts is thus no longer necessary.

%prep
%setup -q

%build
%configure2_5x \
	--libdir=/%{_lib}

%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -rf %{buildroot}/usr/share/doc/nss-myhostname

%clean
rm -rf %{buildroot}

%post
# sed-fu to add myhostname to the hosts line of /etc/nsswitch.conf
if [ -f /etc/nsswitch.conf ] ; then
        sed -i.bak -e '
                /^hosts:/ !b
                /\<myhostname\>/ b
                s/[[:blank:]]*$/ myhostname/
                ' /etc/nsswitch.conf
fi

%preun
# sed-fu to remove myhostname from the hosts line of /etc/nsswitch.conf
if [ "$1" -eq 0 -a -f /etc/nsswitch.conf ] ; then
        sed -i.bak -e '
                /^hosts:/ !b
                s/[[:blank:]]\+myhostname\>//
                ' /etc/nsswitch.conf
fi


%files
%defattr(-,root,root)
%doc README
%doc LICENSE
/%{_lib}/*
