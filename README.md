Manually changing the "Noise Schedule for sampling" setting every time you switch models can be easy to forget. This extension designed for stable-diffusion-webui-forge automatically adjusts this setting based on the currently loaded model's prediction type (Epsilon or V-Prediction). 

If a 'v_prediction' model is detected, the "Noise Schedule for sampling" (internally sd_noise_schedule) is automatically set to "Zero Terminal SNR".
For any other model type (assumed to be Epsilon-prediction or similar), the schedule is set to "Default".


Installation:


Clone this repository into your stable-diffusion-webui-forge/extensions/ directory

Restart the Stable Diffusion WebUI Forge.
