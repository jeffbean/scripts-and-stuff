# Powershell JSON for VMware vCenter 6.0 silent installs

We need to take what the vCenter 6.0 silent install needs and create a JSON file based on parameters. 

Some initial testing with JSON in PS:
    
    $json = @"
    {
       "INSTALLDIR" : "C:\\Program Files\\VMware\\",
       "appliance.net.pnid" : "vCenter.example.com",
       "clientlocale" : "en",
       "db.dsn" : "vCenterDB",
       "db.password" : "sqlpassword",
       "db.type" : "external",
       "db.user" : "vcenter_sql_user",
       "deployment.node.type" : "embedded",
       "machine.cert.replacement" : null,
       "silentinstall" : null,
       "system.vm0.hostname" : null,
       "system.vm0.port" : "443",
       "upgrade.import.directory" : null,
       "vc.5x.password" : null,
       "vc.5x.username" : null,
       "vc.svcuser" : "example\\vcenter_user",
       "vc.svcuserpassword" : "install_password",
       "vmdir.cert.thumbprint" : null,
       "vmdir.domain-name" : "vsphere.local",
       "vmdir.first-instance" : true,
       "vmdir.password" : "sso_user_password",
       "vmdir.replication-partner-hostname" : null,
       "vmdir.site-name" : "Default-First-Site",
       "vmware.data.directory" : "C:\\ProgramData\\VMware\\"
    }
    "@

    $PowerShellRepresentation = $json | ConvertFrom-Json
    $PowerShellRepresentation

    $PowerShellRepresentation | ConvertTo-Json -Compress

After some research I found there is a bug in PS when converting to JSON. So we have to use Compress

## The functions 
These are tailored to be a certain configuration and assume default values will be in the JSON template string. I will have to return and improve for all the install variations including external and embedded database, as well as the deployment.node.type.
    
    $json60installer = @"
    {
       "INSTALLDIR" : "C:\\Program Files\\VMware\\",
       "appliance.net.pnid" : "<changeme>",
       "clientlocale" : "en",
       "db.dsn" : "<changeme>",
       "db.password" : null,
       "db.type" : "external",
       "db.user" : null,
       "deployment.node.type" : "embedded",
       "machine.cert.replacement" : null,
       "silentinstall" : null,
       "system.vm0.hostname" : null,
       "system.vm0.port" : "443",
       "upgrade.import.directory" : null,
       "vc.5x.password" : null,
       "vc.5x.username" : null,
       "vc.svcuser" : "<changeme>",
       "vc.svcuserpassword" : "<changeme>",
       "vmdir.cert.thumbprint" : null,
       "vmdir.domain-name" : "<changeme>",
       "vmdir.first-instance" : true,
       "vmdir.password" : "<changeme>",
       "vmdir.replication-partner-hostname" : null,
       "vmdir.site-name" : "Default-First-Site",
       "vmware.data.directory" : "C:\\ProgramData\\VMware\\"
    }
    "@
    function CreateVCenterJSONFromTemplate() {
        PARAM
        (
          [Parameter(Mandatory = $true)]
          [ValidateNotNullOrEmpty()]
          [string] $VCenterFQDN
          ,
          [Parameter(Mandatory = $true)]
          [ValidateNotNullOrEmpty()]
          [string] $VCInstallUser
          ,
          [Parameter(Mandatory = $true)]
          [ValidateNotNullOrEmpty()]
          [string] $VCInstallPassword
          ,
          [Parameter(Mandatory = $true)]
          [ValidateNotNullOrEmpty()]
          [string] $VCSSODomainName
          ,
          [Parameter(Mandatory = $true)]
          [ValidateNotNullOrEmpty()]
          [string] $DatabaseDSN
          ,
          [Parameter(Mandatory = $false)]
          [ValidateNotNullOrEmpty()]
          [string] $NewSiteName
          ,
          [Parameter(Mandatory = $false)]
          [ValidateNotNullOrEmpty()]
          [string] $ExternalHost
          ,
          [Parameter(Mandatory = $false)]
          [ValidateNotNullOrEmpty()]
          [int] $ExternalPort = 443
          ,
          [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
          $InputJSONObject
        )
        $InputJSONObject.'appliance.net.pnid' = $VCenterFQDN
        $InputJSONObject.'vc.svcuser' = $VCInstallUser
        $InputJSONObject.'vc.svcuserpassword' = $VCInstallPassword
        $InputJSONObject.'vmdir.domain-name' = $VCSSODomainName
        $InputJSONObject.'db.dsn' = $DatabaseDSN
        if ($ExternalHost) {
            $InputJSONObject.'system.vm0.hostname' = $ExternalHost
        }
        if ($ExternalPort) {
            $InputJSONObject.'system.vm0.port' = "$ExternalPort"
        }
    }
    function WriteJsonObjectToFile() {
        param(
            [Parameter(Mandatory = $true)]
            [ValidateScript({
                If(Test-Path $_){$true}else{Throw "Invalid path given: $_"}
            })]
            [string] $OutFile 
            ,
            [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
            $InputJSONObject
        )
        # Has to be compressed or it throws an error, its a BUG in Powershell
        $InputJSONObject | ConvertTo-Json -Compress | Out-File $OutFile
    }

    Try{
        $jsonObject = $json60installer | ConvertFrom-Json
        $jsonObject | CreateVCenterJSONFromTemplate -VCenterFQDN vcenter.jbean.me -VCInstallUser "domain\user" -VCInstallPassword "password1" -VCSSODomainName "vsphere.local" -DatabaseDSN "vCenterDSN"
        
        
        $jsonObject | WriteJsonObjectToFile -OutFile C:\settings.json
    }
    Catch 
    {
        Write-Error -Message $_.Exception.Message 
        Write-Error -Message $_.Exception.ItemName
        Exit 1
    }



# References
* [Parameter Help](http://d-fens.ch/2014/12/04/validating-json-objects-with-powershell-advanced-function-parameters/)
* [Advanced Parameters](https://technet.microsoft.com/en-us/library/hh847743)
* [Try Catch Doc](http://www.vexasoft.com/blogs/powershell/7255220-powershell-tutorial-try-catch-finally-and-error-handling-in-powershell)
* [ConvertTo-Json Error](http://stackoverflow.com/questions/23552000/convertto-json-throws-error-when-using-a-string-terminating-in-backslash)
* [Convert to and From JSON](http://blogs.technet.com/b/heyscriptingguy/archive/2012/10/08/use-powershell-to-convert-to-or-from-json.aspx)

