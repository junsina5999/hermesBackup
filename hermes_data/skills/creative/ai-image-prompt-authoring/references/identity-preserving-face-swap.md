# Worked example: identity-preserving face swap into an editorial portrait

Real session. User wanted his friend's face placed into a high-contrast editorial
portrait (orange wall, hard sun) while keeping the reference's pose, background,
clothing and lighting untouched.

## The reference photo, described concretely

This level of geometric detail is what makes the style reproduce. Note it is spatial,
not adjectival.

- Vertical 9:16, chest-up framing
- Vivid vermilion-orange textured wall
- Bright neon-orange triangular wedge in the upper-left, bounded by a crisp diagonal
  running from near top-center down to the left edge at about a third of frame height
- Deeper shadowed red band along the entire left margin down to the bottom-left corner
- A second diagonal on the right producing a bright orange shaft beside the head
- Slanted shadow line across the lower-left of the face; forehead and nose stay lit
- Hard single-source directional sunlight, crisp shadow edges, warm orange rim light
  on hair and ear rim
- Black ribbed turtleneck with thick rolled collar; unstructured matte black blazer;
  right lapel filling the lower-right corner
- Palette limited to brilliant orange, deep red-orange shadow, near-black
- Shallow DOF, wall slightly soft, sharpest focus on eyes / glasses / beard
- Pale blue-white specular reflections across the lens tops (only cool accent)

## Subject candidates and the ranking given

Three photos were offered:

1. **Denim Levi's shirt, outdoors, blown-out sky** — chosen. Frontal, face sharp,
   1–2 day stubble (natural path to the reference's full beard), thick voluminous
   hair already close to the reference quiff, featureless background.
   Caveat: shot from slightly below → jaw/neck widened; and it was **mirrored**
   (Levi's tab read backwards) so it needed a horizontal flip first.
2. **Teal V-neck, pale blue wall** — good even light and eye-level angle, but fully
   clean-shaven with short flat hair → much further from the target style.
3. **Inside a car, red T-shirt** — worst. Shot from below the chin, jaw and neck
   distorted wide, flat low-contrast diffuse light.

Lesson: "closest to the target style" beat "best technical lighting" here, because
the model has to invent less.

## The delivered prompt

```
Face swap with full style transfer.

From image 1 (the man in the denim Levi's shirt): take ONLY his face and head.
Preserve his identity exactly — his oval-to-round face shape, moderately wide
cheekbones, soft rounded jawline, rounded chin, straight nose with rounded tip,
thick dark straight eyebrows, dark brown eyes, prominent ears, light olive
complexion, the small mole on his cheek beside the nose, and his slightly receded
temple hairline. He is in his early thirties — keep that age.
Correct the low-angle lens distortion: render him at eye level with natural head
proportions, do not exaggerate the jaw, chin or neck width.
Keep his thin rectangular dark gunmetal metal eyeglasses with lightly rounded
corners — do NOT replace them with round frames.
Grow his light stubble into a neatly groomed full beard and mustache: dense along
the jaw and chin, thinning to stubble on the upper cheeks, dark brown with warmer
lighter tones in the mustache.

From image 2: keep EVERYTHING else exactly as it is:
- Identical pose and head angle: head tilted slightly up, turned to the viewer's
  right, gaze directed off-camera above the horizon, contemplative expression,
  lips closed, neck tendons visible from the upward tilt
- Identical hair styling: his own dark hair swept up and back into a loose
  voluminous quiff, stray strands backlit into bright orange filaments
- Identical background: vivid vermilion-orange textured wall with hard-edged
  diagonal sun shadows — bright neon-orange triangular wedge in the upper left,
  deeper shadowed red band along the left margin, bright orange shaft to the right
  of his head
- Identical clothing: black ribbed turtleneck with thick rolled collar,
  unstructured matte black blazer over it, right lapel filling the lower-right corner
- Identical lighting: hard single-source directional sunlight, crisp shadow edges,
  warm orange rim light along the hair and ear rim, a slanted shadow line falling
  across the lower-left of the face while the forehead and nose stay lit
- Identical framing: vertical 9:16, chest-up
- Identical palette: brilliant orange, deep red-orange shadow, near-black

Relight his face to match: warm orange colorcast on the skin, the diagonal cheek
shadow, orange rim light on hair and ear, pale blue-white specular reflections
across the lens tops.

Photorealistic, natural skin texture with visible pores, no beauty smoothing,
shallow depth of field with the wall slightly soft, sharpest focus on the eyes
glasses and beard, 8k high-contrast editorial portrait, 85mm.
```

## What actually came back from Gemini

Style transferred correctly — orange wall, diagonals, turtleneck, blazer, pose all
right. **Identity did not transfer.** The output was a different person:

- age pulled down to late twenties (subject is early-to-mid thirties)
- face narrowed and elongated; sculpted high cheekbones with hollows added
- jaw narrowed, chin tapered
- glasses recolored to copper/bronze (subject's are dark gunmetal)
- no cast shadow of head/shoulder on the wall despite "hard directional sunlight"
- razor-sharp wall shadow edges vs. soft diffuse face shadows — physically incoherent
- missing eyeglass-rim shadow on the cheek

## The repair prompt (iterative, feeding the generated image back)

```
Replace the face in image 1 with the exact face of the man in image 2.
This is a strict identity transfer, not a stylistic interpretation.

Copy from image 2 without alteration: his rounder fuller face shape, his actual
face width, his softer less angular jawline, his rounded chin, his real cheekbone
structure (do NOT add sculpted high cheekbones or hollow cheeks), his straight nose
with rounded tip, his eye shape and dark brown eyes, his thick dark straight
eyebrows, his prominent ears, the mole on his cheek, and his real age — he is in
his early thirties, NOT in his twenties.

Keep his own thin rectangular dark-gunmetal metal glasses. Do not change them to
copper or gold frames.

Do not slim the face. Do not beautify. Do not sharpen the jaw. Do not make him
younger. The result must be unmistakably the same person as in image 2.

Keep everything else from image 1 unchanged: the orange wall, the diagonal shadows,
the black turtleneck and blazer, the pose, the framing, the lighting. Just relight
his real face to match the warm orange sunlight.
```

Escalation path if this still drifts: fal.ai → Flux Kontext Max with the same two
images and prompt.
