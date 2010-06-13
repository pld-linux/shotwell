Summary:	Photo manager for GNOME
Name:		shotwell
Version:	0.5.2
Release:	1
License:	LGPL v2+ and CC-BY-SA
Group:		X11/Applications
Source0:	http://yorba.org/download/shotwell/0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	a347765f3a6ae8408a97d559ed50b0b8
URL:		http://yorba.org/shotwell/
BuildRequires:	GConf2-devel >= 2.22.0
BuildRequires:	dbus-glib-devel >= 0.80.0
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.14.4
BuildRequires:	gtk-webkit-devel >= 1.1.5
BuildRequires:	libexif-devel >= 0.6.16
BuildRequires:	libgee-devel >= 0.5.0
BuildRequires:	libgphoto2-devel >= 2.4.2
BuildRequires:	libsoup-devel >= 2.26.0
BuildRequires:	libunique-devel >= 1.0.0
BuildRequires:	libusb-compat-devel
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.5.9
BuildRequires:	udev-glib-devel >= 145
BuildRequires:	vala >= 0.8.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,preun):	GConf2
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Shotwell is a digital photo organizer designed for the GNOME desktop
environment. It allows you to import photos from disk or camera,
organize them in various ways, view them in full-window or fullscreen
mode, and export them to share with others.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--disable-schemas-install \
	--disable-desktop-update \
	--disable-icon-update
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang shotwell

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install shotwell.schemas
%update_icon_cache hicolor
%update_desktop_database

%preun
%gconf_schema_uninstall shotwell.schemas

%postun
%update_icon_cache hicolor
%update_desktop_database_postun

%files -f shotwell.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING MAINTAINERS NEWS README THANKS
%attr(755,root,root) %{_bindir}/shotwell
%{_desktopdir}/shotwell-viewer.desktop
%{_desktopdir}/shotwell.desktop
%{_datadir}/shotwell
%{_sysconfdir}/gconf/schemas/shotwell.schemas
%{_iconsdir}/hicolor/*/*/*.svg
