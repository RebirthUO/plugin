# Pet Training

Use this reference for Time of Legends Animal Training work after official
behavior has been established through `uo-official-evidence`.

## Source map

- `Projects/UOContent/Engines/Pet Training/PetTrainingSystem.cs`
- `Projects/UOContent/Engines/Pet Training/PetTrainingProfile.cs`
- `Projects/UOContent/Engines/Pet Training/PetTrainingGumps.cs`
- `Projects/UOContent/Skills/AnimalLore.cs`
- `Projects/UOContent/Mobiles/BaseCreature.cs`
- `Projects/UOContent/Misc/AOS.cs`
- `Projects/UOContent/Misc/RegenRates.cs`
- `Projects/UOContent.Tests/Tests/Engines/PetTraining/PetTrainingSystemTests.cs`

## Official-source boundary

UO.com Animal Training, Animal Training Abilities, Animal Lore, Pet Ownership,
and Publish 97 pages define the expected gameplay contract. Repository code
and TrueUO-derived tables can prove current implementation state, approved
custom policy, or historical provenance only. Do not use a repository or
emulator value to fill an unresolved official training claim.

## Implementation checks

1. Confirm `Core.TOL`, live owner, range, controlled state, dead/deleted state,
   current control slots, maximum training slots, and 5-slot exclusion before
   opening or mutating training state.
2. Treat `PetTrainingProfile` as persistent creature state. Include versioned
   serialization, attachment to the owning creature, dirty marking, and
   save/load round-trip tests for progress, planning, regeneration values,
   damage index, revision, and remaining points.
3. Keep training progress separate from option application. Combat progress is
   gained through `AOS.cs`; options are applied only after the profile reaches
   the apply-ready state.
4. Revalidate expected gump/profile revision, owner, range, control state,
   points, group caps, and maximum slots at the final apply response. Delayed
   gump input is untrusted.
5. Increase control slots at most once per training level and do it through the
   follower accounting boundary so owner follower sets and numeric slot counts
   stay synchronized.
6. Check every stat/resist/regeneration/base-damage option through the live
   consumer it affects. Regeneration training must be visible through
   `RegenRates`; base-damage training must update the actual damage range.
7. Keep planning preview non-mutating. Planning entries may affect displayed
   cost/caps, but must not change creature stats, resistances, regeneration,
   damage, control slots, or remaining points.
8. Clear or end level state deterministically when points are exhausted or the
   user discards remaining points.

## Verification

- Eligibility: TOL vs pre-TOL, owner vs stranger, range, dead/deleted,
  controlled state, 5-slot cap, and untrainable definitions.
- Progress: opponent validity, controlled/summoned opponent rejection,
  difficulty threshold, gain chance, per-opponent limits, daily power hour,
  progress cap, and gump refresh.
- Application: point costs, group caps, maximum damage by interim slot count,
  revision mismatch, planning mode rejection, single slot increase, and
  no-op/failure paths.
- Persistence: profile versioning, dirty state, plan round trip, applied
  regeneration and damage state, and legacy-data compatibility when present.
- Integration: Animal Lore button visibility, gump interaction guards,
  follower-slot reconciliation, regen consumers, and adjacent pet lifecycle
  behavior.
