import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA = ROOT / "data"


ARTICLE_MAP = [
    ("surface-truth", "A Surface Is A Promise About What Stays Connected", ["geometry-processing-meshes", "neural-fields-representations"]),
    ("simulation-balance", "Simulation Works By Balancing What Cannot Be Violated", ["physical-simulation", "fluids-smoke-granular"]),
    ("motion-state", "Motion Is State Carried Through Time", ["character-animation-motion", "faces-avatars"]),
    ("material-response", "A Material Is How Matter Answers Light And Force", ["appearance-materials-brdf", "cloth-hair-fibers"]),
    ("light-accounting", "Rendering Is Accounting For How Light Arrives", ["rendering-light-transport", "computational-photography-imaging"]),
    ("generative-constraints", "Generative Graphics Must Preserve Shape While Inventing Detail", ["generative-3d-diffusion", "neural-rendering-radiance-fields"]),
    ("display-eye", "Displays Work By Exploiting What The Eye Will Accept", ["vr-ar-displays", "computational-photography-imaging"]),
    ("fabrication", "Fabrication Turns Geometry Into Matter With Limits", ["fabrication-3d-printing", "geometry-processing-meshes"]),
    ("drawing-structure", "Drawing Is Structure Before It Is Style", ["sketching-vector-2d", "geometry-processing-meshes"]),
    ("sound-contact", "Sound And Touch Reveal Hidden Physical Events", ["sound-multisensory", "physical-simulation"]),
    ("compact-scene", "A Scene Representation Decides What Can Be Forgotten", ["neural-fields-representations", "neural-rendering-radiance-fields"]),
    ("inverse-problem", "Inverse Graphics Recovers The Cause From The Image", ["computational-photography-imaging", "appearance-materials-brdf"]),
    ("control-edit", "Control Means Changing One Thing Without Breaking The Rest", ["generative-3d-diffusion", "character-animation-motion"]),
    ("speed-fidelity", "Fast Graphics Is Choosing Which Error The Viewer Will Notice", ["rendering-light-transport", "vr-ar-displays"]),
    ("graphics-learning", "Learning Helps When Rules Are Known But Too Expensive", ["physical-simulation", "neural-fields-representations"]),
    ("graphics-trust", "A Graphics Result Is Trustworthy Only At Its Failure Boundary", ["geometry-processing-meshes", "rendering-light-transport"]),
]

ARTICLE_CROSSLINKS = {
    "surface-truth": ["fabrication", "compact-scene", "graphics-trust"],
    "simulation-balance": ["sound-contact", "graphics-learning", "speed-fidelity"],
    "motion-state": ["control-edit", "simulation-balance", "generative-constraints"],
    "material-response": ["light-accounting", "inverse-problem", "fabrication"],
    "light-accounting": ["material-response", "inverse-problem", "speed-fidelity"],
    "generative-constraints": ["control-edit", "compact-scene", "graphics-trust"],
    "display-eye": ["speed-fidelity", "light-accounting", "fabrication"],
    "fabrication": ["surface-truth", "material-response", "graphics-trust"],
    "drawing-structure": ["surface-truth", "control-edit", "generative-constraints"],
    "sound-contact": ["simulation-balance", "motion-state", "material-response"],
    "compact-scene": ["surface-truth", "generative-constraints", "speed-fidelity"],
    "inverse-problem": ["light-accounting", "material-response", "graphics-trust"],
    "control-edit": ["generative-constraints", "motion-state", "drawing-structure"],
    "speed-fidelity": ["light-accounting", "display-eye", "compact-scene"],
    "graphics-learning": ["simulation-balance", "compact-scene", "generative-constraints"],
    "graphics-trust": ["surface-truth", "light-accounting", "fabrication"],
}

ARTICLE_THESIS = {
    "surface-truth": "A surface is useful only if nearby samples still describe one object. The papers in this group protect inside, outside, distance, correspondence, sharp features, texture attachment, and editable structure while the surface is simplified, generated, printed, or queried.",
    "simulation-balance": "Simulation is not motion drawn frame by frame. It is an update that must keep accounts: mass should not disappear, contact should not pass through contact, cloth should not stretch without reason, and coupled materials should exchange force in plausible ways.",
    "motion-state": "Motion is memory. A pose at one instant matters because it carries velocity, contact, intent, layer order, identity, and constraints into the next instant. Animation breaks when frames look good separately but lose the state that ties them together.",
    "material-response": "A material is a rule for answering light and force. Wood, skin, hair, fabric, sand, water, paint, and microstructure do not only have appearance; they have responses that must remain stable when lighting, motion, contact, or fabrication changes.",
    "light-accounting": "Rendering asks where light could have traveled before it became a pixel. The papers differ in speed and representation, but they share one burden: estimate enough paths to preserve the scene claim without pretending every shortcut is physically harmless.",
    "generative-constraints": "Generative graphics is useful when invented detail remains attached to structure. A generated shape, view, terrain, motion, or relighting result must still obey correspondence, controllability, geometry, identity, and downstream editing needs.",
    "display-eye": "A display system is a bargain between hardware and perception. It can save work by exploiting what the eye will accept, but only while preserving comfort, depth, focus, latency, brightness, and artifact limits.",
    "fabrication": "Fabrication makes geometry answer to matter. A printable or manufacturable object must respect tool paths, bead thickness, fiber direction, stress, deployability, support, collision, and the limits of the machine that builds it.",
    "drawing-structure": "A drawing is not just marks. It carries hidden order: which stroke continues, which curve is in front, which region owns a color boundary, and which surface or time step a line belongs to.",
    "sound-contact": "Sound and touch are evidence of hidden physical events. They depend on contact, vibration, material, timing, and force, so the representation must preserve the event that produced the sensation.",
    "compact-scene": "A scene representation decides what can be forgotten. Compact storage is useful only if the later question still has enough information: surface, view, lighting, motion, density, uncertainty, or edit handle.",
    "inverse-problem": "Inverse graphics starts from partial evidence and asks what caused it. The hard part is that many scenes can explain the same image, so the method must state what prior, sensor model, or constraint makes one cause credible.",
    "control-edit": "Control means changing one thing while other promises stay true. A useful edit should alter pose, identity, lighting, texture, shape, or layout without silently breaking contact, correspondence, view consistency, or user intent.",
    "speed-fidelity": "Fast graphics chooses which error is least visible or least damaging. The question is not only how much work is skipped, but which physical or perceptual quantity absorbs the approximation.",
    "graphics-learning": "Learning helps when a known rule is too costly, noisy, or incomplete to use directly. It should replace repeated expense, not erase the physical bookkeeping that made the original rule trustworthy.",
    "graphics-trust": "A graphics result is trustworthy only inside the assumptions it names. A beautiful image is weak evidence unless the method says where it fails: sparse views, thin geometry, fast motion, tangled contact, unusual materials, or unsupported hardware.",
}

CORE_IDEA = {
    "surface-truth": "The burden is connectivity. A mesh, field, or point set must let later code recover which pieces belong together and which side of the object a query lies on.",
    "simulation-balance": "The burden is conservation and constraint. The next state must pay for mass, force, contact, volume, bend, and coupling rather than simply looking smooth.",
    "motion-state": "The burden is temporal state. The system must carry the information that makes frame two a consequence of frame one, not a fresh independent picture.",
    "material-response": "The burden is response. The material has to answer changes in light, load, contact, moisture, heat, or motion in a way that stays consistent across views and uses.",
    "light-accounting": "The burden is path contribution. A pixel is an accumulated answer from many possible routes light could have taken through the scene.",
    "generative-constraints": "The burden is structured invention. The model may fill in detail, but it must preserve the relationships the user, renderer, simulator, or editor will depend on later.",
    "display-eye": "The burden is perception under hardware limits. The display can approximate only where the eye and body still accept the result.",
    "fabrication": "The burden is buildability. The digital object must become a physical object without violating material, machine, or assembly constraints.",
    "drawing-structure": "The burden is hidden order. The drawing must remember layer, crossing, boundary, and time relationships that are not visible in a single isolated mark.",
    "sound-contact": "The burden is event cause. A sound or haptic signal must remain tied to the contact, motion, material, or vibration that produced it.",
    "compact-scene": "The burden is recoverability. A compressed representation is good only if the forgotten information is not needed by the next query.",
    "inverse-problem": "The burden is plausible cause. The method must explain why this hidden scene, light, material, or motion is the right cause of the observed evidence.",
    "control-edit": "The burden is edit locality. One requested change should not leak into unrelated identity, shape, material, contact, or timing promises.",
    "speed-fidelity": "The burden is acceptable error. The method must know which error the viewer, tool, or physical system will notice and which error is harmless.",
    "graphics-learning": "The burden is rule preservation. The learned shortcut must keep the governing structure that made the expensive method worth using.",
    "graphics-trust": "The burden is boundary naming. The result must say what assumptions hold it up and what case would make the claim fail.",
}

WHAT_CHANGED = [
    ("Diffusion moved from image synthesis into graphics structure", "The local corpus shows diffusion and flow models appearing in 3D shape, terrain, motion, relighting, material transfer, and scene layout. The change is not simply that graphics uses a fashionable model. The model is being forced to preserve graphics constraints: connected surfaces, usable mesh structure, view consistency, lighting behavior, contact, and controllable edits."),
    ("Neural fields became a storage choice, not only a rendering trick", "Neural fields, splats, and learned implicit representations are now ways to decide what a scene can forget. A compact representation is useful only if the surface, view, lighting, or motion needed later can still be recovered."),
    ("Simulation is being made interactive without dropping bookkeeping", "Many simulation papers are about keeping mass, contact, bending, coupling, and time stability while reducing the solve enough for large scenes, design loops, or interaction. Speed is not the main claim unless the physical quantity is still accounted for."),
    ("Graphics and vision are meeting at inverse problems", "Computational photography, relighting, material recovery, neural rendering, and generative 3D all ask the same reverse question: what hidden scene, surface, light, or material caused this image or sparse measurement?"),
    ("Displays and fabrication pull graphics back into matter", "VR, AR, holography, fabrication, 3D printing, and material design make the output physically accountable. The result must work for the eye, the printer, the actuator, the fiber, the polymer, or the display hardware."),
    ("Failure boundaries matter more than raw visual appeal", "The strong question is no longer whether a result looks plausible in a demo. It is where the method stops being trustworthy: sparse views, extreme lighting, thin structures, tangled contact, unusual materials, unsupported body motion, or fabrication limits."),
]

FAMILY_KEYWORDS = {
    "appearance-materials-brdf": ["material", "brdf", "reflectance", "appearance", "scattering", "relighting", "fabric", "hair", "feather", "microstructure"],
    "character-animation-motion": ["motion", "animation", "character", "pose", "body", "hand", "avatar", "rigging", "skinning", "contact"],
    "cloth-hair-fibers": ["cloth", "hair", "fiber", "yarn", "knit", "garment", "fabric", "feather", "try-on", "strand"],
    "computational-photography-imaging": ["camera", "imaging", "photography", "hdr", "exposure", "thermal", "plenoptic", "holography", "sensor", "image"],
    "fabrication-3d-printing": ["fabrication", "print", "printing", "toolpath", "manufactur", "slicer", "composite", "kirigami", "laminated", "deployable"],
    "faces-avatars": ["face", "facial", "avatar", "portrait", "relight", "head", "human", "hair", "identity", "egocentric"],
    "fluids-smoke-granular": ["fluid", "smoke", "granular", "sand", "water", "air", "flow", "mpm", "lbm", "erosion"],
    "generative-3d-diffusion": ["diffusion", "generative", "generation", "3d", "flow matching", "autoregressive", "text-to", "sample", "prior"],
    "geometry-processing-meshes": ["mesh", "surface", "geometry", "remeshing", "hausdorff", "winding", "nurbs", "tetrahedral", "intersection", "offset"],
    "neural-fields-representations": ["neural field", "implicit", "sdf", "field", "radiance", "gaussian", "compression", "representation", "grid"],
    "neural-rendering-radiance-fields": ["neural rendering", "radiance", "view", "novel view", "gaussian", "splat", "relight", "scene", "nerf"],
    "physical-simulation": ["simulation", "physics", "contact", "deformation", "mpm", "fem", "solver", "dynamics", "bending", "elastic"],
    "rendering-light-transport": ["rendering", "light", "path tracing", "monte carlo", "ray", "holography", "scattering", "illumination", "transport"],
    "sketching-vector-2d": ["sketch", "stroke", "vector", "curve", "drawing", "inbetween", "planar", "2d", "diffusion curve"],
    "sound-multisensory": ["sound", "audio", "haptic", "touch", "vibration", "contact", "acoustic", "tactile"],
    "vr-ar-displays": ["display", "vr", "ar", "holography", "headset", "perception", "foveated", "latency", "comfort"],
}

ARTICLE_EXAMPLE_OVERRIDES = {
    ("display-eye", "vr-ar-displays"): [
        "PAColorHolo: A Perceptually-Aware Color Management Framework for Holographic Displays",
        "A Two-Millisecond Passthrough Headset for Perceptual Studies",
        "MorphSkein: A Shape-Changing Afterimage Display Preserving Pixel Density During Surface-Area Changes Across Troposkein-Based Shapes",
        "HoloPathTracer: Fast and Accurate Wave Path Tracing for Holography",
        "Invisible Holographic Window: Full-color 3D Image Reconstruction from Transparent Surface-relief Computer-generated Holograms",
        "Dual-Path Holographic Laser-Excited Volumetric Display",
    ],
    ("fabrication", "fabrication-3d-printing"): [
        "Uniformly Deployable Kirigami on Arbitrary Planar Graphs",
        "AtomSlicer: Constant-Thickness Field-Aligned Non-Planar Slicing and Continuous Toolpaths for FFF",
        "Co-Optimization of Structure and Manufacturable Semi-Continuous Layers for Laminated Composites",
        "Single-View Holographic Volumetric 3D Printing with Coupled Differentiable Wave-Optical and Photochemical Optimization",
        "Stress-Aware Panelization of Freeform Surfaces",
        "Untangling Surfaces via Shape and Mesh Repulsion",
    ],
    ("sound-contact", "sound-multisensory"): [
        "ProXeek: Seeking and Leveraging Real-World Objects and Environments as Haptic Proxies for Virtual Reality through Multimodal Reasoning",
        "Heterogeneous Subspace Corrections for GPU Deformable Multibody Dynamics",
        "High-Fidelity 4D Cloth Capture Pipeline with a Two-Level Pattern",
        "Interactive Yarn-level Knitwear with Nested Douglas-Rachford Splitting",
        "MOCHI: Motion Enhancement of Collaborative Human-object Interactions",
        "Mechanical Cloaking of Halftoned Imagery",
    ],
    ("graphics-learning", "physical-simulation"): [
        "GMT: A Geometric Multigrid Transformer Solver for Microstructure Homogenization",
        "DiffSurFlow: Efficient and Robust Differentiable Fluid Optimization via Surrogate Strategy on Flow Map",
        "A Few-Step Generative Model on Cumulative Flow Maps",
        "MUSIC: Learning Muscle-Driven Dexterous Hand Control",
        "HIL: Hybrid Imitation Learning for Dynamic Athletic Control",
        "Photons × Force: Differentiable Radiation Pressure Modeling",
    ],
    ("inverse-problem", "computational-photography-imaging"): [
        "Inverse Rendering for Discrete X-Ray Computed Tomography",
        "Thermal Non-Line-of-Sight Imaging through Rough Surfaces",
        "GenPIE: A Time-Resolved Plenoptic Imager",
        "Hi-SPAD: Video-Rate Hyperspectral Imaging and Inference with Single-Photon Cameras",
        "Tensor Decomposition-Based Four-dimensional Background-Oriented Schlieren Tomography for High-Speed, High-Fidelity Flow Field Reconstruction",
        "Lucky High Dynamic Range Smartphone Imaging",
    ],
    ("inverse-problem", "appearance-materials-brdf"): [
        "Learning a Delighting Prior for Facial Appearance Capture in the Wild",
        "EgoRelight: Egocentric Human Capture and Illumination Recovery for Relightable and Photoreal Avatar Rendering",
        "BodyReLux: Temporally Consistent Full-Body Video Relighting",
        "DealMaTe: Multi-Dimensional Material Transfer via Diffusion Transformer",
        "Fiber-level Woven Fabric Capture from a Single Microscopic Image",
        "Fast and Accurate Gaussian Process Modelling of Real-World Materials",
    ],
    ("speed-fidelity", "rendering-light-transport"): [
        "Forget Superresolution, Sample Adaptively (when Path Tracing)",
        "ToF ReSTIR: Time-of-Flight Rendering with Spatio-temporal Reservoir Resampling",
        "Neural Quadrature Rule and Autoregressive Adaptive Sampling",
        "Efficient Fur and Hair Multiple Scattering Using Volumetric Approximation",
        "Sample Matching for Joint Extinction Gradient Estimation in Differentiable Volume Rendering",
        "HoloPathTracer: Fast and Accurate Wave Path Tracing for Holography",
    ],
    ("speed-fidelity", "vr-ar-displays"): [
        "A Two-Millisecond Passthrough Headset for Perceptual Studies",
        "PAColorHolo: A Perceptually-Aware Color Management Framework for Holographic Displays",
        "MorphSkein: A Shape-Changing Afterimage Display Preserving Pixel Density During Surface-Area Changes Across Troposkein-Based Shapes",
        "Dual-Path Holographic Laser-Excited Volumetric Display",
        "Invisible Holographic Window: Full-color 3D Image Reconstruction from Transparent Surface-relief Computer-generated Holograms",
        "Single-View Holographic Volumetric 3D Printing with Coupled Differentiable Wave-Optical and Photochemical Optimization",
    ],
    ("control-edit", "generative-3d-diffusion"): [
        "HumanFlow: Controllable Human Image Generation via Flow Matching",
        "HeadRouter: A Training-free Image Editing Framework for MM-DiTs by Adaptively Routing Attention Heads",
        "Loops2Roofs: Diffusion-based 3D Roof Generation using a Loop Representation",
        "CasLayout: Cascaded 3D Layout Diffusion for Indoor Scene Synthesis with Implicit Relation Modeling",
        "Autoregressive Diffusion with Hybrid Representation for Interactive Human Motion Generation",
        "Nexus: Native Mesh Generation with Diffusion",
    ],
    ("control-edit", "character-animation-motion"): [
        "DMP: Directable Motion Retargeting through Motion Paraphrasing",
        "Skinned Motion Retargeting with Spatially Adaptive Interaction Guidance",
        "MOCHI: Motion Enhancement of Collaborative Human-object Interactions",
        "OmniHands: Robust Motion Capture of Interactive Hands via A Versatile Transformer",
        "ACT: A Unified Framework for Rigging and Animating Characters with Arbitrary Topologies",
        "MUSIC: Learning Muscle-Driven Dexterous Hand Control",
    ],
    ("graphics-trust", "geometry-processing-meshes"): [
        "GPU-accelerated Certified Hausdorff Distance Between Triangle Meshes",
        "A Precision Controlled Surface-Surface Intersection Algorithm for NURBS",
        "Floating-Point Robustness in Parametric Surface Continuous Collision Detection: From Algorithm to Benchmarking",
        "Robust Constrained Tetrahedralization with Steiner-point-free Boundaries",
        "The Antipodal Method: Fast, Accurate, and Robust 3D Generalized Winding Numbers",
        "Untangling Surfaces via Shape and Mesh Repulsion",
    ],
    ("graphics-trust", "rendering-light-transport"): [
        "Robust Computation of Boundary Path Integrals Using Kernel-Density Estimation",
        "Sample Matching for Joint Extinction Gradient Estimation in Differentiable Volume Rendering",
        "ToF ReSTIR: Time-of-Flight Rendering with Spatio-temporal Reservoir Resampling",
        "Inverse Rendering for Discrete X-Ray Computed Tomography",
        "HoloPathTracer: Fast and Accurate Wave Path Tracing for Holography",
        "Generalized Aberrations for Processing-Aware Optical Design",
    ],
    ("surface-truth", "geometry-processing-meshes"): [
        "Feature-Preserving Offset Meshing",
        "Untangling Surfaces via Shape and Mesh Repulsion",
        "The Antipodal Method: Fast, Accurate, and Robust 3D Generalized Winding Numbers",
        "A Robust and Efficient Intersection Algorithm for NURBS Surfaces: Handling Small Loops and Tangent Intersections",
        "Texture-Aware Remeshing for Texture-aware Geometry Processing",
        "GPU-accelerated Certified Hausdorff Distance Between Triangle Meshes",
    ],
    ("simulation-balance", "fluids-smoke-granular"): [
        "Volume-Preserving LBM-MPM Coupling for Air-Water-Sand Mixtures",
        "Kinetic Predicted-Moment Flux Reconstruction for High-Order High-Performance Fluid Simulation",
        "Fast VEM Fluid Simulation",
        "Spatiotemporal FLIP for Fast Free-Surface and Two-Phase Simulation With Very Large Time Steps",
        "DiffSurFlow: Efficient and Robust Differentiable Fluid Optimization via Surrogate Strategy on Flow Map",
        "Mixed Material Point Methods for Stiff Elastoplasticity",
    ],
    ("motion-state", "faces-avatars"): [
        "TwinPose: Person-Specific Subspaces for Multi-View 3D Pose Estimation",
        "BodyReLux: Temporally Consistent Full-Body Video Relighting",
        "EgoRelight: Egocentric Human Capture and Illumination Recovery for Relightable and Photoreal Avatar Rendering",
        "STyMo: Fast and Controllable Few-Shot Motion Style Transfer",
        "Learning a Delighting Prior for Facial Appearance Capture in the Wild",
        "Pixel Cube: Diffusion-based Portrait Video Relighting Through Realistic Lighting Reproduction",
    ],
    ("material-response", "appearance-materials-brdf"): [
        "Fiber-level Woven Fabric Capture from a Single Microscopic Image",
        "Efficient Fur and Hair Multiple Scattering Using Volumetric Approximation",
        "A Real-time, Multiscale and Procedural Feather Appearance Model",
        "Fast and Accurate Gaussian Process Modelling of Real-World Materials",
        "A Unified Homogenization Framework for Straight- and Curved-Crease Origami Materials",
        "DealMaTe: Multi-Dimensional Material Transfer via Diffusion Transformer",
    ],
    ("light-accounting", "rendering-light-transport"): [
        "ToF ReSTIR: Time-of-Flight Rendering with Spatio-temporal Reservoir Resampling",
        "Efficient Fur and Hair Multiple Scattering Using Volumetric Approximation",
        "Radiance Caching for Differentiable Path Tracing",
        "HoloPathTracer: Fast and Accurate Wave Path Tracing for Holography",
        "Sample Matching for Joint Extinction Gradient Estimation in Differentiable Volume Rendering",
        "Neural Quadrature Rule and Autoregressive Adaptive Sampling",
    ],
    ("generative-constraints", "generative-3d-diffusion"): [
        "Nexus: Native Mesh Generation with Diffusion",
        "Grow3D: Hierarchical Next-Scale Octree Prediction for Fast and High-Fidelity 3D Shape Generation",
        "Loops2Roofs: Diffusion-based 3D Roof Generation using a Loop Representation",
        "Tempo3D: Efficient Temporal-Aware Fine-Tuning and Multi-View Latent Aggregation for 3D Generation",
        "AniGen: Unified S3 Fields for Animatable 3D Asset Generation",
        "CasLayout: Cascaded 3D Layout Diffusion for Indoor Scene Synthesis with Implicit Relation Modeling",
    ],
    ("drawing-structure", "geometry-processing-meshes"): [
        "Robust Planar Maps for 3D Vectorization",
        "Implicit Minimal Surfaces for Bijective Correspondences",
        "SQuadGen: Generating Simple Quad Layouts via Chart Distance Fields",
        "Learning Sparse Singularities for Cross Field Design",
        "Texture-Aware Remeshing for Texture-aware Geometry Processing",
        "Spatially Accelerated Winding Numbers for Curved Geometry",
    ],
    ("compact-scene", "neural-fields-representations"): [
        "SAND: Spatially Adaptive Network Depth for Fast Sampling of Neural Implicit Surfaces",
        "SCom DAG: compact representation of spatial data for real-time rendering",
        "Implicit Surface Compression -- with Good Old Discrete Cosine Transform and Motion Compensation",
        "Gabor Fields: Orientation-Selective Level-of-Detail for Volume Rendering",
        "Bounding Stratified Bernoulli Impulses for Ray Marching Gaussian Process Implicit Surfaces",
        "Uncertainty-aware geometry processing on Gaussian Process Implicit Surfaces",
    ],
    ("compact-scene", "neural-rendering-radiance-fields"): [
        "Gaussian Point Splatting",
        "ATGS: Anchored Temporal Gaussian Splatting for Long Volumetric Video Representation",
        "Closed-Form Convolution for physically-accurate defocus in Gaussian Splatting",
        "Radiance Caching for Differentiable Path Tracing",
        "The PhaseTree: Multiphase Signed Distance Fields",
        "Dual Contouring over Expanded Cubes (DCx) for Zero-Level Set Extraction from Neural Unsigned Distance Functions",
    ],
}


FORCES = [
    ("Shape", "Which points, edges, surfaces, and parts belong together, and what must stay connected when the object bends, simplifies, prints, or becomes a neural field."),
    ("Light", "How energy leaves sources, hits matter, scatters, reflects, enters a camera, and becomes pixels without pretending a shortcut is physical truth."),
    ("Motion", "What state must be carried from one instant to the next so bodies, fluids, hair, smoke, hands, cameras, and drawings do not lose identity."),
    ("Matter", "What material, stiffness, density, fiber, pore, pigment, and printed constraint make a visual shape behave like a physical object."),
    ("Generation", "What can be invented from examples while preserving geometry, contact, material response, controllable edits, and view consistency."),
    ("Perception", "What the camera, display, microscope, headset, or sensor actually measured, and what hidden cause must be recovered from that partial evidence."),
    ("Computation", "What approximation, sampling rule, solver, hierarchy, cache, or representation makes the result fast enough without deleting the reason it is correct."),
    ("Failure", "Which assumption breaks first: smoothness, visibility, physical law, view coverage, material model, user control, or display tolerance."),
]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load(name):
    return json.loads((DATA / name).read_text())


def style():
    return """<style>
:root{--bg:#0E1420;--panel:#141D2C;--ink:#EAEEF4;--soft:#B4BFD0;--dim:#8493A8;--line:rgba(150,170,205,.16);--accent:#4FA8B8;--amber:#E3A63A;--serif:"Iowan Old Style",Palatino,Georgia,serif;--sans:-apple-system,system-ui,"Segoe UI",Roboto,Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.72}.wrap{max-width:980px;margin:0 auto;padding:0 24px 70px}header{padding:54px 0 26px}.k,nav a,.pill,footer{font-family:var(--mono)}.k{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}h1{font-family:var(--serif);font-size:clamp(34px,6vw,54px);line-height:1.05;margin:12px 0;color:#fff}h2{font-family:var(--serif);font-size:28px;line-height:1.12;margin:6px 0 10px;color:#fff}h3{font-size:17px;color:#fff;margin:18px 0 6px}p{color:var(--soft);font-size:16px;margin:9px 0}a{color:var(--accent)}nav{position:sticky;top:0;background:rgba(14,20,32,.96);border-bottom:1px solid var(--line);z-index:5}nav .wrap{padding:9px 24px;display:flex;gap:6px;flex-wrap:wrap}nav a{text-decoration:none;color:var(--soft);border:1px solid var(--line);border-radius:999px;padding:4px 9px;font-size:11px}.doc,.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px 22px;margin:16px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}.pill{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:3px 8px;margin:3px;color:var(--soft);font-size:11px;text-decoration:none}.examples{padding-left:18px}.examples li{color:var(--soft);font-size:14px;margin:8px 0}.diagram{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:12px}.node{font-family:var(--mono);font-size:12px;min-height:58px;border:1px solid var(--line);border-radius:9px;background:#102638;color:#dff9ff;display:flex;align-items:center;justify-content:center;text-align:center;padding:8px}table{width:100%;border-collapse:collapse;background:var(--panel)}td,th{border-bottom:1px solid var(--line);padding:9px;text-align:left;vertical-align:top;color:var(--soft);font-size:14px}th{font-family:var(--mono);color:var(--accent);font-size:12px}footer{color:var(--dim);font-size:12px;margin-top:34px}@media(max-width:700px){.diagram{grid-template-columns:1fr}.wrap{padding-left:18px;padding-right:18px}}
</style>"""


def page(title, subtitle, body):
    nav = '<nav><div class="wrap"><a href="index.html">home</a><a href="siggraph-synthesis.html">synthesis</a><a href="siggraph-field-map.html">field map</a><a href="siggraph-first-principles-articles.html">articles</a><a href="siggraph-diagrams.html">diagrams</a><a href="siggraph-reader-paths.html">reader paths</a><a href="siggraph-concept-paper-index.html">paper index</a><a href="siggraph-theme-audit.html">theme audit</a><a href="siggraph-review-guide.html">review guide</a><a href="siggraph-what-changed.html">what changed</a><a href="explorer.html">explorer</a></div></nav>'
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title>{style()}</head><body>{nav}<main class="wrap"><header><div class="k">SIGGRAPH 2026 first-principles layer</div><h1>{escape(title)}</h1><p>{escape(subtitle)}</p></header>{body}<footer>Generated from local SIGGRAPH 2026 analysis data: 153 papers, 16 families, 8 math concepts.</footer></main></body></html>'


def paper_score(paper, keywords):
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    title = paper.get("title", "").lower()
    score = 0
    for kw in keywords:
        k = kw.lower()
        if k in title:
            score += 5
        if k in text:
            score += 2
    return score


def family_examples(families, papers, key, n=5, used=None, article_id=None):
    fam = families[key]
    titles = ARTICLE_EXAMPLE_OVERRIDES.get((article_id, key)) or fam.get("representative_papers") or fam.get("papers") or []
    used = used if used is not None else set()
    out = []
    for title in titles[:n]:
        if title in used:
            continue
        match = next((p for p in papers if (p.get("title") or p.get("t") or "") == title), {})
        abstract = match.get("abstract", "")
        note = abstract.split(". ")[0][:260] if abstract else ""
        used.add(title)
        out.append({"title": title, "note": note})
    if len(out) < n:
        ranked = sorted(
            papers,
            key=lambda p: (-paper_score(p, FAMILY_KEYWORDS.get(key, key.split("-"))), p.get("title", "")),
        )
        for p in ranked:
            t = p.get("title") or p.get("t") or ""
            if not t or t in used:
                continue
            score = paper_score(p, FAMILY_KEYWORDS.get(key, key.split("-")))
            if score <= 0:
                continue
            abstract = p.get("abstract", "")
            note = abstract.split(". ")[0][:260] if abstract else ""
            used.add(t)
            out.append({"title": t, "note": note})
            if len(out) >= n:
                break
    return out[:n]


def article_links(aid):
    titles = {a: t for a, t, _ in ARTICLE_MAP}
    return "".join(f'<a class="pill" href="#{target}">{escape(titles[target])}</a>' for target in ARTICLE_CROSSLINKS.get(aid, []))


def article_thesis(title, keys):
    return ARTICLE_THESIS.get(slug(title), title)


def render_articles(families, papers):
    cards = []
    for i, (aid, title, keys) in enumerate(ARTICLE_MAP, 1):
        blocks = []
        used_examples = set()
        for key in keys:
            fam = families[key]
            examples = "".join(f'<li><b>{escape(ex["title"])}</b>{(": " + escape(ex["note"])) if ex["note"] else ""}</li>' for ex in family_examples(families, papers, key, 6, used_examples, aid))
            math = fam.get("mathematical_principle", fam.get("recurring_math", fam.get("mathematical_move", "")))
            blocks.append(f'''<section class="card"><div class="k">{escape(key)}</div><h3>{escape(fam.get("theme", key.replace("-", " ").title()))}</h3>
<p><b>Ordinary problem.</b> {escape(fam.get("problem_shape", ""))}</p>
<p><b>Naive attempt and what breaks.</b> {escape(fam.get("naive_failure", ""))}</p>
<p><b>Mathematical object.</b> {escape(math)}</p>
<p><b>Why this math fits.</b> {escape(fam.get("why_math_matters", ""))}</p>
<p><b>How the papers split.</b> {escape(fam.get("paper_family", ""))}</p>
<p><b>What changed in 2026.</b> {escape(fam.get("what_changed", ""))}</p>
<p><b>Failure boundary.</b> {escape(fam.get("limits", ""))}</p>
<ul class="examples">{examples}</ul></section>''')
        cards.append(f'''<article id="{aid}" class="doc"><div class="k">Article {i}</div><h2>{escape(title)}</h2>
<p>{escape(article_thesis(title, keys))}</p>
<h3>Core idea</h3><p>{escape(CORE_IDEA[aid])}</p>
<h3>Why the simple approach fails</h3><p>The tempting shortcut is to manipulate visible samples independently: move vertices, paint pixels, average frames, trace fewer rays, generate a finished object in one step, or smooth away a bad contact. These moves often improve the visible case while breaking the hidden structure. SIGGRAPH papers are valuable when they show how to make the hidden structure inspectable.</p>
<h3>Representative paper groups</h3>{"".join(blocks)}
<h3>Read next</h3><p>{article_links(aid)}</p></article>''')
    return page("SIGGRAPH first-principles articles", "Sixteen cross-paper articles derived from the local SIGGRAPH family map, written around the hidden visual and physical quantities rather than method labels.", '<section class="doc"><h2>Ranked entry path</h2><p>Start with surface, simulation, motion, material, and light. Then read generation, display, fabrication, and trust. The remaining articles show how these pressures reappear as compact representations, inverse problems, editing control, speed, learning, and failure boundaries.</p></section>' + "".join(cards))


def render_field_map():
    body = '<div class="grid">' + ''.join(f'<section class="card"><div class="k">Force {i}</div><h2>{escape(name)}</h2><p>{escape(text)}</p></section>' for i, (name, text) in enumerate(FORCES, 1)) + '</div>'
    return page("SIGGRAPH field map", "The conference as eight forces: shape, light, motion, matter, generation, perception, computation, and failure.", body)


def render_synthesis():
    sections = [
        ("The field is still about making impossible worlds computable", "Computer graphics begins with a mismatch. The world contains continuous surfaces, light paths, materials, bodies, fluids, sound, and fabrication constraints. The machine gets finite memory, finite time, finite samples, and incomplete measurements. SIGGRAPH 2026 is the record of how researchers choose what to preserve and what to approximate."),
        ("Geometry is the holding structure", "Meshes, curves, fields, splats, and vectors are different storage contracts. Each says what the object is allowed to forget while still being recoverable as a believable shape. The important question is what stays connected, smooth, sharp, inside, outside, or in contact."),
        ("Physics is the refusal to let pictures float free", "Simulation, materials, cloth, hair, smoke, and light transport make graphics answer to constraints outside the image. A result can look good and still be false if mass disappears, contact breaks, energy goes nowhere, or light behaves in a way no scene could produce."),
        ("Generation is entering graphics through constraints", "Diffusion and neural generation are not replacing graphics craft. They are being bent around graphics constraints: view consistency, surface validity, user control, material response, animation continuity, and edit locality."),
        ("The whole conference is a study of failure boundaries", "A graphics method is trustworthy only where its assumptions hold. The useful pages should therefore teach the boundary: what happens under sparse views, hard lighting, fast motion, tangled cloth, thin geometry, extreme display limits, or fabrication constraints."),
    ]
    body = ''.join(f'<section class="doc"><div class="k">Part {i}</div><h2>{escape(t)}</h2><p>{escape(p)}</p></section>' for i, (t, p) in enumerate(sections, 1))
    return page("What SIGGRAPH 2026 says graphics is becoming", "A compact first-principles synthesis of the 153-paper local analysis.", body)


def render_diagrams():
    diagrams = [
        ("Surface contract", ["points", "connections", "surface rule", "valid shape"], "A representation is a promise that the shape can be recovered after storage or change."),
        ("Light accounting", ["source", "surface response", "many paths", "pixel"], "Rendering adds up many possible ways light could arrive."),
        ("Simulation step", ["state now", "forces", "constraints", "state next"], "Simulation advances the world while preserving what physics forbids breaking."),
        ("Generative control", ["intent", "sample", "constraint check", "valid result"], "Generation is useful when the invented detail still obeys the requested structure."),
        ("Display trick", ["display hardware", "eye response", "perceived image", "comfort limit"], "Displays exploit human perception without crossing discomfort or artifact boundaries."),
        ("Fabrication path", ["digital shape", "material limit", "tool path", "physical object"], "Fabrication asks which digital shape can actually become matter."),
    ]
    cards = []
    for title, steps, note in diagrams:
        nodes = "".join(f'<div class="node">{escape(step)}</div>' for step in steps)
        cards.append(f'<section class="card"><h2>{escape(title)}</h2><div class="diagram">{nodes}</div><p>{escape(note)}</p></section>')
    body = '<div class="grid">' + ''.join(cards) + '</div>'
    return page("SIGGRAPH first-principles diagrams", "Simple visual flows for the hidden quantities in graphics.", body)


def render_reader_paths():
    paths = [
        ("90-minute overview", "Read in this order: synthesis, field map, articles 1-6, diagrams. Stop there if you only need the spine of the field."),
        ("One-day deep read", "Read synthesis, field map, all sixteen articles, then the concept-to-paper index. For each article, read the representative paper groups and the named examples that make the concept concrete."),
        ("One-week study plan", "Day 1 geometry, day 2 simulation, day 3 rendering and materials, day 4 motion and avatars, day 5 generative 3D, day 6 displays and fabrication, day 7 trust and failure boundaries."),
        ("Builder path", "Build a mesh simplifier, a tiny light integrator, a particle simulator, a material viewer, a controlled 3D generator mockup, and a display/fabrication constraint checker."),
    ]
    body = ''.join(f'<section class="doc"><div class="k">Path {i}</div><h2>{escape(t)}</h2><p>{escape(p)}</p></section>' for i, (t, p) in enumerate(paths, 1))
    return page("SIGGRAPH reader paths", "Practical routes through the SIGGRAPH concept layer.", body)


def render_theme_audit(families):
    rows = []
    for key, fam in families.items():
        linked = [title for aid, title, keys in ARTICLE_MAP if key in keys]
        need = "diagram/examples polish" if len(linked) < 2 else "covered by multiple concept articles"
        rows.append(f'<tr><td>{escape(key)}</td><td>{escape(fam.get("theme", key.replace("-", " ").title()))}</td><td>{len(linked)}</td><td>{escape("; ".join(linked[:4]))}</td><td>{escape(need)}</td></tr>')
    body = f'''<section class="doc"><h2>Audit result</h2><p>The source has 16 rich paper families. Every family is now represented in at least one first-principles article, and most are used as evidence in two articles. The next editorial risk is not missing coverage; it is whether each family example is the best possible proof of the concept.</p></section><section class="doc"><table><thead><tr><th>Family key</th><th>Theme</th><th>Article links</th><th>Concept use</th><th>Next audit action</th></tr></thead><tbody>{"".join(rows)}</tbody></table></section>'''
    return page("SIGGRAPH theme audit", "The sixteen SIGGRAPH families checked against the first-principles article layer.", body)


def render_what_changed():
    body = "".join(f'<section class="doc"><div class="k">Change {i}</div><h2>{escape(title)}</h2><p>{escape(text)}</p></section>' for i, (title, text) in enumerate(WHAT_CHANGED, 1))
    return page("What changed from older graphics", "The 2026 shift in SIGGRAPH, read from the local 153-paper analysis.", body)


def render_index(families, papers):
    rows = []
    for aid, title, keys in ARTICLE_MAP:
        ex = []
        used_examples = set()
        for key in keys:
            ex.extend(family_examples(families, papers, key, 4, used_examples))
        links = "<br>".join(escape(x["title"]) for x in ex[:8])
        rows.append(f'<tr><td><a href="siggraph-first-principles-articles.html#{aid}">{escape(title)}</a></td><td>{escape(", ".join(keys))}</td><td>{links}</td></tr>')
    body = f'<section class="doc"><table><thead><tr><th>Concept</th><th>Families</th><th>Representative papers</th></tr></thead><tbody>{"".join(rows)}</tbody></table></section>'
    return page("SIGGRAPH concept-to-paper index", "Each first-principles article tied to the local paper-family evidence.", body)


def patch_home():
    links = '<p><a href="siggraph-synthesis.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:#0E1420;background:var(--accent);border-radius:9px;padding:10px 22px;text-decoration:none;font-weight:600">→ synthesis</a> <a href="siggraph-field-map.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ field map</a> <a href="siggraph-first-principles-articles.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ articles</a> <a href="siggraph-diagrams.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ diagrams</a> <a href="siggraph-concept-paper-index.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ concept-paper index</a> <a href="siggraph-theme-audit.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ theme audit</a> <a href="siggraph-what-changed.html" style="display:inline-block;font-family:var(--mono);font-size:14px;color:var(--accent);border:1px solid var(--line);border-radius:9px;padding:10px 22px;text-decoration:none;margin-left:8px">→ what changed</a></p>'
    for path in [ROOT / "index.html", SITE / "index.html"]:
        text = path.read_text()
        if "siggraph-first-principles-articles.html" not in text:
            text = text.replace('<section>\n  <div class="eye">Go deeper</div>', f'<section>\\n  <div class="eye">First-principles support layer</div>\\n  <h2>Read the conference by hidden quantities</h2>\\n  <p>These pages connect the paper families into a learner-facing map: articles, field forces, synthesis, diagrams, reader paths, and a concept-to-paper index.</p>\\n  {links}\\n</section>\\n<section>\\n  <div class="eye">Go deeper</div>', 1)
            path.write_text(text)


def main():
    SITE.mkdir(exist_ok=True)
    families = load("families_rich.json")
    papers_data = load("papers.json")
    papers = papers_data.get("papers", []) if isinstance(papers_data, dict) else papers_data
    pages = {
        "siggraph-first-principles-articles.html": render_articles(families, papers),
        "siggraph-field-map.html": render_field_map(),
        "siggraph-synthesis.html": render_synthesis(),
        "siggraph-diagrams.html": render_diagrams(),
        "siggraph-reader-paths.html": render_reader_paths(),
        "siggraph-concept-paper-index.html": render_index(families, papers),
        "siggraph-theme-audit.html": render_theme_audit(families),
        "siggraph-what-changed.html": render_what_changed(),
    }
    for name, html in pages.items():
        (SITE / name).write_text(html)
        (ROOT / name).write_text(html)
    patch_home()
    print(f"wrote {len(pages)} support pages")


if __name__ == "__main__":
    main()
