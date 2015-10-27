## Upgrade from 5.5 -> 6.0

Run this on the SQL server to give permissions to DSN account.

    use [master]
    GO
    GRANT VIEW ANY DEFINITION TO [podg\svc_vcntr]
    GO
    use [master]
    GO
    GRANT VIEW SERVER STATE TO [podg\svc_vcntr]
    GO


## External DB
    {
       "INSTALLDIR" : "C:\\Program Files\\VMware\\",
       "appliance.net.pnid" : "vCenter.podc.local",
       "clientlocale" : "en",
       "db.dsn" : "vCenterDB",
       "db.password" : "password",
       "db.type" : "external",
       "db.user" : "podc\\svc_vcntr",
       "deployment.node.type" : "embedded",
       "system.vm0.hostname" : null,
       "system.vm0.port" : "443",
       "upgrade.import.directory" : null,
       "vc.5x.password" : null,
       "vc.5x.username" : null,
       "vc.svcuser" : "podc\\svc_vcntr",
       "vc.svcuserpassword" : "password",
       "vmdir.cert.thumbprint" : null,
       "vmdir.domain-name" : "podc.local",
       "vmdir.first-instance" : true,
       "vmdir.password" : "password",
       "vmdir.replication-partner-hostname" : null,
       "vmdir.site-name" : "UCP-podc",
       "vmware.data.directory" : "C:\\ProgramData\\VMware\\"
    }



## Embedded DB

### Installing vCenter 6 with embedded PSC standalone

    {
        "INSTALLDIR" : "C:\\Program Files\\VMware\\",
        "appliance.net.pnid" : "10.21.57.222",
        "db.type" : "embedded",
        "deployment.node.type" : "embedded",
        "machine.cert.replacement" : "jbean.local",
        "system.vm0.hostname" : null,
        "system.vm0.port" : "443",
        "vc.svcuser" : null,
        "vc.svcuserpassword" : null,
        "vmdir.cert.thumbprint" : null,
        "vmdir.domain-name" : "vsphere.local",
        "vmdir.first-instance" : true,
        "vmdir.password" : "password",
        "vmdir.site-name" : "Default-First-Site-standalone",
        "vmware.data.directory" : "C:\\ProgramData\\VMware\\"
    }

### Installing vCenter 6 with embedded PSC and joining an exsisting site

    {
        "INSTALLDIR" : "C:\\Program Files\\VMware\\",
        "appliance.net.pnid" : "10.21.57.222",
        "db.type" : "embedded",
        "deployment.node.type" : "embedded",
        "machine.cert.replacement" : null,
        "system.vm0.hostname" : null,
        "system.vm0.port" : "443",
        "vc.svcuser" : null,
        "vc.svcuserpassword" : null,
        "vmdir.cert.thumbprint" : null,
        "vmdir.domain-name" : "vsphere.local",
        "vmdir.first-instance" : false,
        "vmdir.password" : "password",
        "vmdir.replication-partner-hostname" : "10.21.57.220",
        "vmdir.site-name" : "Default-First-Site",
        "vmware.data.directory" : "C:\\ProgramData\\VMware\\"
    }


## Upgrade from 5.5
    {
       "INSTALLDIR" : "D:\\ProgramData\\VMware\\",
       "appliance.net.pnid" : "VCENTER.podg.local",
       "clientlocale" : "en",
       "db.clobber" : null,
       "db.dsn" : "vCenterDB",
       "db.password" : null,
       "db.type" : "external",
       "db.user" : null,
       "deployment.node.type" : null,
       "machine.cert.replacement" : null,
       "silentinstall" : null,
       "system.vm0.hostname" : null,
       "system.vm0.port" : "443",
       "upgrade.import.directory" : "D:\\ProgramData\\VMware\\vCenterServer\\export\\",
       "vc.5x.password" : "password",
       "vc.5x.username" : "administrator@vsphere.local",
       "vc.svcuser" : "podg\\svc_vcntr",
       "vc.svcuserpassword" : "password",
       "vmdir.cert.thumbprint" : null,
       "vmdir.domain-name" : "vsphere.local",
       "vmdir.first-instance" : true,
       "vmdir.password" : "password",
       "vmdir.replication-partner-hostname" : null,
       "vmdir.site-name" : "Default-First-Site",
       "vmware.data.directory" : "D:\\ProgramData\\VMware\\"
    }
