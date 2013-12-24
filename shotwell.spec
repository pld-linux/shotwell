Summary:	Photo manager for GNOME
Name:		shotwell
Version:	0.15.1
Release:	1
License:	LGPL v2+ and CC-BY-SA
Group:		X11/Applications
Source0:	http://yorba.org/download/shotwell/0.15/%{name}-%{version}.tar.xz
# Source0-md5:	5af4cfb819249a879a4649a9c7d089e5
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-format_string.patch
URL:		http://yorba.org/shotwell/
# The dependencies are listed in Makefile
BuildRequires:	atk-devel
BuildRequires:	bash
BuildRequires:	gettext-devel
BuildRequires:	gexiv2-devel
BuildRequires:	glib2-devel >= 2.30.0
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.6
BuildRequires:	gtk-webkit3-devel >= 1.4.0
BuildRequires:	json-glib-devel >= 0.6.16
BuildRequires:	libexif-devel >= 0.6.16
BuildRequires:	libgee-devel >= 0.8.5
BuildRequires:	libgphoto2-devel >= 2.4.2
BuildRequires:	libraw-devel >= 0.14.7-2
BuildRequires:	libsoup-devel >= 2.26.0
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	m4
BuildRequires:	pkgconfig
BuildRequires:	rest-devel >= 0.7
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.5.9
BuildRequires:	udev-glib-devel >= 145
BuildRequires:	vala >= 1:0.20.1
BuildRequires:	vala-gexiv2 >= 0.4.90
BuildRequires:	vala-libgee >= 0.8.5
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Shotwell is a digital photo organizer designed for the GNOME desktop
environment. It allows you to import photos from disk or camera,
organize them in various ways, view them in full-window or fullscreen
mode, and export them to share with others.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# this is not autoconf generated
./configure \
	--prefix=%{_prefix} \
	--lib=%{_lib} \
	--libexec=%{_libexecdir} \
	--disable-desktop-update \
	--disable-icon-update

%{__make} \
	CC="%{__cc}" \
	RPMCFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_localedir}/nn{_NO,}

# af_ZA is a duplicate of af
# id_ID is a duplicate of id
# ta_IN is a duplicate of ta
# te_IN is incomplete duplicate of te
# tr_TR is incomplete duplicate of tr
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{af_ZA,id_ID,ta_IN,te_IN,tr_TR}

%find_lang shotwell --with-gnome
%find_lang shotwell-extras

cat shotwell.lang shotwell-extras.lang > shotwell-all.lang

%{__rm} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/gschemas.compiled

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%update_desktop_database_postun
%glib_compile_schemas

%files -f shotwell-all.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING MAINTAINERS NEWS README THANKS
%attr(755,root,root) %{_bindir}/shotwell*
%{_desktopdir}/%{name}-viewer.desktop
%{_desktopdir}/%{name}.desktop
%attr(755,root,root) %{_libexecdir}/shotwell-settings-migrator
%attr(755,root,root) %{_libexecdir}/shotwell-video-thumbnailer
%{_datadir}/appdata/shotwell.appdata.xml
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
