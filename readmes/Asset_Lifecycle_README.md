# Asset Lifecycle

## What this part owns

Everything that happens to an asset from the moment it's registered until it's
retired: registration, allocation, transfers, and maintenance. If it changes an
asset's status, it belongs here.

---

## The four modules, and how they connect

```
Assets        →  the asset itself: register it, search it, track its status
Allocations   →  who currently holds an asset
Transfers     →  moving an asset from one holder to another
Maintenance   →  taking an asset out of service to repair it, then back in
```

Allocations, Transfers, and Maintenance all depend on Assets existing first —
they all change an asset's status, so Assets has to be built before the others
can plug into it.

---

## The asset state machine (the core rule of this whole module)

An asset can only move between statuses in specific ways:

```
Available → Allocated → Returned → Available
Available → Under Maintenance → Available
Available → Reserved → Allocated
```

The rule to hold onto: **no other part of the code is allowed to change an
asset's status directly.** Every module — Allocation, Transfer, Maintenance —
has to go through one single function that checks "is this move actually
allowed?" before changing anything. That's what keeps the state machine real
instead of just a diagram nobody follows.

---

## Step 1 — Build the Assets module

This comes first because everything else points back to it.

1. Define what an asset looks like in the database: name, tag, category,
   status, location, and so on.
2. Write down the state machine rules as data (a simple table of "from this
   status, you can go to these statuses") rather than scattering `if`
   statements everywhere.
3. Write the piece that generates asset tags automatically (`AF-0001`,
   `AF-0002`...) so two people registering assets at the same time never
   collide.
4. Write the function that changes an asset's status — and make it the
   *only* place in the code that's allowed to do that.
5. Write the endpoints: list/search assets, get one asset, register a new
   one, update one, delete (retire) one, view an asset's full history, get
   its QR code.
6. Try it out: register an asset, search for it, try an invalid status
   change and make sure it gets rejected.

---

## Step 2 — Build the Allocations module

This is where "who currently has this asset" lives.

1. Define what an allocation looks like: which asset, who it's allocated to
   (a person or a department), when it's expected back.
2. Add a database-level guarantee that an asset can only have **one active
   allocation at a time** — this is your real defense against double
   allocation, not just a check in your code that could be skipped.
3. Write the "allocate" action: check if the asset is already allocated to
   someone. If it is, don't allow it — instead, tell the caller who
   currently holds it, so the frontend can offer a "Request Transfer"
   button.
4. Write the "return" action: close out the allocation, record the
   condition it came back in, and flip the asset back to Available.
5. Write an endpoint that lists overdue allocations — anything past its
   expected return date.
6. Try it out: allocate an asset, try allocating it again to someone else,
   confirm you get blocked and told who has it.

---

## Step 3 — Build the Transfers module

This handles moving an asset from one holder to another without a manual
return-then-reallocate step.

1. Define what a transfer request looks like: which asset, current holder,
   requested new holder, and its status (requested, approved, rejected,
   completed, cancelled).
2. Write the "request transfer" action — only allowed if the asset is
   currently allocated to someone (you can't transfer an asset nobody
   holds).
3. Write the "approve" action — this closes the old allocation and opens a
   new one for the new holder, reusing the allocation logic from Step 2
   rather than duplicating it.
4. Write "reject" and "cancel" actions. Cancel should only work for the
   person who originally made the request.
5. Try it out: request a transfer, approve it, and confirm the asset's
   history shows the old allocation closed and a new one opened.

---

## Step 4 — Build the Maintenance module

This handles taking an asset out of service and bringing it back.

1. Define what a maintenance request looks like: which asset, who raised
   it, priority, and its status (pending, approved, rejected, assigned,
   in progress, resolved).
2. Write the "raise request" action — this does not change the asset's
   status yet, it just logs the issue.
3. Write the "approve" action — this is the only point where the asset's
   status flips to Under Maintenance. Work should never start before
   approval.
4. Write "reject," "assign technician," and "start" actions.
5. Write the "resolve" action — this is the only point where the asset's
   status flips back to Available.
6. Try it out: raise a request, try to skip straight to "in progress"
   without approval and confirm it's blocked, then approve it properly and
   watch the asset's status change.

---

## Step 5 — Tie it all together

1. Make sure every action across all four modules — register, allocate,
   return, transfer, maintenance approval — writes an entry to the
   activity log, so there's always a record of who did what and when.
2. Make sure every meaningful action sends a notification (asset assigned,
   transfer approved, maintenance resolved, overdue return). You'll likely
   just call into the Notifications module someone else owns, not build
   notifications yourself.
3. Make list endpoints consistent — same pagination style across Assets,
   Allocations, Transfers, and Maintenance.

---

## Step 6 — Test the things that actually get checked

1. Try to allocate an asset that's already allocated — confirm you get
   blocked with the current holder's name.
2. Try to book overlapping maintenance/allocation states — confirm the
   state machine rejects invalid moves.
3. Walk through a full transfer: request → approve → confirm the new
   holder shows up and the old allocation is properly closed.
4. Walk through a full maintenance cycle: raise → approve → resolve —
   confirm the asset's status changes at exactly the right points and
   nowhere else.

---

## The one thing to remember through all four modules

Every module follows the same shape:

```
Model        →  what the data looks like
Schema       →  what goes in and out of the API
Repository   →  how it's fetched/saved in the database
Service      →  the rules for what's allowed to happen
Controller   →  the actual endpoint someone calls
```

And the golden rule that ties all four modules together: **only the Asset
service is allowed to change an asset's status.** Allocation, Transfer, and
Maintenance all ask it to make the change on their behalf — none of them
touch the status field directly.


## gaps to be covered 
```❌ GET /{id}/history endpoint — asset's full allocation + maintenance history — missing
❌ GET /{id}/qrcode endpoint — QR code generation — missing

"Add a database-level guarantee (unique constraint) that an asset can only have one active allocation at a time" — we currently enforce this only in code, not at DB level. A partial index is needed in the migration.
```