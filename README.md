This extension designed for stable-diffusion-webui-forge automatically adjusts the "Noise Schedule for sampling" setting based on the currently loaded model's prediction type (Epsilon or V-Prediction). 

If a 'v_prediction' model is detected, the "Noise Schedule for sampling" (internally sd_noise_schedule) is automatically set to "Zero Terminal SNR".
For any other model type (assumed to be Epsilon-prediction or similar), the schedule is set to "Default".


### Installation:


1. Clone this repository into your stable-diffusion-webui-forge/extensions/ directory

2. Restart Forge.

You should see "[AutoNoiseSchedule] Extension loaded." in the terminal

