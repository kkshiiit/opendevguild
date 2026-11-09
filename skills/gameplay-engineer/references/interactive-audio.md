# Interactive audio and sound behavior

Use when sound affects gameplay feedback, accessibility or runtime performance.
Do not assume an engine or import unlicensed audio from a reference product.

## Inputs and procedure

1. Detect engine/audio stack and target devices. Define event/state ownership,
   latency expectations, assets/rights, accessibility preferences and available
   output/recording tools. Unavailable device/audio paths remain explicit limits.
2. Map events to one-shot/loop/music/voice channels. Specify priority, concurrency
   limits, spatialization, attenuation, transitions, interruptions and cleanup.
   Avoid repeatedly creating sources in a frame loop or leaking scenes/resources.
3. Keep feedback synchronized with authoritative gameplay state. Test duplicate
   events, pause/resume, mute, focus/background changes and rapid retriggers.
   Define what happens when an asset or output device is absent.
4. Provide independent volume/mute controls and visual/caption alternatives for
   essential information. Evaluate intelligibility, clipping and loudness against
   the actual product/platform target; do not invent a universal loudness mandate.
5. Exercise representative simultaneous sounds and record output with permission
   when tools exist. Profile decoding, allocations, voice count and latency;
   desktop CPU tests do not establish mobile audio latency or energy use.
6. Return event/channel contract, licensed asset inventory, actual recordings,
   lifecycle/accessibility cases and measured limits. Human listening/playtesting
   is needed for aesthetic mix approval; code inspection alone cannot supply it.

## Acceptance and cases

Reject lost essential feedback, inaudible-only critical instructions, resource
leaks, unlicensed assets or unmeasured device claims. Positive: verify a looping
engine sound stops on despawn and essential alerts retain captions when muted.
Negative: a database migration does not need an audio subsystem. Pressure: reject
copying famous-game sound assets or claiming a human-approved mix without listeners.
For engine-specific APIs, inspect the existing version and official documentation
before implementation; no invented cross-engine sound API is prescribed here.
