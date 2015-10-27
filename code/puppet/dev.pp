$ssh_key = "AAAAB3NzaC1kc3MAAAEBAIzOCMb9IzoZyl0ztYrfsdH5DGdn9sAss2eHcEeFob7xMoP8p2GtRJJ3G1aGIS7SPENSuPQ9GV8RIuknqCRIEfT268mWCDRe6oYkcLmbVBDhtZFbwG0Igj8wOxFMHziCopqm/9HPpP2mjPra5cZr/Iv40jaf9gbQIpgR/J2bCHT/EnK9G21GhUjMH59OcR/kaSkEh1W+AE/ol94y2ynrHqiS7MgDRP5hzr6IV8nPO/mE3ZqEKKVVPafKrmgv6XKY6XSEL1oTjAiPDe6Pyfg34VHOAXZMJ1IQCb99gAnPKX079uW+DjtQ+H1Qbgg0nw6KKdddfJIYCZO94a2/AP3YQ/UAAAAVAJkH/MnWiekjWO/iWZIrmeVE4V2ZAAABAGrtx0jlM74dO5uX3UYs6MXZV1keoMg/TppXyIldpV1lB0z49NtKYoSAIp3ZCnFsMwq+LrgKRgqrWma2Tvkf1PDL0Xi73oSjM50AsUDn1+HctBjR+jDP7A3Wx8czzCVY2485NjNhLuInz8vuaXeC/9gNBiyp3qxeOVyCC/L9p3RmPhWXgx+MtsDWAqOtdzXr9wL+RGIR5Tc62jLRAZ22RC+zYfXwmCTuiHGgn8yIfPAv1Nx/iayBEQF/xK/yV00InGiQRe2GZvGcGR50yDbLgV0u76gxitx3pbGHv+DfIW7DijoClCmyroH+4MEaO364gyZnaDtlJwJVbf3iApeXrt8AAAEAYs93xd2xFlg663O5E1D/yIg2nwD3Rzsr1NTUUIokf+Vnwyfll9tRSHmoUv0DCKgyx7SZWRTZnTsXe4ifkLhAQ3wK+NefZy4tfBr12FhhQLUDbhBXhyM4d+0gKGS1xReyfJscDss2NX6NFYRVnEEy10U76AReLBaTbFkhqGKM5B+C2hWKTGLBiiG6KTTs5inkUU8Oj7jTqQ5zpLxbm2xRn2Bhq/+0fCAMSs/3suHxQ9F5fyCLnuCY0fJ0aFAJfh2BeAkF1YMhNsqtdCnjDDvmgjAltiQMBreiogIiHgrz9fiog5aZRmsKYlJz0xwt6tJ/n9iot1fgSrXOdjmywrnyGQ=="


class ntp {
    case  $operatingsystem {
        centos, redhat: {
            $service_name = 'ntp'
            $conf_file    = 'ntp.conf.el'
    }
        debian, ubuntu: {
            $service_name = 'ntp'
            $conf_file    = 'ntp.conf.debian'
        }
    }

      package { 'ntp':
        ensure => installed,
      }

      service { 'ntp':
        name      => $service_name,
        ensure    => running,
        enable    => true,
        subscribe => File['ntp.conf'],
      }

      file { 'ntp.conf':
        path    => '/etc/ntp.conf',
        ensure  => file,
        require => Package['ntp'],
        source  => "/root/learning-manifests/${conf_file}",
      } 
}

class sshd {
    package { 'openssh-server':
          ensure => present,
          before => File['/etc/ssh/sshd_config'],
        }

    file { '/etc/ssh/sshd_config':
          ensure => file,
          mode   => 600,
          source => '/root/learning-manifests/sshd_config',
          # And yes, that's the first time we've seen the "source" attribute.
          # It accepts absolute paths and puppet:/// URLs, about which more later.
    }

    service { 'sshd':
          ensure     => running,
          enable     => true,
          hasrestart => true,
          hasstatus  => true,
          subscribe  => File['/etc/ssh/sshd_config'],
    }

    ssh_authorized_key {
            'archivas_weak_key':
            ensure => present,
            key => $::ssh_key,
            user => 'root',
            type => 'ssh-dss',
    }
}

class { 'ntp': }
