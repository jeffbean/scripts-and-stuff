
function VmwareVCenterAddUserAdminPrivleges {
    #########################################################################################
    # This function assumes you are connected to VI-Server
    # $server = Connect-VIServer -User ${USER} -Password ${USER} -Server ${VCENTER_IP}
    # Disconnect-VIServer -Server $server
    #########################################################################################
    param(
        [array]$admin_users
    )
    # $userList = @("podc\svc_vcntr", "podc\ucpadmin", "podc\svc_ucp")
    # VmwareVCenterAddUserAdminPrivleges "10.21.57.241" "administrator" "password" $userList
    #region Private Functions
    #endregion
    foreach ($user in $admin_users) {
        $rootFolder = Get-Folder -NoRecursion
        $myPermission = New-VIPermission -Role Admin -Principal "${user}" -Entity $rootFolder -Propagate:$true
        Set-VIPermission -Permission $myPermission -Role Admin -Propagate:$true
    }

}
function VmwareVCenterAddDatacenters {
    #########################################################################################
    # This function assumes you are connected to VI-Server
    # $server = Connect-VIServer -User ${USER} -Password ${USER} -Server ${VCENTER_IP}
    # Disconnect-VIServer -Server $server
    #########################################################################################
    param(
        [array]$datacenters
    )
    foreach ($dc in $datacenters){
        Write-Host "Creating $dc datacenter"
        New-Datacenter -Name $dc -Location Datacenters | Out-Null
    }
}

function VmwareVCenterAddHostsToDatacenter {
    #########################################################################################
    # This function assumes you are connected to VI-Server
    # $server = Connect-VIServer -User ${USER} -Password ${USER} -Server ${VCENTER_IP}
    # Disconnect-VIServer -Server $server
    #########################################################################################
    # $hostList = @("10.21.57.231", "10.21.57.233")
    # VmwareVCenterAddHostsToDatacenter "UCP Management" "root" "password" $hostList "UCPManagement"
    param(
        [Parameter(
            Mandatory=$true,
            Position=1,
            HelpMessage="The datacenter name to add the hosts to.")
        ]
        [string]$vcenter_datacenter_name,
        [Parameter(
            Mandatory=$true,
            Position=2,
            HelpMessage="The username for the hosts you want to add to the datacenter.")
        ]
        [string]$host_username,
        [Parameter(
            Mandatory=$true,
            Position=3,
            HelpMessage="The password for the hosts you want to add to the datacenter.")
        ]
        [string]$host_password,
        [Parameter(
            Mandatory=$true,
            Position=4,
            HelpMessage="The array of hosts to add to datacenter.")
        ]
        [array] $hosts,
        [Parameter(
            Mandatory=$true,
            Position=5,
            HelpMessage="The cluster name to add the list of hosts to.")
        ]
        [string]$vcenter_cluster_name
    )

    foreach ($host_to_add in $hosts)
    {
        Write-Host " Add $host_to_add to vCenter"
        Add-VMHost $host_to_add -Force -Location "$vcenter_datacenter_name" -User $host_username -Password $host_password | Out-Null
    }
    if ($hosts.Count -gt 1)
    {
        Write-Host " Create management cluster $vcenter_cluster_name in vCenter"
        New-Cluster -Location "$vcenter_datacenter_name" -Name "$vcenter_cluster_name" -DRSEnabled -DRSAutomationLevel FullyAutomated -HAEnabled | Out-Null
        foreach ($host_to_move in $hosts)
        {
            Write-Host " Add $host_to_move to $vcenter_cluster_name cluster"
            Move-VMHost -VMHost $host_to_move -Destination (Get-Cluster "$vcenter_cluster_name") | Out-Null
        }
    }
}

Add-PSSnapin VMware.VimAutomation.Core | Out-Null
  Connect-VIServer -User "administrator@vsphere.local" -Password "" -Server "10.21.57.241" -wa 0 | Out-Null

  # Adding the userlist to the VMware vCenter Administrator group with permissions
  $userList = @("podc\svc_vcntr", "podc\admin", "podc\svc_user")
  VmwareVCenterAddUserAdminPrivleges $userList

  # Adding list of datacenters to VCenter
  $datacenterList = @("UCP Compute", "UCP Management")
  VmwareVCenterAddDatacenters $datacenterList

  # Adding Management Hosts to the UCPManagement Datacenter
  $hostList = @("10.21.57.231", "10.21.57.233")
  VmwareVCenterAddHostsToDatacenter "UCP Management" "root" "password" $hostList "UCPManagement"
  # VmwareVCenterAddHostsToDatacenter $VCENTER_CONFIG_DATACENTER_MANAGEMENT $MANAGEMENT_HOST_USERNAME $MANAGEMENT_HOST_PASSWORD $hostList $VCENTER_CONFIG_MANAGEMENT_CLUSTER_NAME
