Summary:	Photo manager for GNOME
Name:		shotwell
Version:	0.12.0
Release:	0.1
License:	LGPL v2+ and CC-BY-SA
Group:		X11/Applications
Source0:	http://yorba.org/download/shotwell/0.12/%{name}-%{version}.tar.bz2
# Source0-md5:	50aa5b48a6c0d337ef584da90e7eec67
Patch0:		%{name}-cflags.patch
URL:		http://yorba.org/shotwell/
# The dependencies are listed in Makefile
BuildRequires:	GConf2-devel >= 3.0
BuildRequires:	bash
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.30.0
BuildRequires:	gstreamer-devel >= 0.10.28
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.32
BuildRequires:	gtk+3-devel >= 3.0.11
BuildRequires:	gtk-webkit3-devel >= 1.4.0
BuildRequires:	json-glib-devel >= 0.6.16
BuildRequires:	libexif-devel >= 0.6.16
BuildRequires:	libgee-devel >= 0.5.0
BuildRequires:	libgphoto2-devel >= 2.4.2
BuildRequires:	libraw-devel >= 0.9.0
BuildRequires:	libsoup-devel >= 2.26.0
BuildRequires:	libunique3-devel >= 3.0.0
BuildRequires:	libusb-compat-devel
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	m4
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.5.9
BuildRequires:	udev-glib-devel >= 145
BuildRequires:	vala >= 1:0.15.2
BuildRequires:	vala-gexiv2 >= 0.3.92
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
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
#%patch0 -p1

%build
# this is not autoconf generated
./configure \
	--prefix=%{_prefix} \
	--lib=%{_lib} \
	--disable-schemas-install \
	--disable-desktop-update \
	--disable-icon-update

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	PLUGIN_CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang shotwell --with-gnome
%find_lang shotwell-extras

cat shotwell.lang shotwell-extras.lang > shotwell-all.lang

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

%files -f shotwell-all.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING MAINTAINERS NEWS README THANKS
%attr(755,root,root) %{_bindir}/shotwell*
%{_desktopdir}/%{name}-viewer.desktop
%{_desktopdir}/%{name}.desktop
%{_datadir}/%{name}
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/builtin
%{_libdir}/%{name}/plugins/builtin/*.png
%{_libdir}/%{name}/plugins/builtin/*.glade
%attr(755,root,root) %{_libdir}/%{name}/plugins/builtin/*.so
%{_iconsdir}/hicolor/*/*/*.svg
