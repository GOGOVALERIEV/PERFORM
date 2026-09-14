import sys, io, os, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

videos_dir = r'C:\Users\User\Desktop\project-test\downloads\videos'

scripts_info = [
    {
        'name': 'Script 70',
        'dec_ids': 'Dec 336-341',
        'folder': 'Script 70 - Dec 336-341',
        'clickup': 'Script 70 - WLC FB Winners re-done to Youtube (Oct 416-417) / (Dec 336-341)',
        'videos': [
            ('Dec336', 'H1', 'December 336 2025 FB - WLC Redone S70 H1.mp4'),
            ('Dec337', 'H2', 'December 337 2025 FB - WLC Redone S70 H2.mp4'),
            ('Dec338', 'H3', 'December 338 2025 FB - WLC Redone S70 H3.mp4'),
            ('Dec339', 'H4', 'December 339 2025 FB - WLC Redone S70 H4.mp4'),
            ('Dec340', 'H5', 'December 340 2025 FB - WLC Redone S70 H5.mp4'),
            ('Dec341', 'BODY', 'December 341 2025 FB - WLC Redone S70 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 71',
        'dec_ids': 'Dec 342-347',
        'folder': 'Script 71 - Dec 342-347',
        'clickup': 'Script 71 - WLC - FB Winners re-done to Youtube (Oct 415) / (Dec 342-347)',
        'videos': [
            ('Dec342', 'H1', 'December 342 2025 FB - WLC Redone S71 H1.mp4'),
            ('Dec343', 'H2', 'December 343 2025 FB - WLC Redone S71 H2.mp4'),
            ('Dec344', 'H3', 'December 344 2025 FB - WLC Redone S71 H3.mp4'),
            ('Dec345', 'H4', 'December 345 2025 FB - WLC Redone S71 H4.mp4'),
            ('Dec346', 'H5', 'December 346 2025 FB - WLC Redone S71 H5.mp4'),
            ('Dec347', 'BODY', 'December 347 2025 FB - WLC Redone S71 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 72',
        'dec_ids': 'Dec 348-353',
        'folder': 'Script 72 - Dec 348-353',
        'clickup': 'Script 72 - WLC - FB Winners re-done to Youtube Sept 190(Nov 180-181) / (Dec 348-353)',
        'videos': [
            ('Dec348', 'H1', 'December 348 2025 FB - WLC Redone S72 H1.mp4'),
            ('Dec349', 'H2', 'December 349 2025 FB - WLC Redone S72 H2.mp4'),
            ('Dec350', 'H3', 'December 350 2025 FB - WLC Redone S72 H3.mp4'),
            ('Dec351', 'H4', 'December 351 2025 FB - WLC Redone S72 H4.mp4'),
            ('Dec352', 'H5', 'December 352 2025 FB - WLC Redone S72 H5.mp4'),
            ('Dec353', 'BODY', 'December 353 2025 FB - WLC Redone S72 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 73',
        'dec_ids': 'Dec 354-359',
        'folder': 'Script 73 - Dec 354-359',
        'clickup': 'Script 73 - WLC - FB Winners re-done to Youtube Sept 197 (Nov 178-179) / (Dec 354-359)',
        'videos': [
            ('Dec354', 'H1', 'December 354 2025 FB - WLC Redone S73 H1.mp4'),
            ('Dec355', 'H2', 'December 355 2025 FB - WLC Redone S73 H2.mp4'),
            ('Dec356', 'H3', 'December 356 2025 FB - WLC Redone S73 H3.mp4'),
            ('Dec357', 'H4', 'December 357 2025 FB - WLC Redone S73 H4.mp4'),
            ('Dec358', 'H5', 'December 358 2025 FB - WLC Redone S73 H5.mp4'),
            ('Dec359', 'BODY', 'December 359 2025 FB - WLC Redone S73 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 75',
        'dec_ids': 'Dec 360-365',
        'folder': 'Script 75 - Dec 360-365',
        'clickup': 'Script 75 - WLC - FB Winners re-done to Youtube Sept 341 (Dec 360-365)',
        'videos': [
            ('Dec360', 'H1', 'December 360 2025 FB - WLC Redone S75 H1.mp4'),
            ('Dec361', 'H2', 'December 361 2025 FB - WLC Redone S75 H2.mp4'),
            ('Dec362', 'H3', 'December 362 2025 FB - WLC Redone S75 H3.mp4'),
            ('Dec363', 'H4', 'December 363 2025 FB - WLC Redone S75 H4.mp4'),
            ('Dec364', 'H5', 'December 364 2025 FB - WLC Redone S75 H5.mp4'),
            ('Dec365', 'BODY', 'December 365 2025 FB - WLC Redone S75 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 77',
        'dec_ids': 'Dec 372-377',
        'folder': 'Script 77 - Dec 372-377',
        'clickup': 'Script 77 - WLC - FB Winners re-done to Youtube Sept 343 (Dec 372-377)',
        'videos': [
            ('Dec372', 'H1', 'December 372 2025 FB - WLC Redone S77 H1.mp4'),
            ('Dec373', 'H2', 'December 373 2025 FB - WLC Redone S77 H2.mp4'),
            ('Dec374', 'H3', 'December 374 2025 FB - WLC Redone S77 H3.mp4'),
            ('Dec375', 'H4', 'December 375 2025 FB - WLC Redone S77 H4.mp4'),
            ('Dec376', 'H5', 'December 376 2025 FB - WLC Redone S77 H5.mp4'),
            ('Dec377', 'BODY', 'December 377 2025 FB - WLC Redone S77 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 78',
        'dec_ids': 'Dec 378-383',
        'folder': 'Script 78 - Dec 378-383',
        'clickup': 'Script 78 - WLC - FB Winners re-done to Youtube (Oct 3) / (Dec 378-383)',
        'videos': [
            ('Dec378', 'H1', 'December 378 2025 FB - WVH Redone S78 H1.mp4'),
            ('Dec379', 'H2', 'December 379 2025 FB - WVH Redone S78 H2.mp4'),
            ('Dec380', 'H3', 'December 380 2025 FB - WVH Redone S78 H3.mp4'),
            ('Dec381', 'H4', 'December 381 2025 FB - WVH Redone S78 H4.mp4'),
            ('Dec382', 'H5', 'December 382 2025 FB - WVH Redone S78 H5.mp4'),
            ('Dec383', 'BODY', 'December 383 2025 FB - WVH Redone S78 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 79',
        'dec_ids': 'Dec 474-479',
        'folder': 'Script 79 - Dec 474-479',
        'clickup': 'Script 79 - WLC - FB Winners re-done to Youtube (Oct 86) / Dec 747-479 [TYPO: actual is Dec 474-479]',
        'videos': [
            ('Dec474', 'H1', 'December 474 2025 FB - WLC Redone S79 H1.mp4'),
            ('Dec475', 'H2', 'December 475 2025 FB - WLC Redone S79 H2.mp4'),
            ('Dec476', 'H3', 'December 476 2025 FB - WLC Redone S79 H3.mp4'),
            ('Dec477', 'H4', 'December 477 2025 FB - WLC Redone S79 H4.mp4'),
            ('Dec478', 'H5', 'December 478 2025 FB - WLC Redone S79 H5.mp4'),
            ('Dec479', 'BODY', 'December 479 2025 FB - WLC Redone S79 BODY.mp4'),
        ],
    },
    {
        'name': 'Script 140',
        'dec_ids': 'Dec 790-797',
        'folder': 'Script 140 - Dec 790-797',
        'clickup': 'Script 140 (S107) V2 - WLC - FB Version V2 (Dec 790-797)',
        'videos': [
            ('Dec790', 'H1', 'December 790 2025 FB - WLC New Script S140 H1.mp4'),
            ('Dec791', 'H2', 'December 791 2025 FB - WLC New Script S140 H2.mp4'),
            ('Dec792', 'H3', 'December 792 2025 FB - WLC New Script S140 H3.mp4'),
            ('Dec793', 'H4', 'December 793 2025 FB - WLC New Script S140 H4.mp4'),
            ('Dec794', 'H5', 'December 794 2025 FB - WLC New Script S140 H5.mp4'),
            ('Dec795', 'H6', 'December 795 2025 FB - WLC New Script S140 H6.mp4'),
            ('Dec796', 'H7', 'December 796 2025 FB - WLC New Script S140 H7.mp4'),
            ('Dec797', 'BODY', 'December 797 2025 FB - WLC New Script S140 BODY.mp4'),
        ],
    },
]

# Build the guide
guide = """# VIDEO ADS UPLOAD GUIDE - WLC Non Creator
# Generated: March 10, 2026
# Campaign: "Testing | LC | CBO | Jan 2026 | WLC Olavita SF | Non Creator VSL | V2"

# ============================================================
# SUMMARY
# ============================================================

Tasks ready: 9 out of 10 (Script 76 has no FB videos - ask Badar)
Total videos: 56
Total ads to create: 112 (each video x 2 headlines, same TC)
Editor: Jade
Writer: Joseph
Schedule: March 11, 12:00 AM
All ad sets: DEACTIVATED (OFF)

# ============================================================
# THINGS TO ASK BADAR BEFORE STARTING
# ============================================================

1. AD NAMING FORMAT - What's the exact format for video ad names?
   Best guess based on cheatsheet:
   {AdID} {BatchDate} TC1 {HL#} Jade Joseph Non Creator VSL TOF WLC {Angle} {Offer} Noor Skin USA

   UNKNOWN PARTS (Badar must provide):
   - BatchDate: "Dec11"? "Dec15"? "Dec28"?
   - Angle: What angle for each script?
   - Offer: Badar always provides this
   - Destination URL: Badar always provides this

2. SCRIPT 76 - No FB videos exist, only YT. Skip or use YT?

3. SCRIPT 79 - ClickUp says "Dec 747-479" but files are Dec 474-479. Confirm.

4. HOW MANY AD SETS? One per script? One big one?
   Best guess: 1 ad set per script (12 ads each, well under the 50 max)

# ============================================================
# HOW THE 2 HEADLINES WORK
# ============================================================

Each script has:
- Several videos (6 or 8)
- 1 Primary Text (TC1) - SAME for every ad in that script
- 2 Headlines (HL1 and HL2) - each video gets BOTH

Example with 6 videos:
  Video 1 + TC1 + HL1 = Ad 1
  Video 1 + TC1 + HL2 = Ad 2
  Video 2 + TC1 + HL1 = Ad 3
  Video 2 + TC1 + HL2 = Ad 4
  ...
  Video 6 + TC1 + HL1 = Ad 11
  Video 6 + TC1 + HL2 = Ad 12

Total: 6 videos x 2 headlines = 12 ads per script

# ============================================================
# STEP-BY-STEP: HOW TO BUILD ADS IN META
# ============================================================

DO THIS FOR EACH SCRIPT (repeat 9 times):

STEP 1: Upload videos to Media Library
  - Meta Ads Manager > All Tools > Media Library
  - Find or create folder: WLC 2026 > Non Creator VSL
  - Upload the 6 (or 8) videos for this script
  - TIP: Upload from the script folder on your PC

STEP 2: Find the campaign
  - Campaign: "Testing | LC | CBO | Jan 2026 | WLC Olavita SF | Non Creator VSL | V2"

STEP 3: Duplicate an existing ad set
  - Find an existing ad set inside this campaign
  - Duplicate it (preserves all settings like pixel, targeting, etc.)
  - Press F5 (refresh) IMMEDIATELY after duplicating
  - TEMPLATE TRICK: Duplicate TWICE — one to work in, one as clean template

STEP 4: Rename ad set + set schedule
  - Rename: Testing CBO | WLC [Angle] | Batch[Date] | V1
    (Angle and Date from Badar)
  - Set start date: March 11, 12:00 AM (00:00)
  - Keep ad set OFF

STEP 5: Build 1 perfect ad with HL1
  - Set the first video from Media Library
  - Open PRIMARY_TEXT_TC1.txt from the script folder > copy-paste into Primary Text
  - Open HEADLINES.txt > copy HEADLINE 1 > paste into Headline field
  - Set destination URL (from Badar)
  - Turn OFF Advantage+ creative text generation
  - Turn OFF Ad Creative Enhancements
  - Turn OFF Personalized Destination
  - Turn OFF Multi-advertiser ads
  - Name the ad (format from Badar)

STEP 6: Duplicate for all videos with HL1
  - Ctrl+D to duplicate
  - Change the video on each copy (one by one - bulk doesn't work for media)
  - Change the Ad ID in each name (Dec336, Dec337, etc.)
  - Remove "- Copy" from every name
  - You now have 6 ads (or 8 for Script 140), all with HL1

STEP 7: Duplicate ALL ads and switch to HL2
  - Select ALL 6 (or 8) ads you just made
  - Ctrl+D to duplicate them all
  - On each copy: change Headline text to HL2 (from HEADLINES.txt)
  - On each copy: change HL1 to HL2 in the ad name
  - Remove "- Copy" from every name
  - You now have 12 ads (or 16 for Script 140)

STEP 8: QA Checklist (check EVERY ad)
  [ ] Ad set start date = March 11, 12:00 AM?
  [ ] Ad set name correct (no "- Copy")?
  [ ] Every ad has the CORRECT video (not all the same)?
  [ ] Every ad name has correct Ad ID and HL#?
  [ ] TC1 is the same on all ads?
  [ ] HL1 ads have HL1 text, HL2 ads have HL2 text?
  [ ] Destination URL correct?
  [ ] Advantage+ Creative = OFF?
  [ ] Ad Creative Enhancements = OFF?
  [ ] Personalized Destination = OFF?
  [ ] Multi-advertiser ads = OFF?
  [ ] Ad set is DEACTIVATED / OFF?

STEP 9: PUBLISH
  - Click Publish at the bottom
  - This SAVES your work — it does NOT make anything go live
  - If you don't Publish, ALL your work is LOST

STEP 10: Next script
  - Go back to your clean template ad set
  - Duplicate it for the next script
  - Repeat Steps 4-9

STEP 11: When all 9 scripts are done, message Badar
  - List all ad set names you created
  - Say "All OFF for QA"
  - Mention Script 76 (no FB videos)

# ============================================================
# META TIPS & TRICKS (from your experience)
# ============================================================

- Use Edge browser for Meta (not Brave — Shields causes issues)
- Type text in Notepad first, then paste into Meta (avoids typing lag)
- "J" trick: type one letter first to activate Meta's text field, then paste
- If fields freeze: refresh (F5), close extra tabs, try Edge
- Table view is better for managing ads (sidebar cuts off names)
- ALWAYS Publish to save — even if ad set is OFF
- Press F5 after every duplication before editing
- Max 50 ads per ad set — create V2 if you go over (you won't here)

# ============================================================
# TASK-BY-TASK DETAILS
# ============================================================
"""

for s in scripts_info:
    # Read headlines
    hl_path = os.path.join(videos_dir, s['folder'], 'HEADLINES.txt')
    with open(hl_path, 'r', encoding='utf-8') as f:
        hl_content = f.read()

    lines = hl_content.strip().split('\n')
    hl1 = hl2 = ''
    for i, line in enumerate(lines):
        if line.startswith('HEADLINE 1:') and i+1 < len(lines):
            hl1 = lines[i+1].strip()
        if line.startswith('HEADLINE 2:') and i+1 < len(lines):
            hl2 = lines[i+1].strip()

    num_videos = len(s['videos'])
    num_ads = num_videos * 2

    guide += f"""
## {s['name']} ({s['dec_ids']})
----------------------------------------------
ClickUp task: {s['clickup']}
Folder on PC: downloads/videos/{s['folder']}/
Videos: {num_videos}
Ads to create: {num_ads}

HEADLINE 1: {hl1}
HEADLINE 2: {hl2}
TC1: Open PRIMARY_TEXT_TC1.txt in the folder - copy entire contents

VIDEOS IN THIS TASK:
"""
    for dec_id, hook, filename in s['videos']:
        guide += f"  {dec_id} ({hook}): {filename}\n"

    guide += f"""
ADS TO BUILD (video + headline combo):
"""
    ad_num = 1
    for hl_label, hl_text in [('HL1', hl1), ('HL2', hl2)]:
        for dec_id, hook, filename in s['videos']:
            guide += f"  Ad {ad_num:3d}: {dec_id} ({hook}) + TC1 + {hl_label}\n"
            ad_num += 1

    guide += "\n"

guide += """
# ============================================================
# GRAND TOTAL
# ============================================================

Script 70:  6 videos x 2 HL = 12 ads
Script 71:  6 videos x 2 HL = 12 ads
Script 72:  6 videos x 2 HL = 12 ads
Script 73:  6 videos x 2 HL = 12 ads
Script 75:  6 videos x 2 HL = 12 ads
Script 77:  6 videos x 2 HL = 12 ads
Script 78:  6 videos x 2 HL = 12 ads
Script 79:  6 videos x 2 HL = 12 ads
Script 140: 8 videos x 2 HL = 16 ads
---------------------------------
TOTAL: 56 videos, 112 ads, 9 ad sets

Script 76: WAITING ON BADAR (no FB videos)
"""

# Save
guide_path = os.path.join(videos_dir, 'UPLOAD_GUIDE.txt')
with open(guide_path, 'w', encoding='utf-8') as f:
    f.write(guide)

print(f'Guide saved to: {guide_path}')
print(f'Total length: {len(guide)} chars, {guide.count(chr(10))} lines')
