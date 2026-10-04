BASE = '''subject_definitions:
<Picture 1> Fixed 柳沟寺 study: door centered, paper window and desk left, bed right foreground.
<Picture 2> 孙生 (S1), late-20s scholar, gray-blue robe, same face and costume.
<Picture 3> 山魈 (S2), huge yellow-brown creature, giant mouth, sparse long teeth, clawed hands.

summary:
{summary}

retention_analysis:
Keep the exact room geometry and left/right anchors from the supplied references. Preserve character faces, costume, scale, and exits. Live-action historical cinema; no subtitles, logos, watermarks, modern objects, or extra human voices.

detailed_description:
{detail}

overall_soundscape:
{sound}

non_diegetic_music:
N/A - no score.'''

PROMPTS = [
BASE.format(summary='At dusk S1 is already alone inside the study, clears dust, lays bedding, and lights the lamp.', detail='[Shot 1] Start after S1 has entered: the centered door is empty and closed for the entire shot. Exactly one human, S1, crosses to the left desk, brushes dust, unfolds bedding on the right bed, and lights the oil lamp. Never show a doorway silhouette, duplicate person, reflection, family member, or creature. Slow track from desk to bed.', sound='Broom strokes, dust, cloth, wood, insects, and evening wind. S1 breathes quietly; no intelligible dialogue.'),
BASE.format(summary='Moonlit S1 sleeps on the right bed. The outer door opens by itself, then heavy boots approach.', detail='[Shot 1] Hold the same foot-of-bed axis. S1 sleeps facing left. The centered door swings open under mountain wind; the bedroom door opens inward and unseen boots stop outside. End before any creature enters. S1 is the only human.', sound='Night insects, hinges, low wind, and two heavy boot impacts. No intelligible dialogue.'),
BASE.format(summary='S2 enters through the centered door and towers over S1, surveying the room.', detail='[Shot 1] S2 bends under the centered lintel, straightens nearly to the beam, then turns its giant head left and right. S1 recoils on the right bed. S2 stays center-left; no family.', sound='Door groan, boot impacts, deep nonverbal throat resonance, cloth creaks. No intelligible demon words.'),
BASE.format(summary='S1 clearly draws the short knife, strikes S2 once, shouts, and S2 drags the quilt out through the door.', detail='[Shot 1] Close-up: S1 clearly draws a short metal knife from under the pillow; the blade remains visible. [Shot 2] One controlled thrust into S2 abdomen, hollow stone impact. S1 says (S1) <d>[Chinese] 妖物，退开！</d>. [Shot 3] S2 roars without words, catches the quilt, retreats through the centered door, and S1 falls beside the right bed. Absolutely no blood, no red liquid, no wound, no red stain, no gore; the bed and quilt stay clean.', sound='Knife draw and impact, nonverbal roar, claws scraping wood, quilt dragging. Only S1 speaks the single Chinese line.'),
BASE.format(summary='At dawn family members enter only through the left paper window and lift S1 to the bed.', detail='The third supplied reference is a locked S05 composition guide: preserve its family positions, left window entrance, wounded S1 on the floor, and fully closed center door. [Shot 1] Start after the family has entered through the left-rear paper lattice window. Exactly three indistinct family silhouettes remain on the left half of the room. Keep the centered wooden door completely shut, latched, and opaque for every frame; it is a static background anchor and nobody touches, approaches, crosses, or opens it. [Shot 2] The family carries a lamp and folded quilt only across the left half, with the camera framing the left window and desk more prominently; the closed center door remains visible at the far right edge. [Shot 3] They lift S1 from the floor to the right bed while staying clear of the door. Do not show an open doorway, exterior light through the center door, a person in the doorway, a demon, a door gap, or readable family dialogue.', sound='Dawn birds, hurried steps, lamp glass, muffled nonverbal gasps, paper and cloth movement, bed creak.'),
BASE.format(summary='The family examines five claw punctures on the same door and quilt fibers in its gap.', detail='[Shot 1] Push from bed to centered door, revealing quilt wedged in the seam. [Shot 2] Macro five deep claw marks like a basket, splinters and fibers. [Shot 3] S1 reaches and pulls back. No blood or demon.', sound='Room tone, cloth pull, tiny splinters, restrained breathing, morning wind.'),
BASE.format(summary='S1 straps his satchel, takes books, and leaves through the centered door.', detail='[Shot 1] S1 collects books from the left desk and glances at the marked door. [Shot 2] He crosses left-to-center and exits once through it. Camera holds on empty bed and marks; no re-entry.', sound='Books, satchel leather, footfalls, latch, birds, fading breeze.'),
BASE.format(summary='The empty room holds on the claw-marked door as wind moves the curtain and lamp flame, then fades out.', detail='[Shot 1] Locked wide frame of the empty study. Curtain at left window lifts, oil flame leans, centered marked door stays closed. Hold, then fade to black. No human or demon appears.', sound='Mountain wind, curtain fabric, faint lamp hiss, distant birds. No intelligible dialogue.'),
]
