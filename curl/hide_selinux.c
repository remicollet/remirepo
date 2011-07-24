/*
 * make it possible to start a testing OpenSSH server with SELinux
 * in the enforcing mode (#521087)
 */
int security_getenforce(void)
{
    return 0;
}
