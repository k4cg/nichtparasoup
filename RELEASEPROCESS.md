# Release process

1. Get the latest code.
   1. Run: `git checkout master`.
   1. Run: `git pull`.
1. Prepare the new release
   1. Run ala: `git checkout -b release/2.X.Y`
   1. Mark all "Unreleased" changes to be in the version
      1. Modify [`HISTORY.md`](HISTORY.md) by just adding a new headline right under the
         `## Unreleased`  so its right above te latest changes.
         Example ala:
         ```
         ## Unreleased

         ## 2.X.Y

         * Changes
           * foo...
           * bar...
         ```
   1. Run ala: `git commmit -m 'preparing 2.X.Y' HISTORY.md`.
   1. Run: `git push origin`.
1. Merge release branch into "master" branch.
   1. Create a PullRequest from the release branch to "master" branch on github.
   1. Approve the PullRequest and merge it to "master" branch on github.
1. Draft and publish a release on "master" branch in github.  
   Put the latest part of the [`HISTORY.md`](HISTORY.md) in the release notes.
