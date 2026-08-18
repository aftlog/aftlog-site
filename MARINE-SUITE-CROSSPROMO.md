# Marine Suite — Cross-Promotion Spec (canonical)

> Owner: Louis · Apps: AftLog + CatchTales · No Flutter code here — copy + placement rules only.

## 1 · Marine Suite brand description (the ONLY one for About/Help)
```
AftLog handles your boat — maintenance, safety, and trip prep.
CatchTales handles your fishing — species, spots, and conditions.
Together, they make a full day on the water easier.
```
This is the entire Marine Suite identity. No more. No less.
It preserves the independence of both apps.

## 2 · AftLog → CatchTales (in-app hooks)
**Placement rules:** only where fishing context naturally exists; only when the user is
already doing something trip-related. Always one line, optional, contextual.
**Never:** Pro/pricing/purchase screens · maintenance logs · engine or safety-critical
workflows · offline-first warnings.
- **Trip Log:** "Tracking a trip? CatchTales handles the fishing side — species, spots, and conditions."
- **Fuel Log:** "Planning a day on the water? CatchTales keeps the fishing details organized."
- **Checklists:** "Packing gear? CatchTales keeps tackle, bait, and spots organized for the day."
- **Weather / Float Plan:** "Checking conditions? CatchTales adds solunar, tide, and bite score for the fishing side."
- **Ramp / Launch Prep:** "Launching today? CatchTales tracks fishing spots and conditions once you're out there."
- **Safety Tools (optional, very subtle):** "After the boat's ready, CatchTales can track the fishing part of your trip."

## 3 · CatchTales → AftLog (in-app hooks)
**Placement rules:** only where boat context exists; never assume the user owns a boat.
Always one line, optional, contextual.
**Never:** species/catches/tally/community screens · Pro/subscription screens · AI Fish ID · photo/camera workflows.
- **Launch / Ramp Details:** "Launching from a ramp? AftLog handles boat prep, ramp checks, and compliance."
- **Weather / Conditions:** "Checking conditions? AftLog covers float-plan and safety for the boat side."
- **Gear Prep / Tackle Box:** "Getting ready for a day out? AftLog keeps boat checklists and maintenance organized."
- **Fishing Spots / Map:** "Heading to a spot? AftLog tracks trips, fuel, and boat logs for the day."
- **Trip / Session Start:** "Starting a session? AftLog handles the boat — maintenance, safety, and trip prep."

## 4 · Web portal (already shipped in aftlog-site)
- `/catchtales.html` overview page (hero, feature grid, Works-with-AftLog, download placeholder).
- Footer strip + Marine Suite footer column (site-wide, incl. static index/updates).
- Help sidebar Marine Suite block.
- Inline promo cards on: Trip & Fuel Log, Checklists, Float Plan.
- All use the Marine Suite description above; copy-lint clean; site_check green.
