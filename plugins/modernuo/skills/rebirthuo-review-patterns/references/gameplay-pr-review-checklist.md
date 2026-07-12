# Gameplay PR Review Checklist

Use this alongside the umbrella skill for RebirthUO/ModernUO gameplay pull requests.

## Verification pattern

1. Capture PR metadata, Definition of Done, changed files, existing reviews/comments, and CI status with explicit `-R RebirthUO/ModernUO`.
2. Fetch the PR head into an isolated worktree; keep the user's active branch untouched.
3. Run the build and the claimed focused tests from the PR worktree. Record focused results separately from broad-suite results.
4. Trace every changed damage path and lifecycle hook. Pay special attention to values that are changed immediately but consumed later by timers, restoration logic, or delayed damage callbacks.
5. Independently calculate sequence boundaries from the code and compare them to the PR description. Test the first/last value in every phase, cap duration, reset trigger, and first post-reset value.
6. Review PvP/PvM side effects and identify whether the change alters risk/reward, counterplay, or persistent health/state.

## Findings pattern

A blocking gameplay finding should include:

- exact file and line anchor;
- the current value flow or boundary calculation;
- the player-visible consequence;
- the smallest safe correction direction;
- a regression test requirement.

Do not treat five focused tests as proof that delayed restoration, logout/death cleanup, or actual damage integration works.

## Item-property and target-state audit additions

- Reconstruct tooltip order across the full inheritance chain. `AddNameProperties()` usually emits weight/name first, while inherited attribute containers emit stats later; a new item’s own method is not enough to prove client order.
- Compare every `Core.*` gate with both presentation and mechanics. Hiding a special property before its era does not automatically disable generic attributes assigned by the constructor; test a qualifying behavior on the earlier expansion, not only a non-qualifying spell.
- For state stored on an equipped item and keyed by a target, inspect both the caster’s lifecycle and the target’s lifecycle. A target death/deletion event normally passes the target, so an item on the caster will not be found unless the implementation explicitly links or clears it. Distinguish immediate event cleanup from lazy reset on the next damage attempt.
- If buffs are guarded by `PlayerMobile`, plain `Mobile` fixtures only prove formula/state transitions. Add a real `PlayerMobile` fixture for buff creation, removal, logout, death, and unequip.
- Before final comments, repeat `git status --short --branch`, `git log -1`, and `git diff origin/main`; a concurrent commit can invalidate earlier line anchors and test-scope claims.

## GitHub publication

If the authenticated account owns the PR, `gh pr review --request-changes` is rejected by GitHub. Publish a top-level `Code Review Summary` comment instead, stating that it is not a formal review, then read the comment back and verify the returned URL.
