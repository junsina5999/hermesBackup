---
name: ai-image-prompt-authoring
description: Prompts for AI image edits, face swaps, style transfer.
tags: [image-generation, prompting, face-swap, style-transfer, gemini, flux]
---

# AI Image Prompt Authoring

Use when the user wants a prompt for an image model — putting someone's face into
a reference photo's style/pose/wardrobe, restyling a portrait, changing background
or clothing while keeping the subject, or asking "which site/model can do this".

Covers prompt construction, source-photo triage, model routing, and the failure
modes that make results look wrong.

## Language rules

- **Reply to the user in Persian** (their preference), but **write the prompt itself
  in English.** Image models follow English far more reliably. State this once;
  don't ask permission each time.
- Never rely on the model to render Persian/Arabic text inside an image — glyphs come
  out detached and malformed. Generate the image in English/textless, overlay Farsi
  afterward (see `persian-quote-images`).

## Workflow

1. **Get both images before writing the final prompt.** Subject photo(s) AND the
   style reference. A prompt written from the reference alone will not account for
   the subject's real features and the model will invent a face.
2. **Diff the subject against the reference** and show the user a short table:
   beard, glasses shape/color, hair length & volume, apparent age, face width.
   Every row that differs is a line the prompt must explicitly pin down, otherwise
   the model drifts the identity toward the reference.
3. **Triage which source photo to use** when several are offered — rank them and say
   which one, plainly, with reasons (see selection criteria below).
4. **Write the prompt** using the two-block structure below.
5. **Give exact execution steps**: which site, which model, upload order, and that
   upload order matters because the prompt says "image 1" / "image 2".
6. **Pre-arm the user with fix-up lines** for the 2–3 most likely drifts, so they can
   iterate without coming back.

## Source photo selection criteria

Rank candidates on these, best first:

- **Frontal, at eye level.** Low-angle selfies (phone below the chin) widen the jaw
  and neck; the model reproduces that distortion. Prefer eye-level.
- **Face in sharp focus**, lit evenly, no heavy glare across the eyes.
- **Already close to the target style** — if the reference has a full beard, a subject
  photo with stubble transitions more naturally than a clean-shaven one. Same for hair
  volume.
- **Plain / blown-out background** — easier subject isolation.

### Mirrored selfie pitfall

Front-camera selfies are frequently saved un-flipped. Tell: **text reads backwards**
(brand tab, logo, signage). If mirrored, have the user flip horizontally before upload,
otherwise the face is rebuilt with reversed asymmetry and stops looking like them.

## Prompt structure: two hard-separated blocks

Identity-preserving edits work best as an explicit contract, not a description:

```
Face swap with full style transfer.

From image 1 (<distinguishing detail, e.g. "the man in the denim shirt">):
take ONLY his face and head. Preserve his identity exactly —
<enumerate the REAL traits: face shape and width, jawline, chin,
cheekbone structure, nose, eye shape and color, eyebrows, ears,
complexion, moles, hairline, real age>.
<explicit corrections, e.g. "Correct the low-angle lens distortion:
render him at eye level, do not exaggerate jaw or neck width.">
<eyewear: describe HIS frames and say "do NOT replace them with
<the reference's frame type>">
<facial hair: state the target state explicitly, grow or keep>

From image 2: keep EVERYTHING else exactly as it is:
- Identical pose and head angle: <...>
- Identical background: <...>
- Identical clothing: <...>
- Identical lighting: <...>
- Identical framing: <aspect ratio, crop>
- Identical palette: <...>

Relight his face to match: <colorcast, directional shadow across the
face, rim light, lens reflections>.

Photorealistic, natural skin texture with visible pores, no beauty
smoothing, shallow depth of field, sharpest focus on the eyes,
8k high-contrast editorial portrait, 85mm.
```

Full worked example with a real reference: `references/identity-preserving-face-swap.md`

### Negative directives are mandatory

Models beautify by default. Without these lines the output is a generic attractive
stranger wearing the reference's clothes:

- `do not slim the face` / `keep his exact face width and bone structure`
- `do not add sculpted high cheekbones or hollow cheeks`
- `do not sharpen the jaw`
- `do not make him younger` — state the real age numerically
- `no beauty smoothing`
- `do NOT change the glasses to <reference frame style/color>`

Frame it as `This is a strict identity transfer, not a stylistic interpretation.`

## Model routing

| Model | Where | Cost | Use for |
|---|---|---|---|
| **Gemini 2.5 Flash Image (Nano Banana)** | aistudio.google.com | free | first attempt, multi-image input, best free identity retention |
| **Flux Kontext Max** | fal.ai / replicate.com | ~cents per image | when Gemini won't hold the face — purpose-built for edit-with-identity-preserved |
| GPT Image (ChatGPT) | chatgpt.com | sub | easy, understands Persian, but shifts the face (lookalike not same person) |
| Midjourney `--cref` + `--sref` | Discord/web | sub | best artistic quality, cref for face + sref for style |
| Grok Imagine | X app | free-ish | fast, medium quality |

### Gemini Lite pitfall (critical)

**Do NOT use the "Lite" variant.** When the user opens AI Studio and selects
a model, they may see `Gemini 2.5 Flash Image Lite` or similar. Lite models
trade identity fidelity for speed and lower compute — the result is the
*style* reproduces but the *face* is reinvented as a generic attractive
stranger. If the user reports "it got the background and clothes right but
the face isn't him" and they are on Lite, the fix is switching to the
non-Lite model. Instruct them to check Settings (slider icon, upper right)
and ensure the model name does **not** contain "Lite" or "Preview".

Gemini has a real ceiling on preserving a *specific real* face. When the first pass
comes back as a different person, escalate to Flux Kontext rather than re-rolling.

## Diagnosing a returned result

When the user sends back a generated image, inspect it and name concretely what
drifted — do not just say "looks good". Check:

- **Identity drift**: age shifted younger, face narrowed, cheekbones sculpted,
  jaw sharpened, glasses recolored (copper/gold instead of gunmetal is a common one).
- **Was the source even uploaded?** If the face is wholly invented, the most likely
  cause is a text-only prompt with no image attached. Ask before diagnosing deeper.
- **Lighting logic** (the usual realism giveaway): subject close to a wall in hard
  directional sun but **no cast shadow of head/shoulder on the wall**; razor-sharp
  wall shadow edges paired with soft diffuse face shadows; missing eyeglass-rim
  shadow on the cheek. Fix line:
  `cast a hard-edged shadow of his head and shoulder onto the <color> wall`.

### Iterative repair beats re-rolling

Feed the *generated* image back as image 1 plus the real subject photo as image 2,
with a prompt that says `Replace the face in image 1 with the exact face of the man
in image 2. This is a strict identity transfer, not a stylistic interpretation.` and
`Keep everything else from image 1 unchanged`. This preserves the style win already
achieved instead of gambling on a fresh generation.

### When "style right but face wrong": try the BASE-image inversion

The two-block prompt (`From image 1 take face / From image 2 keep everything`) can
cause the model to treat image 2 as the base and *reinterpret* image 1's face into
it — producing a new face in the right style. If this happens, flip the framing:

```
Edit image 1. Image 1 is the base — keep the man in it
exactly as he is. Image 2 is ONLY a lighting and wardrobe
reference. Do not regenerate his face. Do not reinterpret it.
<list the real traits to preserve>
Change ONLY these things: <clothing, background, lighting,
pose — all drawn from image 2>
```

This tells the model to start from the real face and modify the surroundings, not
the other way around. Works better when the model has a strong stylistic
"opinion" that overrides the input face.

## Pitfalls

- Writing the prompt before seeing the subject photo → invented face, wasted round.
- Omitting facial-hair instructions when reference and subject differ → the model
  copies the reference's beard onto a clean-shaven subject unasked.
- Omitting eyewear instructions → frames morph toward the reference's shape and pick
  up the scene's colorcast.
- Not warning about upload order when the prompt references "image 1"/"image 2".
- Forgetting to flip a mirrored selfie.
- Describing the reference in vague mood words ("editorial, moody") instead of
  concrete geometry (wedge positions, shadow diagonals, lapel filling lower-right).
  Concrete geometry reproduces; mood words don't.
- **How to phrase `vision_analyze` calls on people photos:** ask for a *per-image
  attribute description* — "describe face shape and width, glasses frame shape and
  colour, beard density, hair volume, apparent age". Asking it to compare two people,
  identify someone, or judge a photo's "suitability as a face-swap source" makes it
  decline that part of the framing and you lose the round-trip. Collect attributes
  one image at a time and do the comparison yourself.
- The user wants a **plain verdict** when asked "which of these is best" — name the
  single winner in the first line, then a short ranking with reasons. Don't hedge
  across options or bury the answer under analysis.
