# Release process

1. get the latest
    1. run: `git checkout master`
    1. run: `git pull`
1. mark all "Unreleased" changes to be in the version
    1. modify `HISTORY.md` by just adding a new headline right under the `## Unreleased`
       example:
       ```
       ## Unreleased

       ## 2.X.Y
       ```
    1. commit and push the changed `HISTORY.md` to master
        1. run ala `git commmit -m 'preparing 2.X.Y' HISTORY.md`
        1. run ala `git push origin master`
1. draft and publish a release on `master` branch in github
