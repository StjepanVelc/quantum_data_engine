class ExperimentConfig:
    def __init__(
        self,
        drive=True,
        entangle=True,
        noise=False,
        drive_strength=0.3,
        entangle_strength=0.2,
        noise_strength=0.01,
        bloch_update_every=5,
        heatmap_update_every=10,
    ):
        self.drive = drive
        self.entangle = entangle
        self.noise = noise

        self.drive_strength = drive_strength
        self.entangle_strength = entangle_strength
        self.noise_strength = noise_strength

        self.bloch_update_every = bloch_update_every
        self.heatmap_update_every = heatmap_update_every
