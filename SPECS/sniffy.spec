%define name Sniffy
%define version 1.0.1
%define unmangled_version 1.0.1
%define unmangled_version 1.0.1
%define release 24
%define _python /usr/bin/python
%define _pip /usr/bin/pip

Summary: Inspect HTTP packets to find potential abusers
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python-setuptools, gnupg
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Evil Corp
Url: https://github.com/nuriel77/Sniffy

%description
Sniffy: Program to inspect HTTP packets for potential abusers.
        Matching certain patterns and registering results to
        database. When limit/threshold is reached will alert
        by sending email with the information.


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
%{_python} setup.py build

%install
%{_python} setup.py install --single-version-externally-managed --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES --install-scripts="/usr/local/bin"
mkdir -p $RPM_BUILD_ROOT/etc/sniffy $RPM_BUILD_ROOT/etc/init.d $RPM_BUILD_ROOT/etc/logrotate.d $RPM_BUILD_ROOT/usr/local/bin $RPM_BUILD_ROOT/etc/cron.d
install -m 700 etc/init.d/sniffy $RPM_BUILD_ROOT/etc/init.d/sniffy
install -m 700 scripts/get_signatures.sh $RPM_BUILD_ROOT/usr/local/bin/get_signatures.sh
install -m 644 etc/cron.d/sniffy_signatures $RPM_BUILD_ROOT/etc/cron.d/.
install -m 600 etc/sniffy/* $RPM_BUILD_ROOT/etc/sniffy/.
install -m 640 etc/logrotate.d/sniffy $RPM_BUILD_ROOT/etc/logrotate.d/sniffy
echo /etc/init.d/sniffy >> INSTALLED_FILES
echo /etc/cron.d/sniffy_signatures >> INSTALLED_FILES
echo /usr/local/bin/get_signatures.sh >> INSTALLED_FILES
echo "%config(noreplace) /etc/sniffy/defaults" >> INSTALLED_FILES
echo "%config(noreplace) /etc/sniffy/db.creds.yml" >> INSTALLED_FILES
echo "%config(noreplace) /etc/sniffy/signatures.yml" >> INSTALLED_FILES
echo "%config /etc/logrotate.d/sniffy" >> INSTALLED_FILES

%post
/sbin/service sniffy start > /dev/null 2>&1 || :
/sbin/chkconfig --add sniffy > /dev/null 2>&1 || :

%preun
if [ "$1" = 0 ]
then
  /sbin/service sniffy stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del sniffy > /dev/null 2>&1 || :
fi

%postun
service sniffy condrestart > /dev/null 2>&1 ||:

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
