# {{name}}

- **Slug:** `{{slug}}`
- **Kind:** {{character | npc | companion}}
- **Role:** {{role}}
- **Allegiance:** {{allegiance}}
- **Status:** {{active | downed | out | dead | retired}}
- **First Impression:** {{first_impression}}
- **Signature Gear:** {{signature_gear}}
- **Leverage:** {{leverage}}
- **Threat Level:** {{threat_level}}

## Stats

Use the active flavor pack's stat labels. Six slots cover the native packs; unused slots become `-` or `0`.

- **{{STAT_1}}:** {{stat_1}}
- **{{STAT_2}}:** {{stat_2}}
- **{{STAT_3}}:** {{stat_3}}
- **{{STAT_4}}:** {{stat_4}}
- **{{STAT_5}}:** {{stat_5}}
- **{{STAT_6}}:** {{stat_6}}

## Derived

- **HP:** {{hp}}
- **Defense:** {{defense}}
- **Stress:** {{stress}}
- **Reputation:** 0

## Skills

List each skill the character actually uses, formatted as `- **STAT/Skill** rank N`.

- **{{STAT}}/{{Skill}}** rank {{rank}}

## Inventory

- {{inventory_item}}

## Special Features

- {{special_feature}}

## Progression

- **Level:** 1
- **XP:** 0
- **XP to Next Level:** 10
- **XP Log:**
  - +0 {{reason}} ({{utc_now}})

## Skill Entries

Use one subsection per skill that needs a full writeup (frequency, effect, limitations). Skip the heading for skills that are just stat+rank.

### {{STAT}}/{{Skill}}

- **Rank:** {{rank}}
- **Description:** {{description}}
- **Frequency:** {{frequency}}
- **Effect:** {{effect}}
- **Limitations:** {{limitations}}

## Hooks

- {{hooks}}

## Secrets

GM-only links back into `secrets.md`. The bullet here is a pointer, not the secret itself.

- See `../secrets.md` → {{secret_title}}

## Relationship To Crew

{{relationship}}

## Session Notes

Free-form running notes for the GM. Use dated bullets so changes track over the campaign.

- {{utc_now}} — {{session_notes}}
