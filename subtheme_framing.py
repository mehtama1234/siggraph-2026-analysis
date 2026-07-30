# -*- coding: utf-8 -*-
"""Plain-language, first-principles framing for each SIGGRAPH sub-theme:
the specific problem and the approach, no jargon (terms grounded once)."""

FRAMING = {
 "Geometry Processing & Meshes": (
  "A computer holds a shape as a shell of tiny flat triangles, and that shell constantly needs cleaning, simplifying, measuring, and reshaping — without tearing or distorting the surface it stands for.",
  "Algorithms that reorganize and repair the triangles — better-shaped, fewer of them, quicker to compare — so the shape stays faithful and easy to work with."),
 "Neural Fields & Representations": (
  "The usual ways of storing a shape or scene — piles of triangles, grids of pixels — are rigid and heavy, when you often want something more compact and flexible.",
  "Store the shape as a small learned function a computer can evaluate anywhere, trading fixed data for a rule that reconstructs the thing on demand."),
 "Physical Simulation": (
  "To move believably, a virtual object must obey the physics of real matter — but those equations are punishing to compute step after step, and quick to blow up into nonsense if you cut the wrong corner.",
  "Numerical methods that take the largest steps they can get away with while staying stable, and that survive the hard moments — things touching, colliding, deforming — without exploding."),
 "Fluids, Smoke & Granular": (
  "Water, smoke, and sand move in swirling, splashing, piling ways that are gorgeous to look at and maddening to compute at any real scale.",
  "Follow the material as particles or on a grid, using physics shortcuts that keep the motion believable and the volume honest while staying fast enough to use."),
 "Cloth, Hair & Fibers": (
  "Cloth and hair are made of countless thin strands that bend, brush, and tangle — simulating each one, and all their contacts, is overwhelming.",
  "Model the fibers and their contacts efficiently, capturing how the whole thing drapes, folds, and moves without tracking every microscopic collision by brute force."),
 "Character Animation & Motion": (
  "Making a digital character move naturally — walking, balancing, reacting — is hard, because believable motion is subtle and the situations to cover are endless.",
  "Drive characters from captured or learned motion so they move like real bodies and can react on their own, instead of animating every frame by hand."),
 "Appearance, Materials & BRDF": (
  "A leaf, polished metal, and human skin all answer light completely differently, and capturing that look convincingly — without tracking every microscopic surface detail — is its own problem.",
  "Compact models of how a surface reflects light, so you can reproduce a material's look from a few measured or learned numbers."),
 "Rendering & Light Transport": (
  "You see an object only because light bounces off it, often many times around a scene — and simulating all those bounces honestly is astronomically expensive.",
  "Trace only the light paths that matter: follow rays back from the eye, spend effort where it changes the picture most, and clean up the leftover speckle."),
 "Computational Photography & Imaging": (
  "A camera is a narrow window — limited range of brightness, one viewpoint, a blur if anything moved — while the real scene is far richer than any single frame.",
  "Combine several limited shots and lean on what we know about how scenes look to recover the fuller truth: a wider range of light, sharper images, fresh lighting."),
 "Fabrication & 3D Printing": (
  "Turning a virtual design into a real physical object runs headlong into what machines can actually make — a printer or knitting machine can only produce certain shapes.",
  "Plan the design backward from the machine's real limits, so what you model on screen can actually be built faithfully."),
 "VR/AR & Displays": (
  "A virtual world has to reach human eyes through a screen or headset with hard physical limits, and fool a visual system exquisitely sensitive to anything that's wrong.",
  "Design displays and imagery around how human sight actually works — spending effort where the eye will notice, and cutting corners where it won't."),
 "Faces & Avatars": (
  "Human faces are the thing we read most closely, so a digital stand-in has to capture a specific person and stay convincing as it's posed and lit in ways never photographed.",
  "Turn photos or video of a person into a controllable model you can re-pose and relight, learning the fine detail of their face so it holds up under a close look."),
 "Sketching & Vector / 2D": (
  "A great deal of art is still made by drawing, and digital tools that ignore how an artist actually works — in strokes, lines, and shapes — get in the way.",
  "Build drawing and flat-graphics tools that meet artists in their own idiom, turning sketches and strokes into clean, editable, expressive results."),
 "Sound & Multisensory": (
  "A world you can see but not hear or feel is only half-real; sound and touch have to match the visuals to be convincing.",
  "Generate sound and touch that follow from what's happening in the scene, so hearing and feeling line up with seeing."),
 "Neural Rendering & Radiance Fields": (
  "Once you've captured a real scene from a handful of photos, you want to view it from angles you never actually shot — but the gaps between photos hold no information.",
  "Store the captured scene not as fixed geometry but as something a computer can re-photograph from any viewpoint, filling the gaps by learning how the scene looked."),
 "Generative 3D & Diffusion": (
  "Making 3D content by hand is painstaking expert work; the ambition is to hand the machine a description or a few images and get a usable shape or scene straight back.",
  "Use the same start-from-noise models that learned to conjure images, now trained to turn out shapes, textures, and whole scenes."),
 "Other": (
  "Work that sits across or between the field's main problems.",
  "A mix of methods drawn from the rest of the field."),
}
