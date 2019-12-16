# Release process

1. Get the latest.
    1. Run: `git checkout master`.
    1. Run: `git pull`.
1. Mark all "Unreleased" changes to be in the version
    1. Modify [`HISTORY.md`](HISTORY.md) by just adding a new headline right under the `## Unreleased`  
       so its right above te latest changes.
       Example:
       ```
       ## Unreleased

       ## 2.X.Y
       
       ### Changes
       * foo...
       * bar...
       ```
    1. Commit and push the changed `HISTORY.md` to master.
        1. Run ala `git commmit -m 'preparing 2.X.Y' HISTORY.md`.
        1. Run ala `git push origin master`.
1. Draft and publish a release on `master` branch in github.  
   Put the latest part of the [`HISTORY.md`](HISTORY.md) in the release notes.
