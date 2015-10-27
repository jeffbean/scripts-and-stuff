# Use your own GitLab URL here
external_url 'http://git-test.mcp.com'

# We assume your repositories are in /home/git/repositories (default for source installs)
git_data_dir '/home/git'

# Re-use the Postgres that is already running on your system
postgresql['enable'] = false
# This db_host setting is for Debian Postgres packages
gitlab_rails['db_host'] = '/var/run/postgresql/'
gitlab_rails['db_port'] = 5432
# We assume you called the GitLab DB user 'git'
gitlab_rails['db_username'] = 'git'
gitlab_rails['ldap_enabled'] = true
gitlab_rails['ldap_servers'] = YAML.load <<-EOS # remember to close this block with 'EOS' below
main: # 'main' is the GitLab 'provider ID' of this LDAP server
  ## label
  #
  # A human-friendly name for your LDAP server. It is OK to change the label later,
  # for instance if you find out it is too large to fit on the web page.
  #
  # Example: 'Paris' or 'Acme, Ltd.'
  label: 'LDAP'

  host: 'mcp.com'
  port: 389 # or 636
  uid: 'sAMAccountName'
  method: 'plain # "tls" or "ssl" or "plain"
  bind_dn: 'CN=gitlab-auth,CN=Managed Service Accounts,DC=mcp,DC=com'
  password: 'start123'

  # This setting specifies if LDAP server is Active Directory LDAP server.
  # For non AD servers it skips the AD specific queries.
  # If your LDAP server is not AD, set this to false.
  active_directory: true

  # If allow_username_or_email_login is enabled, GitLab will ignore everything
  # after the first '@' in the LDAP username submitted by the user on login.
  # Example:
  # - the user enters 'jane.doe@example.com' and 'p@ssw0rd' as LDAP credentials;
  # - GitLab queries the LDAP server with 'jane.doe' and 'p@ssw0rd'.
  # If you are using "uid: 'userPrincipalName'" on ActiveDirectory you need to
  # disable this setting, because the userPrincipalName contains an '@'.
  allow_username_or_email_login: true

  # Base where we can search for users
  #   Ex. ou=People,dc=gitlab,dc=example
  base: ''

  # Filter LDAP users
  #   Note: GitLab does not support omniauth-ldap's custom filter syntax.
  #
  user_filter: ''
EOS
