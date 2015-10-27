-   Install svn command line tools:
    -   [http://www.sliksvn.com/pub/Slik-Subversion-1.7.2-x64.msi](http://www.sliksvn.com/pub/Slik-Subversion-1.7.2-x64.msi "http://www.sliksvn.com/pub/Slik-Subversion-1.7.2-x64.msi")

-   Add svn tools to path
    -   \> setx -m PATH "C:\\Program Files\\SlikSvn\\bin;%path%"

-   Set default editor
    -   \> setx -m SVN\_EDITOR "C:\\Program Files\\Windows NT\\Accessories\\wordpad.exe"

Action

Command

| Example

Create a Branch or tag

svn copy URL1 URL2 -m "creating new branch for XYZ" \
\

c:\\sources\> svn copy https://ucprepo/svn/ucp/trunk/HiPCM/Trunk/ \\ https://ucprepo/svn/ucp/branches/MyNewBranch/ \\ "Creating new branch MyNewBranch" **NOTE:** This operation is very quick and low-cost. It should be used for long standing branches as well as one-off spikes. Operation can be followed with 'svn switch' to switch working copy to new branch.

Switch a working copy to a branch or tag

svn switch URL

c:\\sources\\trunk\>svn info Working Copy Root Path: C:\\sources URL: https://ucprepo/svn/ucp/trunk ... c:\\sources\\trunk\>svn switch https://ucprepo/svn/ucp/branches/GA1.0 c:\\sources\\trunk\>svn info URL: https://ucprepo/svn/ucp/branches/GA1.0

Synchronize a branch with trunk

svn merge trunkURL; svn commit

-   1.  This merges changes only on your local machine. You will still need to commit them after running build test.

C:\\V2Sources\\branches\\GA2.0\>svn merge https://ucprepo/svn/v2ucp/trunk

-   1.  Check status of merged files - Make sure none are in 'Conflict' state

C:\\V2Sources\\branches\\GA2.0\>svn stat

-   1.  Commit merged changes

C:\\V2Sources\\branches\\GA2.0\>svn commit -m "Merging up to revision \#\#\#\# from trunk"

See merge history between two branches

svn mergeinfo SOURCE TARGET

c:\\sources\\branches\\1.0-Patch2.5\>svn mergeinfo .

Merge a branch back into trunk \
\

svn merge --reintegrate branchURL; svn commit

svn merge --reintegrate https://ucprepo/svn/ucp/branches/1.0-Patch2.5/ **NOTE:** Branch must be deleted and re-created after this operation. If it is not, subsequent merges will result in erroneous conflicts \
 **NOTE:** Before re-integrating to trunk, all changes from trunk must be merged and resolved on the branch.

Merge one specific revision

svn merge -c REV URL; svn commit

c:\\sources\\branches\\1.0-Patch2.5\>svn merge -r 28727 https://ucprepo/svn/ucp/trunk/

Merge range of changes \
\

svn merge -r REV1:REV2 URL; svn commit

c:\\sources\\branches\\1.0-Patch2.5\>svn merge -r 28720:28727 https://ucprepo/svn/ucp/trunk/ **NOTE:** Changes should be merged to/from parent branch rather than siblings

Undo file delete

svn copy URL@REV localPath \
**NOTE:** REV=revision at which time the object existed

svn copy https://ucprepo/svn/v2ucp/trunk/automation@8321 c:\\v2ucp\\trunk\\automation ; svn commit -m "reverting delete" \
**NOTE:** You can also revert through tortoise svn client. -\> Show log, right click, revert

Undo committed change

svn merge -c -REV URL; svn commit \
\

c:\\sources\\trunk\>svn merge -c -5147 https://ucprepo/svn/ucp/trunk/ **NOTE:** Notice the extra '-' in front of 'REV'

Rename a folder or file \
\

svn move URL1 URL2

svn move "https://ucprepo/svn/ucp/test.tmp" "https://ucprepo/svn/ucp/test.tmp2" -m "copy test" **NOTE:** It is safer to perform renames as atomic operations via URL rather than locally

Remove a branch

svn delete URL

c:\\sources\\trunk\> svn delete https://ucprepo/svn/ucp/Branches/MyTemporaryBranch

Pro tips
--------

-   using the '\^' operator in a command automatically substitutes the fully qualified URL path for the current directory
    -   EX:

c:\\sources\>svn copy "\^/test.tmp" "\^/test.tmp2" -m "copy test" Committed revision 28731.

Is equivalent to:

c:\\sources\> svn copy "https://ucprepo/svn/ucp/test.tmp" "https://ucprepo/svn/ucp/test.tmp2" -m "copy test"

{{pdf|Svnreferencebook.pdf‎|Full SVN reference}}
